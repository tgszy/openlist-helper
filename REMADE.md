# OpenList 快速导入神器使用说明

## 项目简介

OpenList 快速导入神器是一个便捷的工具，用于批量添加阿里云盘、夸克网盘、115网盘和天翼云盘资源到 OpenList。它提供了极简的 WebUI 界面，支持智能识别多种网盘格式，并具备完善的账号管理功能。

## 功能特性

- ✅ **多网盘支持**：阿里云盘、夸克网盘、115网盘、天翼云盘
- ✅ **批量导入**：一键批量添加分享链接，智能识别四盘格式
- ✅ **账号管理**：添加、删除、检测网盘账号状态
- ✅ **实时反馈**：实时显示导入进度和结果
- ✅ **错误处理**：完善的错误处理和日志记录
- ✅ **环境配置**：支持环境变量配置
- ✅ **Docker部署**：支持Docker一键部署
- ✅ **美观界面**：深色美观界面 + HTMX 无刷新交互

## 安装与运行

### 1. 手动安装运行

```bash
# 克隆仓库（需先安装Git）
git clone <your-repo-url>
cd openlist_helper

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
copy .env.example .env
# 编辑.env文件，设置FLASK_SECRET等变量

# 启动应用
python app.py
```

应用将在 `http://0.0.0.0:3456` 运行。

### 2. Docker运行

**方式一：本地构建镜像**

```bash
docker build -t openlist-importer .
docker run -d -p 3456:3456 --name openlist-importer openlist-importer
```

**方式二：使用环境变量**

```bash
docker run -d -p 3456:3456 \
  -e FLASK_SECRET=your-secret-key \
  --name openlist-importer \
  openlist-importer
```

**方式三：直接使用Docker Hub镜像**

```bash
docker run -d -p 3456:3456 --name openlist-importer <your-dockerhub-username>/openlist-importer:latest
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

## 环境变量配置

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| FLASK_SECRET | Flask应用密钥 | openlist-importer-2025-final |

## 部署到GitHub和Docker Hub（可选）

### 1. 上传到GitHub仓库

1. **创建GitHub仓库**
   - 登录GitHub，点击右上角"+"号，选择"New repository"
   - 填写仓库名称（如openlist-helper），选择是否公开
   - 点击"Create repository"

2. **初始化本地仓库**
   ```bash
   # 在项目根目录执行
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **关联远程仓库**
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   ```

4. **推送代码**
   ```bash
   git push -u origin main
   ```

### 2. 配置Docker Hub自动推送

项目已配置GitHub Actions工作流，会在以下情况下自动构建并推送到Docker Hub：
- 推送到main分支
- 创建版本标签（如v1.0.0）

**配置步骤**：
1. 在GitHub仓库的Settings > Secrets and variables > Actions中添加以下Secrets：
   - `DOCKERHUB_USERNAME`：Docker Hub用户名
   - `DOCKERHUB_TOKEN`：Docker Hub访问令牌（在Docker Hub设置中生成）

## 项目结构

```
openlist_helper/
├── app.py              # 应用入口文件
├── app/               # 主应用包
│   ├── __init__.py    # 应用初始化
│   ├── routes.py      # 路由定义
│   └── utils/         # 工具函数
│       └── parsers.py # 资源解析函数
├── requirements.txt   # Python依赖列表
├── Dockerfile         # Docker构建配置
├── .env.example       # 环境变量示例
├── .github/workflows/ # GitHub Actions工作流
│   └── docker-push.yml # Docker Hub自动推送
├── README.md          # 英文项目说明
├── REMADE.md          # 简化版功能介绍
└── 使用说明.md        # 中文使用说明（本文件）
```

## 开发说明

### 项目依赖

- Flask 3.0.3
- requests 2.32.3
- python-dotenv 1.0.0

### 开发流程

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

## 许可证

MIT
