# OpenList 快速导入神器

便捷地批量添加网盘资源到 OpenList 的工具。

## 功能特性

- ✅ 支持多种网盘类型：阿里云盘、夸克网盘、115网盘、天翼云盘
- ✅ 批量导入资源链接
- ✅ 网盘账号管理（添加、删除、检测状态）
- ✅ 实时显示导入进度和结果
- ✅ 完善的错误处理和日志记录
- ✅ 支持环境变量配置
- ✅ Docker部署支持

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
└── .github/workflows/ # GitHub Actions工作流
    └── docker-push.yml # Docker Hub自动推送
```

## 安装与运行

### 1. 手动安装运行

```bash
# 克隆仓库
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

```bash
docker build -t openlist-importer .
docker run -d -p 3456:3456 --name openlist-importer openlist-importer
```

或使用环境变量：

```bash
docker run -d -p 3456:3456 \
  -e FLASK_SECRET=your-secret-key \
  --name openlist-importer \
  openlist-importer
```

## 如何使用

1. 打开浏览器访问应用页面
2. 配置OpenList地址和Admin Token
3. （可选）配置网盘账号信息
4. 在资源批量添加区粘贴资源链接，格式如下：

```
/阿里/电影 https://www.alipan.com/s/xxxx 1234
/夸克/资源 https://pan.quark.cn/s/xxxx
/115/资料 114514 1234567890ABCDEF 8888
/天翼/备份 https://cloud.189.cn/s/xxxx pwd
```

5. 点击"开始导入"，等待导入完成

## 上传到GitHub仓库

按照以下步骤手动上传到GitHub：

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

## Docker Hub自动推送

项目已配置GitHub Actions工作流，会在以下情况下自动构建并推送到Docker Hub：

- 推送到main分支
- 创建版本标签（如v1.0.0）

### 配置Docker Hub凭证

需要在GitHub仓库的Settings > Secrets and variables > Actions中添加以下Secrets：

- `DOCKERHUB_USERNAME`：Docker Hub用户名
- `DOCKERHUB_TOKEN`：Docker Hub访问令牌（在Docker Hub设置中生成）

## 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| FLASK_SECRET | Flask应用密钥 | openlist-importer-2025-final |

## 开发说明

### 项目依赖

- Flask 3.0.3
- requests 2.32.3
- python-dotenv 1.0.0

### 开发流程

```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

## 许可证

MIT
