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

from utils import get_path, BookCursor

index_router = APIRouter(prefix='/comic')
comic_path, handle_path = get_path()
step = 25   # step与前端保持一致


class Cache:
    ...


global cache
cache = Cache()


class QuerySort(Enum):
    time = lambda x: os.path.getmtime(os.path.join(comic_path, x))
    name = lambda x: x
    asc = False
    desc = True

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)


@index_router.get("/")
async def get_books(request: Request, sort: str = Query(None)):
    sort = sort or "time_desc"  # 默认时间倒序
    func, _sort = sort.split("_")
    books = os.listdir(comic_path)
    return sorted(books, key=getattr(QuerySort, func), reverse=getattr(QuerySort, _sort).value)


@index_router.get("/{book_name}")
async def get_books(request: Request, book_name: str):
    book_md5 = hashlib.md5(book_name.encode('utf-8')).hexdigest()
    if not hasattr(cache, book_md5):
        setattr(cache, book_md5, BookCursor(book_name, os.listdir(comic_path.joinpath(book_name))))
    book = getattr(cache, book_md5)
    return book.get()


class Book(BaseModel):
    name: str
    handle: str  # save/remove/del
    
    
@index_router.post("/handle")
async def handle(request: Request, book: Book):
    book_path = comic_path.joinpath(book.name)
    if book.handle == "del":
        raise OSError('请自行寻找删除目录方法，本人并没提供相关删除文件代码并不承担错误删除文件的责任')
        # return {"path": book.name, "handled": f"{book.handle}eted"}
    if not os.path.exists(book_path):
        return JSONResponse(status_code=404, content=f"book[{book.name}] not exist]")
    _ = shutil.move(book_path, handle_path.joinpath(book.handle, book.name))
    return {"path": _, "handled": f"{book.handle}d"}
