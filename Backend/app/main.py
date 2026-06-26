from fastapi import FastAPI
from database import create_tables, init_garbage_types 
import os
import shutil
import uuid
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

# 创建 FastAPI 实例
app = FastAPI(title="垃圾分类识别系统", version="1.0.0")

# 写一个测试接口，用来确认服务是否启动成功
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "服务运行正常"}



# 启动时自动建表和预置数据
create_tables()
init_garbage_types()



# 上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    # 1. 保存图片到本地
    file_extension = image.filename.split(".")[-1] if "." in image.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # 2. TODO: 替换为真实模型推理
    # 目前返回模拟数据
    result = {
        "label": "易拉罐",
        "category": "可回收物",
        "confidence": 0.95,
        "image_path": file_path
    }

    return JSONResponse(content={
        "code": 0,
        "data": result
    })