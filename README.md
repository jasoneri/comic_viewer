# ComicViewer
![](https://img.shields.io/badge/Backend-Python3.12-green.svg?colorA=abcdef)  ![](https://img.shields.io/badge/Frontend-Vite+Vue3+elementPlus-blue.svg?colorA=abcdef)  

超简单 fastapi + vue3 项目， pc本地下漫画(或任意图片目录)后用手机浏览器进行局域网阅读

## 预览
![](https://images.cnblogs.com/cnblogs_com/jsoneri/2401311/o_240530080611_comic_viewer.png)

## 部署
### 版本
> Python==3.12.3（实际3.8也行）<br>
> node 最新
### backend
> 在backend/settings 修改目录，把内容放进comic目录内，示例如下
```shell
yourComicPath
└── GrandBlue碧蓝之海62话
     ├── 1.jpg
     ├── 2.jpg
     ......
```
```shell
cd backend
python -m pip install -r requirements.txt
python app.py
```

### frontend
```shell
cd frontend
npm i
npm run dev
```
> 默认端口为8080，配置在vite.config.js

## 使用
查查你pc局域网ip，手机进ip:8080就行，如预览所示