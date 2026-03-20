#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""恢复器模块"""
import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Callable, Optional
from io import BytesIO
from config import generate_fake_hex
from utils import hex_to_bytes


class Restorer:
    """
    恢复流程:
    1. 读取混淆 ZIP 二进制数据
    2. 16 进制替换：.txt/ → .txt1 (恢复为正常 ZIP)
    3. 解压到临时目录
    4. 批量重命名：.txt1 → .txt
    5. 输出到目标目录
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
        self.stats = {'fixed': 0, 'extracted': 0, 'renamed': 0}
        self.temp_dir = None

    def _patch_zip_bytes(self, zip_path: str) -> Optional[bytes]:
        """字节级修复：将 .txt/ 替换为 .txt1"""
        with open(zip_path, 'rb') as f:
            data = f.read()
        modified = False
        for ext, info in self.ext_map.items():
            fake_bytes = hex_to_bytes(info['fake_hex'])
            temp_bytes = info['temp'].encode()
            if fake_bytes in data:
                count = data.count(fake_bytes)
                data = data.replace(fake_bytes, temp_bytes)
                self.stats['fixed'] += count
                modified = True
                self.log(f"  🔧 替换：{fake_bytes!r} → {temp_bytes!r} ({count} 处)")
        return data if modified else None

    def _extract_zip(self, zip_data: bytes, extract_to: str, 
                     progress_callback: Optional[Callable] = None):
        """从内存 ZIP 数据提取文件"""
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(BytesIO(zip_data), 'r') as zf:
            members = [m for m in zf.namelist() if not m.endswith('/')]
            total = len(members)
            for idx, member in enumerate(members):
                try:
                    zf.extract(member, extract_to)
                    self.stats['extracted'] += 1
                    self.log(f"  ✓ 提取：{member}")
                except Exception as e:
                    self.log(f"  ✗ 提取失败 {member}: {e}")
                if progress_callback and total > 0:
                    progress_callback(int((idx + 1) / total * 50))

    def _rename_extracted_files(self, extract_to: str, 
                                progress_callback: Optional[Callable] = None):
        """批量重命名恢复原始扩展名"""
        renamed = 0
        files = [f for f in Path(extract_to).rglob('*') if f.is_file()]
        total = len(files)
        for idx, file_path in enumerate(files):
            suffix = file_path.suffix.lower()
            for ext, info in self.ext_map.items():
                if suffix == info['temp']:
                    new_suffix = ext
                    new_name = file_path.stem + new_suffix
                    new_path = file_path.parent / new_name
                    counter = 1
                    while new_path.exists():
                        new_path = file_path.parent / f"{file_path.stem}_{counter}{new_suffix}"
                        counter += 1
                    file_path.rename(new_path)
                    self.log(f"  ✏️  重命名：{file_path.name} → {new_path.name}")
                    renamed += 1
                    break
            if progress_callback and total > 0:
                progress_callback(50 + int((idx + 1) / total * 50))
        self.stats['renamed'] = renamed
        self.log(f"📝 重命名完成：{renamed} 个文件")

    def restore(self, zip_path: str, output_dir: str, create_zip=False,
                progress_callback: Optional[Callable] = None):
        self.log(f"🔍 分析文件：{zip_path}")
        self.log(f"   文件大小：{os.path.getsize(zip_path) / 1024:.2f} KB")
        
        self.log(f"\n🔧 步骤 1: 修复 ZIP 字节结构...")
        patched_data = self._patch_zip_bytes(zip_path)
        if not patched_data:
            self.log("⚠ 未找到需要修复的混淆标记，尝试直接提取...")
            with open(zip_path, 'rb') as f:
                patched_data = f.read()
        else:
            self.log(f"  ✓ 共修复 {self.stats['fixed']} 处字节")
        
        self.temp_dir = output_dir + "_temp"
        self.log(f"\n📦 步骤 2: 提取到临时目录 {self.temp_dir} ...")
        self._extract_zip(patched_data, self.temp_dir, progress_callback)
        
        self.log(f"\n✏️  步骤 3: 恢复原始扩展名...")
        self._rename_extracted_files(self.temp_dir, progress_callback)
        
        os.makedirs(output_dir, exist_ok=True)
        for item in Path(self.temp_dir).iterdir():
            dest = Path(output_dir) / item.name
            if item.is_file():
                shutil.copy2(item, dest)
            else:
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
        
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.log(f"  ✓ 已清理临时目录")
        
        self.log(f"\n✅ 恢复完成!")
        self.log(f"   修复标记：{self.stats['fixed']}, 提取文件：{self.stats['extracted']}, 重命名：{self.stats['renamed']}")
        return True