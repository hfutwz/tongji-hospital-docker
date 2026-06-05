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

### 你需要什么

- 一台能上网的电脑
- 至少 8GB 内存（推荐 16GB）
- 至少 20GB 可用磁盘空间
- 一个文本编辑器（记事本、VS Code、vim 都行）

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
3. 安装完成后**重启电脑**
4. 重启后 Docker Desktop 会自动启动（任务栏右下角出现鲸鱼图标 🐳）
5. 打开 **PowerShell** 或 **命令提示符**，输入：
   ```powershell
   docker --version
   ```
   看到版本号（如 `Docker version 24.x.x`）表示安装成功

**Git 安装（用 git clone 方式获取代码时需要）：**

下载 [Git for Windows](https://git-scm.com/download/win)，安装时一路默认即可。

### 1.2 Mac

**Docker Desktop 安装：**

| Mac 芯片 | 下载链接 |
|---------|---------|
| **Apple Silicon（M1/M2/M3/M4）** | [Docker Desktop for Mac (Apple Chip)](https://docs.docker.com/desktop/install/mac-install/) |
| **Intel 芯片** | [Docker Desktop for Mac (Intel Chip)](https://docs.docker.com/desktop/install/mac-install/) |

安装步骤：

1. 下载对应 `.dmg` 文件，双击打开
2. 将 Docker 图标拖入 Applications 文件夹
3. 从启动台打开 Docker Desktop
4. 菜单栏出现鲸鱼图标 🐳
5. 打开 **终端**，输入：
   ```bash
   docker --version
   ```
   看到版本号表示安装成功

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

> **不需要** Docker Desktop。Linux 直接用 Docker Engine + `docker compose` 插件。

### 验证 Docker 可用

在终端（PowerShell / 终端）中执行：

```bash
docker run hello-world
```

看到 `Hello from Docker!` 就说明 Docker 可以正常工作了。

---

## 2. 获取代码

**方式一：git clone（推荐，可随时更新）**

```bash
# 所有系统通用
git clone https://github.com/hfutwz/tongji-hospital-docker.git
cd tongji-hospital-docker
```

**方式二：下载 ZIP 压缩包**

1. 浏览器打开 https://github.com/hfutwz/tongji-hospital-docker
2. 点击绿色 **Code** 按钮 → **Download ZIP**
3. 解压到任意目录（比如 `D:\tongji-hospital-docker` 或 `~/Desktop/tongji-hospital-docker`）
4. 打开终端进入该目录

---

## 3. 配置环境变量

### 3.1 创建 .env 文件

```bash
# Windows (PowerShell)
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

### 3.2 编辑 .env 文件

用文本编辑器打开 `.env` 文件，修改以下内容：

```ini
# MySQL root 密码（改成你自己的密码）
MYSQL_ROOT_PASSWORD=your_secure_password_here

# 腾讯地图 API Key（用于地理编码和地图渲染）
# 申请地址：https://lbs.qq.com/
TENCENT_MAP_KEY=your_tencent_map_key_here
```

> **关于腾讯地图 Key：** 如果暂时没有，可以先留空或填 `placeholder`。系统仍可正常启动，但地图热力图和地理编码功能将不可用。申请地址：https://lbs.qq.com/ → 注册 → 创建应用 → 获取 Key（WebService 类型）。

---

## 4. 一键启动

```bash
# 所有系统通用（在 tongji-hospital-docker 目录下执行）
docker compose up -d
```

**首次启动**需要做以下事情，约 3-8 分钟（取决于网络速度）：

1. 拉取基础镜像：MySQL 8.0、Redis 7、RabbitMQ 3、Node 18、Maven 3、OpenJDK 8、Python 3.11（约 800MB）
2. 编译前端 (`npm install` + `npm run build:prod`)
3. 编译后端 (`mvn package`)
4. 构建预测服务镜像
5. 启动 6 个容器
6. 自动导入数据库（9 张表 + 2151 条数据）

**如果看到类似这样的输出，说明正在启动：**

```
[+] Running 6/6
 ✔ Container trauma-mysql     Healthy
 ✔ Container trauma-redis     Healthy
 ✔ Container trauma-rabbitmq  Healthy
 ✔ Container trauma-predict   Started
 ✔ Container trauma-backend   Started
 ✔ Container trauma-frontend  Started
```

### 查看启动进度

```bash
# 实时查看日志
docker compose logs -f

# 按 Ctrl+C 停止查看日志（不会停止容器）
```

### 查看各容器状态

```bash
docker compose ps
```

输出示例：

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

### 5.1 验证前端（Nginx）

```bash
# 所有系统通用
curl http://localhost/

# 或在浏览器打开
# http://localhost/
```

如果看到登录页面，前端部署成功 ✅

### 5.2 验证后端（Spring Boot）

```bash
# 所有系统通用
curl http://localhost:9090/api/patient/list

# 预期返回 JSON 格式的患者列表数据
```

### 5.3 验证预测服务（FastAPI）

```bash
# 所有系统通用
curl http://localhost:8000/

# 预期返回
# {"service":"trauma-prediction","docs":"/docs"}
```

### 5.4 验证数据库（MySQL）

```bash
docker compose exec mysql mysql -u root -p -e "SHOW TABLES;" healthineersvisualization
# 输入 .env 中设置的密码

# 预期看到 9 张表：
# gcs_score
# injuryrecord
# intervention_extra
# interventiontime
# iss_patient_injury_severity
# patient
# patient_info_off_admission
# patient_info_on_admission
# rts_score
```

### 5.5 验证数据库数据量

```bash
docker compose exec mysql mysql -u root -p -e \
  "SELECT COUNT(*) AS total_patients FROM patient;" healthineersvisualization
# 输入密码

# 预期输出：total_patients: 2151
```

---

## 6. 训练预测模型

数据导入后，预测模型需要首次训练：

```bash
# 所有系统通用
curl -X POST http://localhost:8000/api/model/train
```

**预期返回：**

```json
{
  "status": "success",
  "version": "v1_20260605_2030",
  "trained_count": 2131,
  "metrics": {
    "top1_accuracy": 0.4215,
    "sample_count": 427,
    "train_count": 1704,
    "test_count": 427
  }
}
```

> **说明：** `top1_accuracy: 0.4215` 表示 Top-1 准确率 42.15%（5 分类，随机基线 20%，模型约为随机基线的 2.1 倍）。训练完成后模型文件保存在 `prediction/models/` 目录下。

### 查看模型状态

```bash
curl http://localhost:8000/api/model/status
```

---

## 7. 访问系统

| 访问内容 | 地址 | 说明 |
|---------|------|------|
| **系统首页** | http://localhost | 自动跳转到登录页 |
| **登录账号** | admin / hos123 | 管理员账号 |
| **预测 API 文档** | http://localhost:8000/docs | Swagger 交互式文档 |
| **RabbitMQ 管理后台** | http://localhost:15672 | 账号 guest / guest |

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

### 8.1 通过 Docker Desktop（Windows / Mac）

Docker Desktop 提供图形化界面，适合不熟悉命令行的用户：

| 查看内容 | 操作方式 |
|---------|---------|
| **容器整体状态** | 打开 Docker Desktop → 左侧 "Containers" → 展开 `tongji-hospital-docker` |
| **容器 CPU/内存占用** | 点击容器名称 → "Stats" 标签页 |
| **容器日志** | 点击容器名称 → "Logs" 标签页 |
| **容器内文件** | 点击容器名称 → "Files" 标签页 |
| **进入容器终端** | 点击容器名称 → "Terminal" 标签页 |

**具体操作示例：**

1. 打开 Docker Desktop
2. 左侧菜单点击 **Containers**
3. 找到 `tongji-hospital-docker`，展开
4. 看到 6 个容器（trauma-mysql、trauma-redis、trauma-rabbitmq、trauma-predict、trauma-backend、trauma-frontend）
5. 绿色圆点 = 运行正常 ✅，红色 = 异常 ❌

### 8.2 通过命令行（Linux / 所有系统通用）

#### 查看前端（Nginx）日志

```bash
docker compose logs frontend
# 实时跟踪
docker compose logs -f frontend
```

> 前端 Nginx 日志主要显示 HTTP 请求记录（访问日志），不显示应用代码日志。

#### 查看后端（Spring Boot）日志

```bash
docker compose logs backend
# 近 100 行
docker compose logs --tail 100 backend
# 实时跟踪（推荐）
docker compose logs -f backend
```

> 后端日志显示：SQL 查询、API 调用、异常堆栈等信息。通过日志可以排查 API 报错。

#### 查看预测服务（FastAPI）日志

```bash
docker compose logs predict
# 实时跟踪
docker compose logs -f predict
```

> 预测服务日志显示：模型加载状态、API 请求、训练进度等。

#### 查看数据库（MySQL）日志

```bash
docker compose logs mysql
# 近 50 行
docker compose logs --tail 50 mysql
```

> MySQL 日志显示：连接情况、慢查询等。正常情况下日志较少。

#### 查看模型文件（训练产出）

模型训练后，在宿主机上查看：

```bash
# Windows (PowerShell) / Mac / Linux 通用
ls prediction/models/

# 看到类似文件：
# current.pkl               ← 当前模型（二进制）
# current.meta.json         ← 当前模型元数据
# v1_20260605_2030.pkl     ← 历史版本
# v1_20260605_2030.meta.json
```

> 模型文件通过 Docker volume (`predict-models`) 持久化，容器重建后不会丢失。

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

### 9.1 端口被占用

**现象：** 启动时报错 `port is already allocated`

**解决：**

```bash
# 查看谁占用了端口
# Windows
netstat -ano | findstr ":80"
netstat -ano | findstr ":3306"

# Mac / Linux
lsof -i :80
lsof -i :3306

# 解决方法：
# 1. 关闭占用端口的程序（如已安装的 MySQL、Nginx、Apache）
# 2. 或修改 docker-compose.yml 中的端口映射（如 80→8080）
```

### 9.2 内存不足

**现象：** 编译或启动时卡住不动，或报 `exit code 137`

**解决：**

- 关闭其他大型应用（浏览器、IDE 等）
- Docker Desktop 设置中增加内存限制：Settings → Resources → Memory → 至少 4GB
- 如果电脑内存 < 8GB，建议使用云服务器部署

### 9.3 前端构建失败（Node.js 内存溢出）

**现象：** 前端构建时 `JavaScript heap out of memory`

**解决：**

- Docker Desktop 设置 → Resources → Memory → 增加到 6GB
- 重启 Docker Desktop

### 9.4 后端启动后自动退出

**现象：** `docker compose ps` 显示 backend 状态为 `Restarting` 或 `Exited`

**排查：**

```bash
# 查看后端日志
docker compose logs backend --tail 50
```

常见原因：
- MySQL 未就绪 → 等待 1-2 分钟后后端会自动重连
- 数据库连接密码错误 → 检查 `.env` 中的 `MYSQL_ROOT_PASSWORD`
- 腾讯地图 Key 缺失 → 不影响启动，仅地图功能不可用

### 9.5 预测模型训练失败

**现象：** `curl -X POST http://localhost:8000/api/model/train` 返回错误

**排查：**

```bash
# 查看预测服务日志
docker compose logs predict --tail 30

# 检查数据库连接
docker compose exec predict python -c "
from app.config import DB_HOST
print(f'DB_HOST: {DB_HOST}')
"
```

常见原因：
- 数据库未完全初始化 → 等待 MySQL 容器状态变为 `healthy` 后再训练
- 网络问题 → 确保 `docker compose up -d` 全部完成

### 9.6 Windows 下换行符问题

**现象：** 启动报错 `/bin/sh^M: bad interpreter`

**解决：**

```bash
# 在 PowerShell 中执行
# 将 .env.example 转为 Unix 换行符后保存为 .env
(Get-Content .env.example) -replace "`r`n", "`n" | Set-Content -NoNewline .env
```

### 9.7 Mac Apple Silicon 兼容性

M1/M2/M3/M4 芯片的 Mac 可能遇到 MySQL 镜像兼容问题：

**现象：** MySQL 容器无法启动，提示 `platform` 错误

**解决：** Docker Desktop 会自动处理多架构镜像，无需额外配置。如果遇到问题，确保 Docker Desktop 版本 ≥ 4.15。

---

## 10. 停止与重启

### 停止所有容器

```bash
docker compose down
```

### 停止但保留数据

```bash
docker compose stop
```

### 重新启动

```bash
docker compose start
# 或强制重建
docker compose up -d --build
```

### 完全清除（删除所有数据）

```bash
docker compose down -v
# ⚠️ 这会删除数据库数据和模型文件！
# 下次启动会自动从 SQL 重新初始化数据库
```

---

## 部署完成清单

- [ ] Docker 已安装并正常运行
- [ ] 代码已克隆/解压到本地
- [ ] `.env` 文件已配置
- [ ] `docker compose up -d` 执行成功，6 个容器全部 UP
- [ ] 浏览器打开 http://localhost 看到登录页
- [ ] 使用 admin / hos123 登录成功
- [ ] 预测模型训练完成（`curl -X POST http://localhost:8000/api/model/train`）
- [ ] 大屏可视化看板正常显示图表
- [ ] 地图热力图正常加载
- [ ] 伤因预测页面正常显示预测结果

---

*如有部署问题，请查看各容器日志：`docker compose logs <容器名>`*