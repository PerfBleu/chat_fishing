#  FetchData, UploadData, conn, fetch, upload
from dataclasses import dataclass
import sqlalchemy
import datetime
from ..config import sqlitestring

import contextlib
from uuid import uuid4
from typing import Callable
from asyncio import current_task
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    DateTime,
    String,
    VARCHAR,
    TEXT,
    text
)
import atexit

engine = create_engine(sqlitestring, pool_recycle=1500)
#async_session = sessionmaker(async_engine, class_=AsyncSession)
conn = engine.connect()

def destory():
    conn.close()

atexit.register(destory)

Base = declarative_base()

# class Fish_Data(Base):
#     __tablename__ = 'fish_data'
#     uid = Column(VARCHAR(20))
#     passwd = Column(TEXT)
#     state = Column(TEXT)
#     disp_name = Column(Integer)
#     status = Column(VARCHAR(50))


class FetchData:
    def __init__(self, uid, passwd="12345", namespace="钓鱼") -> None:
        self.用户名 = uid
        self.密码 = passwd
        self.disp_name = namespace

class UploadData:
    def __init__(self, uid, passwd, state, disp_name) -> None:
        self.用户名 = uid
        self.密码 = passwd
        self.钓鱼 = state
        self.disp_name = disp_name

async def fetch(data: FetchData):
    row = conn.execute(
        text("SELECT 钓鱼 FROM 用户数据 WHERE 用户名=:uid AND 密码=:pw;"),
        {"uid":data.用户名, "pw":data.密码}).fetchone()
    return {"userdata": row["钓鱼"]}

def upload(obj: UploadData):
    conn.execute(
        "REPLACE INTO 用户数据 (用户名, 密码, 钓鱼) VALUES (?,?,?)",
        obj.用户名, obj.密码, obj.钓鱼
    )