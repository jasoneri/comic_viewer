<div align="center">
  <h1 id="koishi">ComicViewer</h1>
  <img src="https://img.shields.io/badge/Backend-Python3.12-green.svg?colorA=abcdef" alt="tag">
  <img src="https://img.shields.io/badge/Frontend-Vite+elementPlus-blue.svg?colorA=abcdef" alt="tag">
</div>


## 📑介绍
超简单 fastapi + vue3 项目， pc本地下漫画(或任意图片目录)后用手机浏览器进行局域网阅读


▼ 预览 ▼

![](doc/assets/comic_viewer.jpg)

### 内容目录树参考
必改配置：`backend/conf.yml`中`path`的值（默认`D:\Comic`，切本就改成`D:\Comic\本子`，支持运行时热更改）
```shell
D:\Comic                              
   ├── web_handle                     # 程序创建的操作处理目录
        ├── save                      # 被保存的书
        ├── remove                    # 被移除的书
        └── record.txt                # 保存/移除/删除的记录，与`CGS.exe`的工具箱中的`已阅最新话数记录`关联
   └── web                            # 放内容（使用`CGS`的话目录结构就是已定的，使用自定义的话就需要创建这个`web`文件夹）
        └── GrandBlue碧蓝之海_第62话
             ├── 1.jpg
             ├── 2.jpg
             ......
```

> 打包好的开箱即用版 → [点击前往下载页面](https://github.com/jasoneri/comic_viewer/releases)，包名 `comic_viewer.7z`<br>
> 内含另外的 `部署指南` ，替代下面的 `准备/部署` 和 `运行`

> 使用可以参考 [CGS的使用指南](https://www.veed.io/view/zh-CN/688ae765-2bfb-4deb-9495-32b24a273373?panel=comments) ，
> `01:52` 开始


## 📢更新

### V1.6 | 2024-09-13

增加筛选按钮（重新加载键的右侧），<br>
能根据关键字筛出使页面仅显示包含关键字的书，按重新加载就能恢复
> mark一下：用手机edge测试时输入消息框与输入法之间有空白需要划一下去掉空白才能输入筛选成功，已反馈官方，用手机自带浏览器倒是没问题

## ⚡️准备/部署
### 版本
+ Python==3.12.3（实际3.8也行）
+ node  // newest
### backend
改配置：看上面的 [内容目录树参考](#内容目录树参考)，把漫画放进该目录的`web`文件夹内

```shell
cd backend
python -m pip install -r requirements.txt
```

### frontend
默认端口为8080，配置在`frontend/vite.config.js`
```shell
cd frontend
npm i
```
## 🚀运行
```shell
cd frontend
npm start
```
或在项目根目录运行脚本 `comic_viewer.bat`

## ✈️使用
启动后终端会显示局域网ip与端口 `Network:`行，手机进浏览器照样填地址即可，如预览所示

默认是删除功能没起效（防呆误删），熟悉后若需要删除功能，前往`backend/api/routes/comic.py`搜索`book.handle == "del"`，<br>
把下面两行解除注释 （<kbd># </kbd>去掉，注意去掉<kbd>#</kbd>后空格）

## 🔰其他
### kemono
配置`backend/conf.yml`中有个`kemono_path`，可观看从`CGS`脚本集下的`kemono`内容，
[点击查看`kemono`内容目录树参考](https://github.com/jasoneri/ComicGUISpider/blob/GUI/utils/script/script.md#%E8%BF%90%E8%A1%8C%E8%BF%87%E5%90%8E%E6%89%80%E5%BE%97%E7%9B%AE%E5%BD%95%E6%A0%91)， <br>
观看链接为 `你的局域网ip:端口/kemono`

## 💬交流
![](https://img.shields.io/badge/QQ群-437774506-blue.svg?colorA=abcopq)

## 🔇开源许可
详见 [MIT License](https://github.com/jasoneri/comic_viewer/blob/master/LICENSE)

---

![comic_viewer](https://count.getloli.com/get/@comic_viewer?theme=rule34)
