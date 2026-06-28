import os
import shutil
import uuid
import glob
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from database import create_tables, init_garbage_types
from model_service import get_model
# 创建 FastAPI 实例
app = FastAPI(title="垃圾分类识别系统", version="1.0.0")

# 上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 健康检查接口
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "服务运行正常"}

# 预测接口（真实模型推理）
@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    # 1. 保存图片到本地
    file_extension = image.filename.split(".")[-1] if "." in image.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    clean_uploads(100)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # 2. 加载模型并推理
    try:
        model = get_model()
        result = model.predict(file_path)
        
        # 添加图片路径到结果中
        result["image_path"] = file_path
        
        return JSONResponse(content={
            "code": 0,
            "data": result
        })
    except Exception as e:
        return JSONResponse(content={
            "code": -1,
            "message": f"推理失败: {str(e)}"
        }, status_code=500)
def clean_uploads(max_files=100):
    """保留最近 max_files 张图片，删除多余旧文件"""
    files = glob.glob(os.path.join(UPLOAD_DIR, "*.*"))
    if len(files) > max_files:
        # 按创建时间排序，删除最旧的
        files.sort(key=os.path.getctime)
        for f in files[:-max_files]:  # 保留最近 max_files 个
            os.remove(f)
# 启动时自动建表和预置数据
create_tables()
init_garbage_types()