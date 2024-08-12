<div align="center">
  <h1 id="koishi">ComicViewer</h1>
  <img src="https://img.shields.io/badge/Backend-Python3.12-green.svg?colorA=abcdef" alt="tag">
  <img src="https://img.shields.io/badge/Frontend-Vite+Vue3+elementPlus-blue.svg?colorA=abcdef" alt="tag">
</div>

超简单 fastapi + vue3 项目， pc本地下漫画(或任意图片目录)后用手机浏览器进行局域网阅读

## 预览
![](doc/comic_viewer.jpg)

> 打包好的开箱即用版 → [点击前往下载页面](https://github.com/jasoneri/comic_viewer/releases)，包名 `comic_viewer.7z`<br>
> 内含另外的 `部署指南` ，无需看以下说明

## 准备
### 版本
+ Python==3.12.3（实际3.8也行）
+ node  // newest
### backend
在`backend/conf.yml`修改目录，默认是`D:\Comic`, 把漫画放进该目录内，示例如下
```shell
yourComicPath
└── GrandBlue碧蓝之海_第62话
     ├── 1.jpg
     ├── 2.jpg
     ......
```
```shell
cd backend
python -m pip install -r requirements.txt
```

### frontend
默认端口为8080，配置在frontend/vite.config.js
```shell
cd frontend
npm i
```
## 部署运行
```shell
cd frontend
npm start
```

## 使用
启动后终端会显示局域网ip与端口 `Network:`行

手机进浏览器照样填地址即可，如预览所示

## 交流
群 437774506

## 免责声明
### 开源许可
详见 [MIT License](https://github.com/jasoneri/comic_viewer/blob/master/LICENSE)
### 注意事项
关于删除事项，要么自己写功能详见 `backend/api/routes/comic.py[50:9]`，要么直接使用当删除(del)不存在，所造成的后果与本人无关。
