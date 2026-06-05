"""
FastAPI 入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.prediction import router

app = FastAPI(
    title="创伤预测服务（时空因导算法）",
    description="基于上海同济医院急救数据的时空伤因分布预测 API",
    version="1.0.0",
)

# CORS（允许 Java 后端跨域调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def on_startup():
    """启动时自动加载模型并同步版本号"""
    from app.api.prediction import reload_model
    try:
        reload_model()
        print(f"[startup] 模型加载成功")
    except Exception as e:
        print(f"[startup] 模型加载失败（服务仍可启动，需手动训练）: {e}")


@app.get("/", include_in_schema=False)
def root():
    return {"service": "trauma-prediction", "docs": "/docs"}
