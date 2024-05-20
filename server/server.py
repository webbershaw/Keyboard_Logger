import uuid
import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
import uvicorn

# 读取配置文件
def read_config():
    with open("server-config.yaml", "r") as file:
        return yaml.safe_load(file)

config = read_config()
db_config = config['database']

# 初始化FastAPI应用
app = FastAPI()

# 配置数据库连接
DATABASE_URL = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定义数据库模型
class Record(Base):
    __tablename__ = "keyboard"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    remote_time = Column(DateTime)
    device = Column(String(255))
    content = Column(Text)

# 创建表
Base.metadata.create_all(bind=engine)

# 定义请求体
class RecordCreate(BaseModel):
    time: str
    device: str
    content: str

# 定义接收POST请求的接口
@app.post("/records/")
async def create_record(record: RecordCreate):
    # 解析日期字符串
    try:
        local_time = datetime.datetime.strptime(record.time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # 创建数据库会话
    db = SessionLocal()
    db_record = Record(
        remote_time=local_time,
        device=record.device,
        content=record.content
    )
    try:
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error saving record to database")
    finally:
        db.close()

    return {
        "time": db_record.remote_time,
        "device": db_record.device,
        "content": db_record.content
    }

# 添加uvicorn启动命令
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
