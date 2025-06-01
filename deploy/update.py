#!/usr/bin/python
# -*- coding: utf-8 -*-
"""code update
base on client, env-python: embed"""
import base64
import json
import os
import shutil
import stat
import pathlib
import traceback
import zipfile

import httpx
from tqdm import tqdm
from colorama import init, Fore

init(autoreset=True)
path = pathlib.Path(__file__).parent.parent.parent
existed_proj_p = path.joinpath('scripts')
temp_p = path.joinpath('temp')
proxies = None
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
}


class TokenHandler:
    gitee_t_url = "https://gitee.com/json_eri/ComicGUISpider/raw/GUI/deploy/t.json"
    gitee_t_file = existed_proj_p.joinpath('deploy/gitee_t.json')

    def __init__(self):
        self.token = self.check_token()

    @property
    def headers(self):
        return {**headers, 'Authorization': self.token} if self.token else headers

    def check_token(self):
        if not self.gitee_t_file.exists():
            self.download_t_file()
        try:
            with open(self.gitee_t_file, 'r', encoding='utf-8') as f:
                tokens = json.load(f)
        except json.decoder.JSONDecodeError:
            tokens = []
        for _token in tokens:
            token = f"Bearer {base64.b64decode(_token).decode()}"
            with httpx.Client(headers={**headers, 'Authorization': token}) as client:
                resp = client.head(f"https://api.github.com")
                if str(resp.status_code).startswith('2'):
                    return token
        else:
            print(Fore.RED + ("[ 本地文件的token全部失效，当前将使用无状态去请求github api（受限60请求/小时）]\n"
                              "下次使用更新会重新下载token文件，还是全部失效的话可截图告知开发者"))
            os.remove(self.gitee_t_file)

    def download_t_file(self):
        with open(self.gitee_t_file, 'w', encoding='utf-8') as f:
            resp = httpx.get(self.gitee_t_url)
            resp_json = resp.json()
            json.dump(resp_json, f, ensure_ascii=False)


class GitHandler:
    speedup_prefix = "https://gh.llkk.cc/"

    def __init__(self, owner, proj_name, branch):
        self.sess = httpx.Client(proxies=proxies)
        self.commit_api = f"https://api.github.com/repos/{owner}/{proj_name}/commits"
        self.src_url = f"https://api.github.com/repos/{owner}/{proj_name}/zipball/{branch}"
        t_handler = TokenHandler()
        self.headers = t_handler.headers

    # src_url = f"{self.speedup_prefix}https://github.com/{self.github_author}/{proj_name}/archive/refs/heads/{branch}.zip"

    def normal_req(self, *args, **kwargs):
        resp = self.sess.get(*args, headers=self.headers, **kwargs)
        if not str(resp.status_code).startswith("2"):
            raise ValueError(resp.text)
        return resp.json()

    def get_version_info(self, ver):
        resp_json = self.normal_req(f"{self.commit_api}/{ver}")
        return resp_json

    def check_changed_files(self, ver):
        print(Fore.BLUE + "[ 检查版本中.. ]")
        resp_json = self.normal_req(self.commit_api)
        vers = list(map(lambda _: _["sha"], resp_json))
        if not ver:
            print(Fore.RED + "[ 没有version文件，准备初始化.. ]")
            return vers[0], []
        ver_index = vers.index(ver) if ver in vers else None
        valid_vers = vers[:ver_index]
        if len(valid_vers) > 10:
            print(Fore.YELLOW + f"[ 检测到堆积过多待更新版本，将忽略更新消息直接拉至最新版本代码... ]")
            return vers[0], ["*"]
        files = []
        print(Fore.BLUE + f"[ 检查需要更新的代码中.. ]")
        for _ver in valid_vers:
            resp_json = self.get_version_info(_ver)
            files.extend(list(map(lambda _: _["filename"], resp_json["files"])))
            print(Fore.GREEN + f"[ {_ver[:8]} ] {resp_json['commit']['message']}")
        out_files = list(set(files))
        if "deploy/update.py" in out_files:  # make sure update.py must be local-updated
            out_files.remove("deploy/update.py")
            out_files.insert(0, "deploy/update.py")
        return vers[0], out_files

    def download_src_code(self, _url=None, zip_name="src.zip"):
        """proj less than 1Mb, actually just take little second"""
        temp_p.mkdir(exist_ok=True)
        zip_file = temp_p.joinpath(zip_name)
        with self.sess.stream("GET", _url or self.src_url, follow_redirects=True) as resp:
            with open(zip_file, 'wb') as f:
                size = 50 * 1024
                for chunk in tqdm(resp.iter_bytes(size), ncols=80, ascii=True, desc=Fore.BLUE + "[ 下载代码文件中.. ]"):
                    f.write(chunk)
        return zip_file


class Proj:
    proj = "redViewer"
    github_author = "jasoneri"
    name = "redViewer"
    branch = "master"
    git_handler = GitHandler(github_author, name, branch)
    ver = ""
    first_flag = False
    local_ver = None
    changed_files = []

    def check_existed_version(self):
        local_ver_file = existed_proj_p.joinpath('version')
        if not local_ver_file.exists():
            self.first_flag = True
        else:
            with open(local_ver_file, 'r', encoding='utf-8') as f:
                return f.read().strip()

    def check(self):
        self.local_ver = local_ver = self.check_existed_version()
        self.ver, self.changed_files = self.git_handler.check_changed_files(local_ver)

    def local_update(self):
        def delete(func, _path, execinfo):
            os.chmod(_path, stat.S_IWUSR)
            func(_path)

        def move(src, dst):
            if src.is_dir() and dst.exists():
                shutil.rmtree(dst, ignore_errors=True)
                if dst.exists():  # fix
                    os.rmdir(dst)
            dst.parent.mkdir(exist_ok=True)
            if src.exists():
                shutil.move(src, dst)

        if not self.first_flag and not self.changed_files:
            print(Fore.CYAN + "[ 代码已是最新.. 若有其他问题向群里反映 ]")
            return

        proj_zip = self.git_handler.download_src_code()
        with zipfile.ZipFile(proj_zip, 'r') as zip_f:
            zip_f.extractall(temp_p)
        temp_proj_p = next(temp_p.glob(f"{self.github_author}-{self.name}*"))
        # REMARK(2024-08-08):      # f"{self.name}-{self.branch}"  this naming by src_url-"github.com/owner/repo/...zip"
        if self.first_flag or self.changed_files[0] == "*":
            # first_flag: when the first-time use this update(no version-file)
            print(Fore.YELLOW + "[ 首次使用更新，初始化覆盖中.. ]")
            _, folders, files = next(os.walk(temp_proj_p))
            all_files = (*folders, *files)
            for file in tqdm(all_files, total=len(all_files), ncols=80, ascii=True,
                             desc=Fore.BLUE + "[ 更新代码中.. ]"):
                move(temp_proj_p.joinpath(file), existed_proj_p.joinpath(file))
        else:
            for changed_file in tqdm(self.changed_files, total=len(self.changed_files),
                                     ncols=80, ascii=True, desc=Fore.BLUE + "[ 更新代码中.. ]"):
                move(temp_proj_p.joinpath(changed_file), existed_proj_p.joinpath(changed_file))
        shutil.rmtree(temp_p, onerror=delete)

    def end(self):
        with open(existed_proj_p.joinpath('version'), 'w', encoding='utf-8') as f:
            f.write(self.ver)
        print(Fore.GREEN + "=" * 40 + "[ 更新完毕 ]" + "=" * 40)


def regular_update():
    retry_times = 1
    __ = None
    try:
        proj = Proj()
        proj.check()
    except Exception as e:
        __ = traceback.format_exc()
        print(__)
        print(Fore.RED + f"[Errno 11001] 是网络问题，重试更新即可。 若其他情况导致更新一直失败请截图发issue或找群反映")
        return
    while retry_times < 4:
        try:
            proj.local_update()
            proj.end()
            break
        except Exception as e:
            __ = traceback.format_exc()
            print(Fore.RED + f"[ 更新失败, 准备重试-{retry_times} ]\n{type(e)} {e} ")
            retry_times += 1
    if retry_times > 3:
        print(__)
        print(Fore.RED + f"[Errno 11001] 是网络问题，重试更新即可。 若其他情况导致更新一直失败请截图发issue或找群反映")


if __name__ == '__main__':
    regular_update()
