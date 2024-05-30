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
> 查查pc局域网ip，并在frontend/src/utils/settings.js中ip部分更改成查的ip（处理前端跨域）<br>
> 默认端口为8080，配置在frontend/vite.config.js

```shell
cd frontend
npm i
npm run dev
```

## 使用
手机进 `pc局域网ip:8080` 就行，如预览所示

## 注意事项
免责声明：关于删除事项，要么自己写功能详见 `backend/api/routes/comic.py[50:9]`，要么直接使用当删除(del)不存在