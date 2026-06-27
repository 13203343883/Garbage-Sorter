from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# 1. 创建数据库引擎（使用SQLite，文件名为 garbage.db）
SQLALCHEMY_DATABASE_URL = "sqlite:///./garbage.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite多线程访问需要
)

# 2. 创建会话类，用于操作数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 创建基类，所有模型都继承它
Base = declarative_base()


# 4. 定义三张表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True, nullable=False)  # 微信唯一标识
    created_at = Column(DateTime, default=datetime.utcnow)


class GarbageType(Base):
    __tablename__ = "garbage_types"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False)  # 如 "易拉罐"
    category = Column(String(20), nullable=False)  # 如 "可回收物"
    disposal_guide = Column(String(200))  # 如 "压扁后投入可回收垃圾桶"


class RecognitionRecord(Base):
    __tablename__ = "recognition_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 允许未登录用户
    image_url = Column(String(500))  # 图片存储路径或URL
    result_label = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 可选：关联用户对象（方便联表查询）
    user = relationship("User")


# 5. 创建所有表
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功！")


# 6. 预置垃圾类别数据
def init_garbage_types():
    """
    预置常见的垃圾类别，供模型识别结果映射使用。
    """
    session = SessionLocal()
    try:
        # 检查是否已经有数据
        if session.query(GarbageType).count() > 0:
            return

        default_types = [
            {"label": "易拉罐", "category": "可回收物", "disposal_guide": "压扁后投入可回收垃圾桶"},
            {"label": "塑料瓶", "category": "可回收物", "disposal_guide": "洗净后投入可回收垃圾桶"},
            {"label": "玻璃瓶", "category": "可回收物", "disposal_guide": "投入可回收垃圾桶，注意轻放"},
            {"label": "废纸", "category": "可回收物", "disposal_guide": "折叠整齐后投入可回收垃圾桶"},
            {"label": "苹果核", "category": "厨余垃圾", "disposal_guide": "投入厨余垃圾桶"},
            {"label": "香蕉皮", "category": "厨余垃圾", "disposal_guide": "投入厨余垃圾桶"},
            {"label": "茶叶渣", "category": "厨余垃圾", "disposal_guide": "投入厨余垃圾桶"},
            {"label": "废电池", "category": "有害垃圾", "disposal_guide": "投入有害垃圾桶，不可随意丢弃"},
            {"label": "过期药品", "category": "有害垃圾", "disposal_guide": "投入有害垃圾桶"},
            {"label": "塑料袋", "category": "其他垃圾", "disposal_guide": "投入其他垃圾桶"},
            {"label": "烟蒂", "category": "其他垃圾", "disposal_guide": "熄灭后投入其他垃圾桶"},
            {"label": "卫生纸", "category": "其他垃圾", "disposal_guide": "投入其他垃圾桶"},
        ]

        for item in default_types:
            garbage = GarbageType(**item)
            session.add(garbage)

        session.commit()
        print("✅ 预置垃圾类别数据插入成功！")
    except Exception as e:
        session.rollback()
        print(f"⚠️ 预置数据插入失败: {e}")
    finally:
        session.close()


# 7. 测试数据库连接和初始化
if __name__ == "__main__":
    print("正在初始化数据库...")
    create_tables()
    init_garbage_types()
    print("🎉 数据库初始化完成！")