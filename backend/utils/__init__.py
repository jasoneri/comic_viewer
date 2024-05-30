#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import pathlib


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
        return [f"/static/{self.book_name}/{pages}"
                for pages in self._pages[self.head:self.tail]]
