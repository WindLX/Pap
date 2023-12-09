# Pap

## 简介

Pap 是一个pdf文件管理软件，提供了简洁的世界 Web 页面，通过标签对文件进行管理，可为托管文件自由添加 markdown 笔记.

## 安装

Pap 需要 Python 3.11.4 的运行环境. 所有脚本均可通过 `Get-Help script.ps1` (Windows) 或者 `script.sh --help` (Linux) 获取帮助信息

### Windows/Linux

从 `release` 中下载最新版本的压缩包 `PapPack`，解压后在 `PapPack` 目录下运行 `.\pap.ps1` (Windows) 或者 `./pap/sh` (Linux) 即可启动程序，用浏览器打开对应的网络地址即可查看.

### Docker

运行 `docker build -t pap .` 即可构建 docker 镜像，容器内默认服务地址为 `172.17.0.2:13956`，容器暴露端口为 `13956`

### 从源码构建

从源码构建 Pap 需要安装 Node.js v18.17.0 和 Python 3.11.4 运行时，在项目目录下运行 `.\scripts\tools.ps1 -Pack` (Windows) 或者 `./scripts/tool.sh --pack` (Linux) 即可

## 开发

`scripts\tool.ps1` 和 `scripts/tool.sh` 提供了一些实用开发工具，如静态类型检查，测试，编译构建和打包。通过 `Get-Help .\scripts\tools.ps1` 或者 `./scripts/tool.sh --help` 命令获取脚本的更多帮助信息.

## TODO

- [x] Markdown Parser
- [x] Markdown Editor
- [x] File Lock
- [x] Not save tip
- [x] File Rename
- [x] Note Tag
- [x] Rightbar
- [x] Private Lock
- [ ] Keymap
- [ ] Style
- [x] Title List
- [x] Markdown Ref net
- [x] Resource
- [x] Pdf viewer
- [x] Music viewer
- [ ] Video viewer
- [x] Data Export
- [ ] Table
- [ ] Database
- [ ] OCR