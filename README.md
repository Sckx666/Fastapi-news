```markdown
# 📰 FastAPI News 项目

> 一个基于 FastAPI + Vue + Mysql + Redis 的前后端分离新闻系统。支持 Docker 一键部署与本地手动开发两种模式。

## ⚠️ 重要前置要求

**如果使用Docker启动，请提前把Mysql的3306端口和reodis的端口6379关闭！**  
项目依赖 Redis 进行缓存/会话管理，未启动 Redis 将导致显示速度变慢。

---

## 🐳 Docker 启动（推荐）

适用于快速体验或生产环境部署，无需手动配置数据库与依赖。

```bash
# 1. 克隆项目并进入根目录

# 2. 一键启动所有服务（后台运行）
docker compose up -d
```

启动成功后，可通过 `docker compose ps` 查看容器状态，访问对应端口即可使用。

---

## 🛠️ 手动启动（本地开发）

适用于二次开发与调试，需分别启动基础服务、后端与前端。

### 1️⃣ 启动基础服务

| 服务 | 操作说明 |
| :--- | :--- |
| **Redis** | 确保 Redis 服务已在后台正常运行 |
| **MySQL** | 启动 MySQL 服务后，需要手动运行mysql/init.sql文件，或者执行初始化脚本：<br>`mysql -u root -p < mysql/init.sql` |

### 2️⃣ 启动后端

```bash
# 进入后端目录
cd FastApi-news

# 安装依赖
pip install -r requirements.txt

# 启动主程序
python main.py
```

### 3️⃣ 启动前端

```bash
# 进入前端目录
cd 

# 安装依赖（首次运行需要）
npm install

# 启动开发服务器
npm run dev
```

> 💡 **快捷操作**：在前端文件夹内右键 → 「在终端中打开」→ 输入 `npm run dev` 即可启动。

---


## ❓ 常见问题

| 问题现象 | 解决方案 |
| :--- | :--- |
| 启动时报连接错误 | 检查 Redis 是否已启动并监听正确端口 |
| 数据库表不存在 / 数据为空 | 确认已成功执行 `mysql/init.sql` 脚本 |
| pip 安装依赖失败 | 建议使用虚拟环境，或更换国内镜像源 |
| Docker 端口被占用 | 修改 `docker-compose.yml` 中的端口映射配置 |
| 前端页面空白 / 接口404 | 检查后端是否正常运行，以及前端代理配置是否正确 |
