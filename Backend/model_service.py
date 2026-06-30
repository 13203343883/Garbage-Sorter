import onnxruntime as ort
import cv2
import numpy as np
import os
import json

# 类别映射文件路径
RULE_FILE = "Model/garbage_classify_rule.json"

class YOLOClassifier:
    def __init__(self, model_path="Model/best.onnx"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")
        
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        
        input_shape = self.session.get_inputs()[0].shape
        self.input_size = (input_shape[2], input_shape[3])
        
        # 加载类别映射表
        self.class_names = []
        self.category_map = {}
        self._load_rule_file()
    
    def _load_rule_file(self):
        """加载 garbage_classify_rule.json 并构建映射"""
        if not os.path.exists(RULE_FILE):
            raise FileNotFoundError(f"规则文件不存在: {RULE_FILE}")
        
        with open(RULE_FILE, 'r', encoding='utf-8') as f:
            rule_data = json.load(f)
        
        # rule_data 格式: {"0": "其他垃圾/一次性快餐盒", ...}
        for idx, value in rule_data.items():
            category, label = value.split('/', 1)  # 按 '/' 拆成两段
            self.class_names.append(label)
            self.category_map[label] = category
    
    def preprocess(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.input_size)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict(self, image_path):
        input_tensor = self.preprocess(image_path)
        outputs = self.session.run([self.output_name], {self.input_name: input_tensor})
        
        output = outputs[0]
        
        # 根据输出形状解析
        if len(output.shape) == 2 and output.shape[0] == 1:
            scores = output[0]
            class_id = np.argmax(scores)
            confidence = np.max(scores)
        elif len(output.shape) == 1:
            class_id = np.argmax(output)
            confidence = np.max(output)
        else:
            # 处理 YOLO 检测格式
            class_id = np.argmax(output[0, 0, :])
            confidence = output[0, 0, class_id]
        
        label = self.class_names[class_id] if class_id < len(self.class_names) else "未知"
        category = self.category_map.get(label, "其他垃圾")
        
        return {
            "label": label,
            "category": category,
            "confidence": float(confidence),
            "class_id": int(class_id)
        }


_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = YOLOClassifier()
    return _model_instance


if __name__ == "__main__":
    model = get_model()
    print(f"模型加载成功！类别数量: {len(model.class_names)}")
    for i, label in enumerate(model.class_names[:5]):
        print(f"  {i}: {label}")