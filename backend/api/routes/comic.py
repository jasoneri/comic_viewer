#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
import random
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Query
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from send2trash import send2trash

from utils import conf, BookCursor, BookSort, quote

index_router = APIRouter(prefix='/comic')
step = 25   # step与前端保持一致
executor = ThreadPoolExecutor(max_workers=1)


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
    def check_name(cls, books):
        if all(bool(BookSort.section_regex.search(book)) for book in books):
            cls.name = BookSort.get_sort_key


@index_router.get("/")
async def get_books(request: Request, sort: str = Query(None)):
    sort = sort or "time_desc"  # 默认时间倒序
    func, _sort = sort.split("_")
    books = list(map(lambda _: _.name, filter(lambda x: x.is_dir(), conf.comic_path.iterdir())))
    if not books:
        return JSONResponse("no books exists", status_code=404)
    QuerySort.check_name(random.choices(books, k=5))
    out_books = sorted(books, key=getattr(QuerySort, func), reverse=getattr(QuerySort, _sort).value)
    
    result = []
    for book in out_books:
        try:
            first_img = next(conf.comic_path.joinpath(book).iterdir()).name
        except StopIteration:
            first_img = None
        result.append({"book_name": book, "first_img": f"/static/{quote(book)}/{first_img}"})
    return result


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


@index_router.get("/{book_name}")
async def get_book(request: Request, book_name: str):
    book_md5 = hashlib.md5(book_name.encode('utf-8')).hexdigest()
    book_path = conf.comic_path.joinpath(book_name)
    if not os.path.exists(book_path):
        if hasattr(cache, book_md5):
            return getattr(cache, book_md5).get()
        return JSONResponse(status_code=404, content=f"book[{book_name}] not exist]")
    if not hasattr(cache, 'order'):
        cache.order = []
    if hasattr(cache, book_md5):
        cache.order.remove(book_md5)
        cache.order.append(book_md5)
    else:
        cache_attrs = [a for a in vars(cache) if not a.startswith('_')]
        if len(cache_attrs) > 30:
            remove_keys = cache.order[:len(cache_attrs)//2]
            for key in remove_keys:
                delattr(cache, key)
                cache.order.remove(key)
        setattr(cache, book_md5, BookCursor(book_name, os.listdir(conf.comic_path.joinpath(book_name))))
        cache.order.append(book_md5)
    book = getattr(cache, book_md5)
    return book.get()


class Book(BaseModel):
    name: str
    handle: str  # save/remove/del
    
    
@index_router.post("/handle")
async def handle(request: Request, book: Book):
    book_path = conf.comic_path.joinpath(book.name)
    if not os.path.exists(book_path):
        return JSONResponse(status_code=404, content=f"book[{book.name}] not exist]")
    with open(conf.handle_path.joinpath("record.txt"), "a+", encoding="utf-8") as f:
        f.writelines(f"<{book.handle}>{book.name}\n")
    if book.handle == "del":
        shutil.rmtree(book_path)
        return {"path": book.name, "handled": f"{book.handle}eted"}
    elif book.handle == "remove":
        asyncio.get_event_loop().run_in_executor(executor, send2trash, book_path)
        return JSONResponse({"path": book.name, "handled": f"{book.handle}d"})
    else:
        _ = shutil.move(book_path, conf.handle_path.joinpath(book.handle, book.name))
        return {"path": _, "handled": f"{book.handle}d"}
