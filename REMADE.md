# OpenList 快速导入神器

批量导入阿里云盘、夸克、115、天翼云盘资源到 OpenList 的极简 WebUI 工具。

## 功能
- 一键批量添加分享链接
- 智能识别四盘格式
- 配置网盘账号（刷新/新增/检测/编辑/删除）
- 深色美观界面 + HTMX 无刷新交互
- Docker 一键部署 + GitHub → Docker Hub 自动构建

## 启动
```bash
docker run -d -p 3456:3456 --name openlist-importer <your-dockerhub-username>/openlist-importer:latest