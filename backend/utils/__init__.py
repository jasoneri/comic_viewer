#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import pathlib
from urllib.parse import quote

basepath = pathlib.Path(__file__).parent


def get_path():
    with open(basepath.parent.joinpath('settings'), 'r', encoding='utf-8') as fp:
        text = fp.read()
    comic_path = pathlib.Path(re.findall(r'\[comic ([\s\S]*?)\]', text)[0])
    handle_path = pathlib.Path(re.findall(r'\[handle ([\s\S]*?)\]', text)[0])
    os.makedirs(comic_path, exist_ok=True)
    os.makedirs(handle_path, exist_ok=True)
    os.makedirs(handle_path.joinpath('save'), exist_ok=True)
    os.makedirs(handle_path.joinpath('remove'), exist_ok=True)
    return comic_path, handle_path


class BookCursor:
    head = 0

    def __init__(self, book_name, pages):
        self.book_name = book_name
        self._pages = self._sort(pages)
        self.tail = len(pages)

    @staticmethod
    def _sort(pages):
        return sorted(pages, key=lambda x: int(re.search(r'\d+', x).group()))

    def get(self, cursor=None):
        # 当内容非常非常多时，考虑后端根据游标返回批次内容时使用, 有游标时需要处理tail与step的比较, head递进step再比较tail（step与前端保持一致）
        return [f"/static/{quote(self.book_name)}/{pages}"
                for pages in self._pages[self.head:self.tail]]


class BookSort:
    section_regex = re.compile(r'(\d+\.?\d?)[话卷]')

    @classmethod
    def by_section(cls, book_with_section):
        _s = cls.section_regex.search(book_with_section)
        book_name = book_with_section.split('_')[0]
        return book_name, float(_s.group(1)) if bool(_s) else 0   # 前置使用此方法的是第一本书名，其余避免错误所以兜底0
