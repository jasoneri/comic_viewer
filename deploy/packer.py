#!/usr/bin/python
# -*- coding: utf-8 -*-
"""code packer
env-python: developer
"""
import os
import shutil
import pathlib
import stat
import datetime

import py7zr

from tqdm import tqdm
from loguru import logger
from github import Github, Auth

# import github.Requester  # REMARK(2024-08-08): modified in package: HTTPSRequestsConnectionClass.session.proxies


path = pathlib.Path(__file__).parent
api_github = "https://api.github.com"
github_token = "**create token by your github account**"
proxies = None
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Origin": "https://github.com",
    "Connection": "keep-alive",
    "Referer": "https://github.com/",
    "Priority": "u=0",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}
preset = {
    "python": ["api-ms-win-core", "base_library.zip", ".tcl", "tclIndex", "MSVCP140.dll", "cacert.pem", "cp936.enc",
               "__init__", "python.exe", "pythonw.exe", "VCRUNTIME140_1.dll"],
    "matplotlib": ["matplotlibrc", ".load-order", "matplotlib.svg"], "request": ["msgcat-1.6.1.tm"],
    "plotly": ["plotly.json", "plotly.min.js", "package_data\\templates"], "pyecharts": ["pyecharts"],
    "pyqtwebengine": ["QtWebEngineProcess.exe", "icudtl.dat", "qtwebengine_devtools_resources.pak",
                      "qtwebengine_resources", "qt.conf"], "streamlit": ["streamlit\\static"],
    "trame_vtk": ["static_viewer.html"], "python-docx": ["docx\\templates"], "python-pptx": ["pptx\\templates"],
    "scrapy": ["mime.types"]}
release_desc = """开箱即用
---
### 下载
下面的`comic_viewer.7z`<br>
下载很慢 ？到压缩包的下载链接右键复制到 https://github.akams.cn/ 上进行下载加速

### 运行
解压双击运行 `comic_viewer.exe`

### 更新
一般情况下，使用包内的更新程序 `comic_viewer-更新.exe` 即可<br>
特殊情况，如运行环境需要变化时，需要在此页面下绿色安装包 (包更新未必是最新，更新日期参照标题) 
> 绿色包保证 `运行环境` 的更新，更新程序保证 `代码` 的更新，<br>
> 所以会有包更新没跟上代码更新，优先以内置的`comic_viewer-更新.exe` 为主

---
其他问题 [回到项目主页](https://github.com/jasoneri/comic_viewer) 下方找群进群询问"""


class Proj:
    proj = "comic_viewer"
    name = "comic_viewer"

    def __repr__(self):
        return self.proj


proj = Proj()


class Clean:
    """aim at runtime like site-packages"""

    @staticmethod
    def clean_packages():
        """clean site-packages"""
        package_p = path.joinpath('site-packages')
        for p in tqdm(package_p.glob("[psw][ieh][pte]*")):  # pip, set-tools, wheel, not need
            shutil.rmtree(str(p), ignore_errors=True)

    @staticmethod
    def end_work(specified: iter = None):
        def delete(func, _path, execinfo):
            os.chmod(_path, stat.S_IWUSR)
            func(_path)

        waiting = specified or ("scripts/.git", )
        for p in tqdm(waiting):
            _p = path.joinpath(p)
            if _p.exists():
                shutil.rmtree(_p, onerror=delete) if _p.is_dir() else os.remove(_p)


class Packer:
    github_author = "jasoneri"
    executor = path.parent.joinpath(r'Bat_To_Exe_Converter\Bat_To_Exe_Converter.exe')
    zip_file = path.joinpath(f'{proj}.7z')
    preset_zip_file = path.joinpath(f'{proj}_preset.7z')

    def __init__(self, default_specified: tuple):
        self.default_specified = default_specified

    @classmethod
    def bat_to_exe(cls):
        def _do(bat_file, exe_file, icon, *args):
            if exe_file.exists():
                os.remove(exe_file)
            args_str = " ".join(args)
            command = f"cd {path} && {cls.executor} /bat {bat_file} /exe {exe_file} /icon {icon} /x64 {args_str}"
            error_code = os.system(command)
            if error_code:  # Unreliable, need raise error make next step run correctly
                raise OSError(f"[ fail - packup {bat_file}], error_code: {error_code}")
            else:
                logger.info(f"[ success {bat_file} ]")

        _do(path.joinpath(rf"scripts/launcher/{proj}.bat"), path.joinpath(rf"{proj}.exe"),
            path.joinpath(rf"scripts/launcher/{proj}.ico"), "/uac-user")
        _do(path.joinpath(rf"scripts/launcher/update.bat"), path.joinpath(rf"{proj}-更新.exe"),
            path.joinpath(rf"scripts/launcher/{proj}.ico"))

    @staticmethod
    def markdown_to_html(file_path, out_name):
        import markdown
        with open(path.joinpath(file_path), 'r', encoding='utf-8') as f:
            md_content = f.read()
        html = markdown.markdown(md_content.replace(r"![](", "![](scripts\\doc\\"))
        html_style = f"""<!DOCTYPE html><html><head><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css"></head><body><article class="markdown-body">
        {html}
        </article></body></html>"""
        with open(path.joinpath(out_name), 'w', encoding='utf-8') as f:
            f.write(html_style)

    def packup(self, runtime_init=False):
        zip_file = self.zip_file
        specified = self.default_specified
        mode = "a"
        if runtime_init:
            # {proj}_preset.7z: only include runtime and site-packages. If env changed, re-packup it
            if self.preset_zip_file.exists():
                logger.debug(f"[ preset_zip_file exists ] run normal packup")
                logger.debug(f"[ if need init ] delete '{self.preset_zip_file}' manually later")
                return self.packup()
            zip_file = self.preset_zip_file
            specified = ('runtime', 'site-packages')
            mode = "w"
        else:
            shutil.copy(self.preset_zip_file, self.zip_file)
        with py7zr.SevenZipFile(zip_file, mode, filters=[{"id": py7zr.FILTER_LZMA2}]) as zip_f:
            for file in tqdm(tuple(specified)):
                if path.joinpath(file).exists():
                    zip_f.writeall(file)
        if not self.zip_file.exists():
            self.packup()

    @staticmethod
    def upload(zip_file):
        date_now = datetime.datetime.now().strftime("%Y%m%d")
        repo = proj.name
        if github_token.startswith("**create"):
            raise ValueError("[ you forget to replace your github token ] ")
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        user = g.get_user()
        release = user.get_repo(repo).get_latest_release()
        # delete asset
        """github note:
        If you upload an asset with the same filename as another uploaded asset,
        you'll receive an error and must delete the old file before you can re-upload the new asset."""
        _asset = list(filter(lambda x: x.name == zip_file, release.assets))
        if _asset:
            _asset[0].delete_asset()
        # upload asset
        release.upload_asset(str(path.joinpath(zip_file)), name=zip_file)
        # update release
        text = release_desc
        release.update_release(name=f"{date_now} - v1.1.0", message=text)


def clean():
    """almost run few times in upfront"""
    Clean.clean_packages()
    Clean.end_work()


if __name__ == '__main__':
    # clean()                   # step 0
    Packer.bat_to_exe()  # step 1
    Packer.markdown_to_html('scripts/doc/deploy.md', '部署指南.html')  # step 2
    packer = Packer(('scripts', f'{proj}.exe', f'{proj}-更新.exe', '部署指南.html'))
    packer.packup(runtime_init=True)  # step 3
    packer.upload('comic_viewer.7z')  # step 4
    Clean.end_work((f'{proj}.exe', f'{proj}-更新.exe', 'comic_viewer.7z', '部署指南.html'))  # step 5
    # If error occur, exegesis previous step and run again
