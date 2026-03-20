#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""此模块由QwenAI生成"""
"""多语言支持模块"""
import os
import json
from typing import Dict

LANG_DIR = "lang"
DEFAULT_LANG = "zh"


class LanguageLoader:
    """语言加载器类"""
    
    def __init__(self):
        self.languages = {}
        self.current_lang = DEFAULT_LANG
        
    def load_language(self, lang_code: str) -> Dict:
        """加载指定语言文件"""
        lang_file = os.path.join(LANG_DIR, f"{lang_code}.json")
        
        if not os.path.exists(lang_file):
            print(f"⚠ 语言文件不存在：{lang_file}，使用默认语言")
            lang_file = os.path.join(LANG_DIR, f"{DEFAULT_LANG}.json")
        
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠ 语言文件加载失败：{e}")
            return {}
    
    def set_language(self, lang_code: str):
        """设置当前语言"""
        self.current_lang = lang_code
        if lang_code not in self.languages:
            self.languages[lang_code] = self.load_language(lang_code)
    
    def get_text(self, key: str, **kwargs) -> str:
        """获取翻译文本，支持格式化参数"""
        if self.current_lang not in self.languages:
            self.set_language(self.current_lang)
        
        texts = self.languages.get(self.current_lang, {})
        text = texts.get(key, key)  # 如果找不到 key，返回 key 本身作为降级
        
        # 支持格式化参数替换
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text
    
    def get_available_languages(self) -> list:
        """获取所有可用的语言列表"""
        langs = []
        if os.path.exists(LANG_DIR):
            for file in os.listdir(LANG_DIR):
                if file.endswith('.json'):
                    langs.append(file[:-5])  # 去掉 .json 后缀
        return langs if langs else [DEFAULT_LANG]


# 全局语言加载器实例
lang_loader = LanguageLoader()


def get_text(key: str, **kwargs) -> str:
    """便捷函数：获取翻译文本"""
    return lang_loader.get_text(key, **kwargs)


def set_language(lang_code: str):
    """便捷函数：设置语言"""
    lang_loader.set_language(lang_code)


def get_available_languages() -> list:
    """便捷函数：获取可用语言列表"""
    return lang_loader.get_available_languages()
