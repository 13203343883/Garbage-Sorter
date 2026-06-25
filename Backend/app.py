from fastapi import FastAPI

# 创建 FastAPI 实例
app = FastAPI(title="垃圾分类识别系统", version="1.0.0")

# 写一个测试接口，用来确认服务是否启动成功
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "服务运行正常"}

