import requests

# 替换成你电脑上的一张图片路径
image_path = "C:/Users/31767/Pictures/R-C.jpg"

with open(image_path, "rb") as f:
    files = {"image": f}
    response = requests.post("http://127.0.0.1:8000/predict", files=files)

print(response.json())