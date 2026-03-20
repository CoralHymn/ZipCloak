#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""混淆器模块"""
import os
import zipfile
from pathlib import Path
from typing import List, Callable, Optional
from config import generate_fake_hex
from utils import hex_to_bytes


class Obfuscator:
    """
    混淆流程:
    1. 创建临时 ZIP，文件名使用 .txt1 等临时扩展名
    2. 读取 ZIP 二进制数据
    3. 16 进制替换：.txt1 → .txt/ (让解压软件误判为文件夹)
    4. 保存为最终混淆 ZIP
    """
    
    def __init__(self, config: dict, selected_exts: List[str], log_callback: Callable = None):
        self.config = config
        self.selected_exts = set(selected_exts)
        self.ext_map = {}
        for ext in selected_exts:
            if ext in config['extensions']:
                info = config['extensions'][ext]
                if 'fake_hex' not in info:
                    info['fake_hex'] = generate_fake_hex(ext)
                self.ext_map[ext] = info
        self.log = log_callback or print
        self.stats = {'total': 0, 'obfuscated': 0}

    def _should_obfuscate(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in self.ext_map

    def _get_temp_name(self, filename: str) -> str:
        """获取临时文件名（.txt → .txt1）"""
        path = Path(filename)
        suffix = path.suffix.lower()
        if suffix in self.ext_map:
            return str(path.with_suffix('')) + self.ext_map[suffix]['temp']
        return filename

    def create(self, source_path: str, output_zip: str, compress=True, 
               progress_callback: Optional[Callable] = None):
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"源路径不存在：{source_path}")
        
        temp_zip = output_zip.replace('.zip', '_temp.zip')
        mode = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
        
        self.log(f"📦 步骤 1: 创建临时 ZIP (使用临时扩展名)...")
        with zipfile.ZipFile(temp_zip, 'w', mode) as zf:
            files = list(source.rglob('*'))
            total_files = len([f for f in files if f.is_file()])
            for idx, file_path in enumerate(files):
                if file_path.is_file():
                    rel_path = file_path.relative_to(source)
                    parts = list(rel_path.parts)
                    parts[-1] = self._get_temp_name(parts[-1])
                    arcname = '/'.join(parts)
                    zf.write(file_path, arcname)
                    self.stats['total'] += 1
                    if self._should_obfuscate(file_path.name):
                        self.stats['obfuscated'] += 1
                        self.log(f"  🔒 {rel_path} → {arcname}")
                    else:
                        self.log(f"  ✓ {rel_path}")
                    if progress_callback and total_files > 0:
                        progress_callback(int((idx + 1) / total_files * 50))
        
        self.log(f"  ✓ 临时 ZIP 创建完成：{temp_zip}")
        
        self.log(f"\n🔧 步骤 2: 执行 16 进制字节替换...")
        with open(temp_zip, 'rb') as f:
            data = f.read()
        
        replaced_count = 0
        for ext, info in self.ext_map.items():
            temp_bytes = info['temp'].encode()
            fake_bytes = hex_to_bytes(info['fake_hex'])
            if temp_bytes in data:
                count = data.count(temp_bytes)
                data = data.replace(temp_bytes, fake_bytes)
                replaced_count += count
                self.log(f"  🔁 替换：{temp_bytes!r} → {fake_bytes!r} ({count} 处)")
        
        self.log(f"\n💾 步骤 3: 保存混淆 ZIP...")
        with open(output_zip, 'wb') as f:
            f.write(data)
        
        if os.path.exists(temp_zip):
            os.remove(temp_zip)
        
        self.log(f"\n📦 混淆完成：{output_zip}")
        self.log(f"   总文件：{self.stats['total']}, 已混淆：{self.stats['obfuscated']}")
        self.log(f"   字节替换：{replaced_count} 处")
        self.log(f"   文件大小：{os.path.getsize(output_zip) / 1024:.2f} KB")
        return output_zip