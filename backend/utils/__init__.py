#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pathlib
import shutil
import typing as t
from urllib.parse import quote
from dataclasses import dataclass, asdict, field

import yaml
from platformdirs import user_config_path

basepath = pathlib.Path(__file__).parent
yaml.warnings({'YAMLLoadWarning': False})
conf_dir = user_config_path("redViewer", ensure_exists=False).parent
conf_dir.mkdir(parents=True, exist_ok=True)


def toAppConfigLocation(ori_file: pathlib.Path):
    file = ori_file.name
    location_file = conf_dir.joinpath(file)
    if ori_file.exists() and not location_file.exists():
        shutil.move(str(ori_file), str(location_file))
    return location_file


def yaml_update(_f, yaml_string):
    with open(_f, 'r+', encoding='utf-8') as fp:
        fp.seek(0)
        fp.truncate()
        fp.write(yaml_string)


@dataclass
class Conf:
    comic_path = None
    handle_path = None
    file = toAppConfigLocation(basepath.parent.joinpath('conf.yml'))
    path: t.Union[str, pathlib.Path] = None
    kemono_path: t.Union[str, pathlib.Path] = None
    scrollConf: dict = field(default_factory=dict)

    def __init__(self):
        self.init()

    def init(self):
        if not self.file.exists():
            with open(basepath.joinpath('conf_sample.yml'), 'r', encoding='utf-8') as fps:
                with open(self.file, 'w', encoding='utf-8') as fpw:
                    fpw.write(fps.read())
        with open(self.file, 'r', encoding='utf-8') as f:
            cfg = f.read()
        yml_config = yaml.load(cfg, Loader=yaml.FullLoader)
        for k, v in yml_config.items():
            if 'path' in k:
                v = pathlib.Path(v)
                v.mkdir(parents=True, exist_ok=True)
            self.__setattr__(k, v or getattr(self, k, None))
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
            setattr(Conf, "_instance", object.__new__(cls))
        return getattr(Conf, "_instance")

    def get_content(self):
        return self.file.read_text()

    def update(self, cfg):
        if isinstance(cfg, str):
            cfg_string = cfg
        else:
            _cfg = asdict(self)
            _cfg.update(cfg)
            for k, v in _cfg.items():
                if isinstance(v, pathlib.Path):
                    _cfg[k] = str(v)
            cfg_string = yaml.dump(_cfg, allow_unicode=True, sort_keys=False)
        yaml_update(self.file, cfg_string)
        self.init()


conf = Conf()


class BookCursor:
    head = 0
    static = "/static/"

    def __init__(self, book_name, pages, sort_func=None):
        self.book_name = book_name
        self._pages = self._sort(pages, sort_func)
        self.tail = len(pages)

    @staticmethod
    def _sort(pages, func=None):
        def _by_int(p):
            _int = re.search(r'\d+', p)
            if bool(_int):
                return int(_int.group())
            return 0
        func = func or _by_int
        return sorted(pages, key=func)

    def get(self, cursor=None):
        # 当内容非常非常多时，考虑后端根据游标返回批次内容时使用, 有游标时需要处理tail与step的比较, head递进step再比较tail（step与前端保持一致）
        return [f"{self.static}{quote(self.book_name)}/{pages}"
                for pages in self._pages[self.head:self.tail]]


class BookSort:
    section_regex = re.compile(r'_第?(\d+\.?\d*)([话卷])')
    volume_regex = re.compile(r'_第?(\d+\.?\d*)卷')

    @classmethod
    def by_section(cls, book_with_section):
        _s = cls.section_regex.search(book_with_section)
        book_name = book_with_section.split('_')[0]
        if not _s:
            return book_name, 2, 0
        num = float(_s.group(1))
        type_ = _s.group(2)
        priority = 0 if type_ == '卷' else 1
        if type_ == '卷' and '番外' in book_with_section:
            return book_name, priority, num + 0.5
        return book_name, priority, num

    @classmethod
    def get_sort_key(cls, book):
        name, priority, num = cls.by_section(book)
        return (name, priority, num)


class KemonoBookCursor(BookCursor):

    def __init__(self, u_s, book_name, pages, sort_func=None):
        self.u_s = u_s
        super(KemonoBookCursor, self).__init__(book_name, pages, sort_func)
        self.static = f"/static_kemono/{u_s}/"


if __name__ == '__main__':
    print(conf)