# 创伤地图和伤情预测系统 — 新手部署指南

> 面向零 Docker 经验的用户。跟着步骤走，20 分钟内完成部署。

---

## 目录

- [1. 准备工作（按操作系统）](#1-准备工作按操作系统)
- [2. 获取代码](#2-获取代码)
- [3. 配置环境变量](#3-配置环境变量)
- [4. 一键启动](#4-一键启动)
- [5. 验证启动成功](#5-验证启动成功)
- [6. 训练预测模型](#6-训练预测模型)
- [7. 访问系统](#7-访问系统)
- [8. 如何查看各组件运行状态](#8-如何查看各组件运行状态)
- [9. 常见问题排查](#9-常见问题排查)
- [10. 停止与重启](#10-停止与重启)

---

## 1. 准备工作（按操作系统）

### 1.1 Windows

**Docker Desktop 安装：**

| Windows 版本 | 推荐方式 |
|-------------|---------|
| **Windows 10/11 专业版/企业版** | [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) |
| **Windows 10/11 家庭版** | 同上，安装时勾选 "Use WSL 2 instead of Hyper-V" |

> **注意：** Windows 7 或更早版本不支持最新 Docker Desktop。请使用带 Docker 的 Linux 服务器。

安装步骤：

1. 打开 [Docker Desktop 下载页](https://docs.docker.com/desktop/install/windows-install/)
2. 下载 `Docker Desktop Installer.exe`，双击运行
3. 安装完成后重启电脑
4. 打开 **PowerShell** 或 **命令提示符**，输入：
   ```powershell
   docker --version
   ```

**Git 安装：** [Git for Windows](https://git-scm.com/download/win)

### 1.2 Mac

**Docker Desktop 安装：**

| Mac 芯片 | 下载链接 |
|---------|---------|
| **Apple Silicon（M1/M2/M3/M4）** | [Docker Desktop for Mac (Apple Chip)](https://docs.docker.com/desktop/install/mac-install/) |
| **Intel 芯片** | [Docker Desktop for Mac (Intel Chip)](https://docs.docker.com/desktop/install/mac-install/) |

安装步骤：

1. 下载对应 `.dmg` 文件，双击安装
2. 打开 **终端**，输入：
   ```bash
   docker --version
   ```

### 1.3 Linux

**Docker Engine 安装：**

```bash
# Ubuntu / Debian
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# 退出重新登录使权限生效

# CentOS / RHEL / Fedora
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# 退出重新登录

# 验证
docker --version
```

验证：

```bash
docker run hello-world
```

---

## 2. 获取代码

```bash
git clone https://github.com/hfutwz/tongji-hospital-docker.git
cd tongji-hospital-docker
```

> 或从 GitHub 下载 ZIP：https://github.com/hfutwz/tongji-hospital-docker → Code → Download ZIP → 解压

---

## 3. 配置环境变量

```bash
# Windows
copy .env.example .env
# Mac / Linux
cp .env.example .env
```

编辑 `.env`：

```ini
# MySQL root 密码（改成你自己的密码）
MYSQL_ROOT_PASSWORD=your_secure_password_here

# 腾讯地图 API Key（用于地理编码和地图渲染）
# 申请地址：https://lbs.qq.com/
TENCENT_MAP_KEY=your_tencent_map_key_here
```

> 腾讯地图 Key 暂缺时填 `placeholder`，系统仍可启动，仅地图功能不可用。申请：https://lbs.qq.com/ → 注册 → 创建应用 → WebService 类型 Key。

---

## 4. 一键启动

```bash
# 所有系统通用（在 tongji-hospital-docker 目录下执行）
docker compose up -d
```

首次启动约 3-8 分钟（拉取镜像 + 编译前端 + 编译后端 + 自动导入数据库）。

启动完成时输出：

```
[+] Running 6/6
 ✔ Container trauma-mysql     Healthy
 ✔ Container trauma-redis     Healthy
 ✔ Container trauma-rabbitmq  Healthy
 ✔ Container trauma-predict   Started
 ✔ Container trauma-backend   Started
 ✔ Container trauma-frontend  Started
```

查看日志：`docker compose logs -f`（Ctrl+C 退出）。

`docker compose ps` 正常输出：

```
NAME               STATUS                      PORTS
trauma-mysql       Up (healthy)               0.0.0.0:3306->3306/tcp
trauma-redis       Up (healthy)               0.0.0.0:6379->6379/tcp
trauma-rabbitmq    Up (healthy)               0.0.0.0:5672->5672/tcp, 0.0.0.0:15672->15672/tcp
trauma-predict     Up                         0.0.0.0:8000->8000/tcp
trauma-backend     Up                         0.0.0.0:9090->9090/tcp
trauma-frontend    Up                         0.0.0.0:80->80/tcp
```

---

## 5. 验证启动成功

### 5.1 验证前端

```bash
curl http://localhost/
```
浏览器打开 http://localhost/，看到登录页面即成功。

### 5.2 验证后端

```bash
curl http://localhost:9090/api/patient/list
```
返回 JSON 患者列表数据即正常。

### 5.3 验证预测服务

```bash
curl http://localhost:8000/
# 预期返回 {"service":"trauma-prediction","docs":"/docs"}
```

### 5.4 验证数据库

```bash
docker compose exec mysql mysql -u root -p -e "SHOW TABLES;" healthineersvisualization
# 输入密码，应看到 9 张表

docker compose exec mysql mysql -u root -p -e \
  "SELECT COUNT(*) FROM patient;" healthineersvisualization
# 输出：2151
```

---

## 6. 训练预测模型

数据导入后，首次训练预测模型：

```bash
curl -X POST http://localhost:8000/api/model/train
```

预期返回 `"status":"success"`，`top1_accuracy` 约 0.42（5 分类，随机基线 0.20）。

查看模型状态：`curl http://localhost:8000/api/model/status`

---

## 7. 访问系统

| 访问内容 | 地址 |
|---------|------|
| 系统首页 | http://localhost（账号 admin / hos123） |
| 预测 API 文档 | http://localhost:8000/docs |
| RabbitMQ 管理后台 | http://localhost:15672（guest / guest） |

### 登录后可以访问的页面

| 页面 | 路径 | 功能 |
|------|------|------|
| 患者管理 | `/patient-list` | 2151 条患者记录的分页管理（筛选/编辑/删除/详情） |
| 地图热力图 | `/map` | 腾讯地图实时热力图（按季节/时段/年份筛选） |
| 月度地图动画 | `/monthly-heatmap` | 逐月播放热力图变化 |
| 大屏可视化看板 | `/bigscreen` | 8 个统计图表（ISS/GCS/RTS/伤因/旭日图/热力矩阵/身体热力图） |
| 患者统计 | `/hourly` | 24 小时时段分布统计 |
| 伤因预测 | `/prediction` | 4 个预测卡片（时空-伤因概率预测） |

---

## 8. 如何查看各组件运行状态

### 8.1 Docker Desktop（Windows / Mac）

打开 Docker Desktop → Containers → `tongji-hospital-docker`，展开可看到 6 个容器。点击容器名可查看 Logs / Stats / Files / Terminal。

### 8.2 命令行（所有系统通用）

**前端：** `docker compose logs frontend`

**后端：** `docker compose logs -f backend`（SQL 查询、API 调用、异常堆栈）

**预测服务：** `docker compose logs predict`（模型加载、API 请求、训练进度）

**数据库：** `docker compose logs mysql`

**模型文件（训练产出）：** `ls prediction/models/`（current.pkl + current.meta.json + 历史版本）

### 8.3 各组件功能呈现对照表

| 组件 | 功能呈现形式 | Docker Desktop 查看 | 命令行查看 |
|------|-------------|-------------------|-----------|
| **前端** | 浏览器页面（http://localhost） | Containers → Logs | `docker compose logs frontend` |
| **后端** | API 接口 + 终端日志 | Containers → Logs | `docker compose logs backend` |
| **数据库** | MySQL 表数据 | Containers → Terminal → `mysql` | `docker compose exec mysql mysql ...` |
| **预测服务** | 训练产出文件 + API 响应 | Containers → Files → `/app/models/` | `ls prediction/models/` |
| **Redis** | 缓存数据（无显式界面） | Containers → Terminal → `redis-cli` | `docker compose exec redis redis-cli` |
| **RabbitMQ** | 管理后台（http://localhost:15672） | 浏览器访问 | 浏览器访问 |

---

## 9. 常见问题排查

### 9.1 端口被占用（`port is already allocated`）

```bash
# Windows
netstat -ano | findstr ":80"
# Mac / Linux
lsof -i :80
```
关闭占用程序，或修改 `docker-compose.yml` 端口映射（如 `80:80` → `8080:80`）。

### 9.2 内存不足（卡住或 `exit code 137`）

Docker Desktop → Settings → Resources → Memory → 至少 4GB，重启 Docker。

### 9.3 后端反复重启

```bash
docker compose logs backend --tail 50
```
常见原因：MySQL 未就绪（等待 1-2 分钟）、`.env` 密码错误。

### 9.4 预测模型训练失败

```bash
docker compose logs predict --tail 30
```
等待 MySQL 状态变为 `healthy` 后再执行训练。

### 9.5 Windows 换行符（`/bin/sh^M`）

```powershell
(Get-Content .env.example) -replace "`r`n", "`n" | Set-Content -NoNewline .env
```

---

## 10. 停止与重启

```bash
docker compose stop          # 停止，保留数据
docker compose start         # 重新启动
docker compose up -d --build # 强制重建
docker compose down -v       # ⚠️ 删除所有数据（数据库+模型）
```

---

