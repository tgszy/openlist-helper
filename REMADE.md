# OpenList 快速导入神器使用说明

## 项目简介

OpenList 快速导入神器是一个便捷的工具，用于批量添加阿里云盘、夸克网盘、115网盘和天翼云盘资源到 OpenList。它提供了极简的 WebUI 界面，支持智能识别多种网盘格式，并具备完善的账号管理功能。

## 安装与运行

### 1. Docker运行

**方式一：本地构建镜像**

```bash
docker build -t openlist-helper .
docker run -d -p 3456:3456 --name openlist-helper openlist-helper
```

**方式二：使用环境变量**

```bash
docker run -d -p 3456:3456 \
  -e FLASK_SECRET=your-secret-key \
  --name openlist-helper \
  openlist-helper
```

**方式三：直接使用Docker Hub镜像**

```bash
docker run -d -p 3456:3456 --name openlist-helper <your-dockerhub-username>/openlist-helper:latest
```

### 2. Docker Compose运行

**方式一：使用默认配置**

```bash
# 创建docker-compose.yml文件（如果尚未创建）
# 内容已默认包含在项目中
version: '3.8'

services:
  openlist-helper:
    build: .
    image: openlist-helper
    container_name: openlist-helper
    ports:
      - "3456:3456"
    environment:
      - FLASK_SECRET=openlist-helper-2025-final
    restart: unless-stopped

# 启动服务
docker-compose up -d
```


## 使用方法

1. **访问应用**：打开浏览器访问 `http://localhost:3456`

2. **配置OpenList**：
   - 在界面中配置OpenList地址
   - 输入Admin Token

3. **配置网盘账号**（可选）：
   - 添加网盘账号信息
   - 检测账号状态
   - 管理现有账号（编辑/删除）

4. **批量添加资源**：
   - 在资源批量添加区粘贴资源链接
   - 支持以下格式：

     ```
     /阿里/电影 https://www.alipan.com/s/xxxx 1234
     /夸克/资源 https://pan.quark.cn/s/xxxx
     /115/资料 114514 1234567890ABCDEF 8888
     /天翼/备份 https://cloud.189.cn/s/xxxx pwd
     ```

5. **开始导入**：点击"开始导入"按钮，等待导入完成

6. **查看结果**：实时查看导入进度和结果反馈
