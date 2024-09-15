#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import shutil
import py7zr
from colorama import init, Fore

init(autoreset=True)


if __name__ == '__main__':
    """初次使用时，将预设极限压缩过的node依赖包解压至frontend"""
    root = pathlib.Path(__file__).parent.parent.parent
    scripts_p = root.joinpath('scripts')
    pkg = "node_modules"
    pkg_zip = f"{pkg}.7z"
    npm_pkg = root.joinpath(f"runtime/{pkg_zip}")
    os.system("npm config set registry https://registry.npm.taobao.org")
    if npm_pkg.exists():
        print(Fore.YELLOW + "[ 首次使用，初始化环境中.. ]")
        npm_pkg_p = scripts_p.joinpath(f'frontend/{pkg}')
        npm_pkg_p.mkdir(exist_ok=True)
        new_npm_pkg = scripts_p.joinpath(f'frontend/{pkg_zip}')
        shutil.move(npm_pkg, new_npm_pkg)
        with py7zr.SevenZipFile(new_npm_pkg, 'r') as zip_f:
            zip_f.extractall(npm_pkg_p)
        os.remove(new_npm_pkg)
        print(Fore.CYAN + "[ 初始化完成 ]")
    else:
        print(Fore.CYAN + "[ 无需初始化 ]")
