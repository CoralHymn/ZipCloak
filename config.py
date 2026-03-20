#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配置管理模块"""
import os
import json
from typing import Dict

CONFIG_FILE = "zipcloak_config.json"

DEFAULT_EXTENSIONS = {
    ".txt": {"temp": ".txt1", "fake_hex": "2E 74 78 74 2F"},
    ".ini": {"temp": ".ini1", "fake_hex": "2E 69 6E 69 2F"},
    ".png": {"temp": ".png1", "fake_hex": "2E 70 6E 67 2F"},
    ".jpg": {"temp": ".jpg1", "fake_hex": "2E 6A 70 67 2F"},
    ".jpeg": {"temp": ".jpeg1", "fake_hex": "2E 6A 70 65 67 2F"},
    ".bmp": {"temp": ".bmp1", "fake_hex": "2E 62 6D 70 2F"},
    ".gif": {"temp": ".gif1", "fake_hex": "2E 67 69 66 2F"},
    ".py": {"temp": ".py1", "fake_hex": "2E 70 79 2F"},
    ".json": {"temp": ".json1", "fake_hex": "2E 6A 73 6F 6E 2F"},
    ".xml": {"temp": ".xml1", "fake_hex": "2E 78 6D 6C 2F"},
    ".cfg": {"temp": ".cfg1", "fake_hex": "2E 63 66 67 2F"},
    ".dat": {"temp": ".dat1", "fake_hex": "2E 64 61 74 2F"},
    ".pdf": {"temp": ".pdf1", "fake_hex": "2E 70 64 66 2F"},
    ".doc": {"temp": ".doc1", "fake_hex": "2E 64 6F 63 2F"},
    ".docx": {"temp": ".docx1", "fake_hex": "2E 64 6F 63 78 2F"},
}

DEFAULT_CONFIG = {
    "extensions": DEFAULT_EXTENSIONS.copy(),
    "last_source": "",
    "last_output": "",
    "compress": True,
    "language": "zh"
}

PRESET_EXTENSIONS = list(DEFAULT_EXTENSIONS.keys())


def generate_fake_hex(ext: str) -> str:
    """为扩展名生成伪装 16 进制"""
    fake_suffix = ext + "/"
    return ' '.join(f'{b:02X}' for b in fake_suffix.encode())


def load_config() -> dict:
    """加载配置，自动修复旧格式"""
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
            if "extensions" in loaded:
                for ext, info in loaded["extensions"].items():
                    if "temp" in info and "fake_hex" not in info:
                        info["fake_hex"] = generate_fake_hex(ext)
                        print(f"🔧 自动修复配置：{ext} 添加 fake_hex")
                    config["extensions"][ext] = info
            for key in ["last_source", "last_output", "compress", "language"]:
                if key in loaded:
                    config[key] = loaded[key]
        except Exception as e:
            print(f"⚠ 配置加载失败：{e}，使用默认配置")
    return config


def save_config(cfg: dict):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)