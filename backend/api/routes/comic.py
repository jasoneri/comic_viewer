#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
from enum import Enum

from fastapi import APIRouter, Query
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from utils import conf, BookCursor, BookSort

index_router = APIRouter(prefix='/comic')
step = 25   # step与前端保持一致


class Cache:
    ...


global cache
cache = Cache()


class QuerySort(Enum):
    time = lambda x: os.path.getmtime(conf.comic_path.joinpath(x))
    name = lambda x: x
    asc = False
    desc = True

    @classmethod
    def check_name(cls, book):
        cls.name = BookSort.by_section if bool(BookSort.section_regex.search(book)) else lambda x: x


@index_router.get("/")
async def get_books(request: Request, sort: str = Query(None)):
    sort = sort or "time_desc"  # 默认时间倒序
    func, _sort = sort.split("_")
    books = list(map(lambda _: _.name, filter(lambda x: x.is_dir(), conf.comic_path.iterdir())))
    if not books:
        return JSONResponse("no books exists", status_code=404)
    QuerySort.check_name(books[0])
    return sorted(books, key=getattr(QuerySort, func), reverse=getattr(QuerySort, _sort).value)


class ConfContent(BaseModel):
    text: str


@index_router.get("/conf")
@index_router.post("/conf")
async def duel_conf(request: Request, conf_content: ConfContent = None):
    if request.method == "GET":
        return conf.get_content()
    else:
        conf.update(conf_content.text)
        return "update conf successfully"


class ScrollConf(BaseModel):
    IntervalTime: int
    IntervalPixel: int


@index_router.get("/conf_scroll")
@index_router.post("/conf_scroll")
async def duel_scroll_conf(request: Request, scroll_conf: ScrollConf = None):
    if request.method == "GET":
        if not hasattr(conf, "scrollConf"):
            setattr(conf, "scrollConf", {"IntervalTime": 15, "IntervalPixel": 1})
        return {"IntervalTime": conf.scrollConf["IntervalTime"], "IntervalPixel": conf.scrollConf["IntervalPixel"]}
    else:
        conf.update({"scrollConf": {
            "IntervalTime": scroll_conf.IntervalTime, "IntervalPixel": scroll_conf.IntervalPixel
        }})
        return "update scroll conf successfully"


@index_router.get("/{book_name}")
async def get_book(request: Request, book_name: str):
    book_md5 = hashlib.md5(book_name.encode('utf-8')).hexdigest()
    if not hasattr(cache, book_md5):
        # todo except FileNotFoundError:
        setattr(cache, book_md5, BookCursor(book_name, os.listdir(conf.comic_path.joinpath(book_name))))
    book = getattr(cache, book_md5)
    return book.get()


class Book(BaseModel):
    name: str
    handle: str  # save/remove/del
    
    
@index_router.post("/handle")
async def handle(request: Request, book: Book):
    book_path = conf.comic_path.joinpath(book.name)
    with open(conf.handle_path.joinpath("record.txt"), "a+", encoding="utf-8") as f:
        f.writelines(f"<{book.handle}>{book.name}\n")
    if book.handle == "del":
        shutil.rmtree(book_path)
        return {"path": book.name, "handled": f"{book.handle}eted"}
    elif not os.path.exists(book_path):
        return JSONResponse(status_code=404, content=f"book[{book.name}] not exist]")
    else:
        _ = shutil.move(book_path, conf.handle_path.joinpath(book.handle, book.name))
        return {"path": _, "handled": f"{book.handle}d"}
