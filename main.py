from datetime import date, datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, select, create_engine, SQLModel, Field
from fastapi.middleware.cors import CORSMiddleware


class Visit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str
    visit_time: datetime = Field(default_factory=datetime.now)
    visit_date: date = Field(default_factory=date.today, index=True)

sqlite_url = f"sqlite:///../volume/dbs/database.db"
engine = create_engine(sqlite_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


def get_session():
    with Session(engine) as session:
        yield session

@app.get("/visit/{path}")
async def record_visit(
    path: str,
    session: Session = Depends(get_session)
):
    # 创建新访问记录
    visit = Visit(path=path)
    session.add(visit)
    session.commit()
    
    # 获取今日总访问次数
    today = date.today()
    total_visits = session.exec(
        select(Visit).where(Visit.visit_date == today)
    ).all()
    
    return {
        "path": path,
        "today_path_visits": sum(i.path == path for i in total_visits),
        "today_total_visits": len(total_visits),
    }


if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host='0.0.0.0', port=8000)