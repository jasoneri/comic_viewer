#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pathlib
from urllib.parse import quote
import yaml

basepath = pathlib.Path(__file__).parent
yaml.warnings({'YAMLLoadWarning': False})


class Conf:
    comic_path = None
    handle_path = None

    def init(self):
        with open(basepath.parent.joinpath('conf.yml'), 'r', encoding='utf-8') as f:
            cfg = f.read()
        yml_config = yaml.load(cfg, Loader=yaml.FullLoader)
        self._get_path(yml_config)

    def _get_path(self, yml_config):
        def makedirs():
            comic_path.mkdir(exist_ok=True)
            handle_path.mkdir(exist_ok=True)
            handle_path.joinpath('save').mkdir(exist_ok=True)
            handle_path.joinpath('remove').mkdir(exist_ok=True)
        comic_path = pathlib.Path(yml_config['path']).joinpath('web')
        handle_path = comic_path.parent.joinpath(f"{comic_path.stem}_handle")
        makedirs()
        self.comic_path = comic_path
        self.handle_path = handle_path

    def __new__(cls, *args, **kwargs):
        if not hasattr(Conf, "_instance"):
            Conf._instance = super().__new__(cls, *args, **kwargs)
            Conf._instance.init()
        return Conf._instance


conf = Conf()


class BookCursor:
    head = 0

    def __init__(self, book_name, pages, sort_func=None):
        self.book_name = book_name
        self._pages = self._sort(pages, sort_func)
        self.tail = len(pages)

    @staticmethod
    def _sort(pages, func=None):
        func = func or (lambda x: int(re.search(r'\d+', x).group()))
        return sorted(pages, key=func)

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
