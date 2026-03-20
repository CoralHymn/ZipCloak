#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工具函数模块"""
import hashlib


def hex_to_bytes(hex_str: str) -> bytes:
    """将空格分隔的 16 进制字符串转为 bytes"""
    return bytes.fromhex(hex_str.replace(' ', ''))


def bytes_to_hex(data: bytes) -> str:
    """将 bytes 转为空格分隔的 16 进制字符串"""
    return ' '.join(f'{b:02X}' for b in data)


def calculate_file_hash(filepath: str) -> str:
    """计算文件 SHA256 哈希（前 16 位）"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]