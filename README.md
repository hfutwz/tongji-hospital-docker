# 创伤地图和伤情预测系统

> 单仓库整合部署版 — 前端 + 后端 + 预测服务

基于 2151 条真实急救抢救室病历数据，提供创伤事件地图可视化、统计分析、伤因预测的完整 Web 系统。

---

## 仓库结构

```
tongji-hospital-docker/
├── frontend/              # 前端（Vue 2 + Element UI + ECharts + 腾讯地图）
├── backend/               # 后端（Spring Boot 2.3 + MyBatis-Plus + MySQL + Redis）
├── prediction/            # 预测服务（Python FastAPI + 条件概率统计模型）
├── db/                    # 数据库初始化 SQL
└── README.md
```

## 系统架构

```
Nginx (:80)
├── /          → 前端静态文件 (frontend/dist/)
└── /api/*     → 后端 (:9090)
                    ├── MySQL (:3306)
                    ├── Redis (:6379)
                    ├── RabbitMQ (:5672)
                    └── /api/prediction/* → 预测服务 (:8000)
```

## 快速开始（Docker）

```bash
# 1. 克隆仓库
git clone git@github.com:hfutwz/tongji-hospital-docker.git
cd tongji-hospital-docker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env：填写 MySQL 密码、腾讯地图 Key 等

# 3. 一键启动
docker compose up -d

# 4. 初始化数据库
docker compose exec mysql mysql -u root -p healthineersvisualization < db/init.sql

# 5. 触发预测模型全量训练
curl -X POST http://localhost:8000/api/model/train

# 6. 访问系统
# http://localhost
# 默认账号: admin / hos123
```

## 各模块独立运行

### 前端

```bash
cd frontend
npm install
npm run serve        # 开发模式，端口 8001
npm run build:prod   # 生产构建 → dist/
```

### 后端

```bash
cd backend
# 确保 MySQL + Redis + RabbitMQ 已启动
mvn spring-boot:run -Dspring-boot.run.profiles=dev
# 端口 9090
```

### 预测服务

```bash
cd prediction
pip install -r requirements.txt
cp .env.example .env  # 编辑数据库连接
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 技术栈

| 层次 | 技术 | 端口 |
|------|------|------|
| 前端 | Vue 2.6 + Element UI + ECharts 5 + Three.js | 80 (Nginx) |
| 后端 | Spring Boot 2.3 + MyBatis-Plus 3.4 + Redis + RabbitMQ | 9090 |
| 预测 | Python FastAPI + joblib + SQLAlchemy | 8000 |
| 数据 | MySQL 8.0 | 3306 |

## 数据库

初始化 SQL 位于 `db/` 目录，包含 9 张业务表及 2151 条患者数据：

- `patient` — 患者基础信息
- `injuryrecord` — 病例发生记录（含时空坐标、伤因）
- `interventiontime` / `intervention_extra` — 干预时间
- `gcs_score` / `rts_score` / `iss_patient_injury_severity` — 创伤评分
- `patient_info_on_admission` / `patient_info_off_admission` — 入/离室信息

## 页面功能

| 路径 | 功能 |
|------|------|
| `/login` | 登录（admin / hos123） |
| `/patient-list` | 患者管理（分页/筛选/详情弹窗） |
| `/map` | 地图热力图（腾讯地图） |
| `/monthly-heatmap` | 月度地图动画 |
| `/bigscreen` | 大屏可视化看板（8 个图表） |
| `/hourly` | 患者数量时段统计 |
| `/prediction` | 伤因预测（4 个预测卡片） |

## 原仓库

| 模块 | 原独立仓库 |
|------|-----------|
| 前端 | [tongji-hospital-front](https://github.com/hfutwz/tongji-hospital-front) |
| 后端 | [tongji-hospital-back](https://github.com/hfutwz/tongji-hospital-back) |
| 预测 | [Healthineers-visualization-predict](https://github.com/hfutwz/Healthineers-visualization-predict) |