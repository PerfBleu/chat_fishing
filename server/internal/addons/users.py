#  FetchData, UploadData, conn, fetch, upload
from dataclasses import dataclass
import sqlalchemy
import datetime
import json
import os
from pathlib import Path
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

default = {
            "userdata": {
                    "游戏中": False,
                    "钓鱼力": 1.00,
                    "钓鱼次数": 0,
                    "空军次数": 0,
                    "钓到的鱼": [],
                    "我的鱼篓": [],
                    "钓鱼图鉴": {},
                    "开始游戏时间": None,
                    "第一次钓到鱼": "",
                    "第一次钓到的鱼": {},
                    "第一次空军时间": "",
                    "经过的消息数量": 0,
                    "累计的消息数量": 0,
                    "被鱼跑掉的次数": 0,
                    "被鱼跑掉的总次数": 0,
                    "最近的 10000 条日志": [],
                }
            }

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
    uid = data.用户名
    pw = data.密码
    row = conn.execute(
        text("SELECT 密码 FROM 用户数据 WHERE 用户名=:uid;"),
        {"uid":uid}).fetchone()
    user_profile_path = Path(os.path.dirname(__file__)).parent.parent / "profiles" / f"{uid}.json"
    # if pw == row[0]:
    if not os.path.exists(user_profile_path):
        with open(user_profile_path, "w", encoding='utf-8') as f:
            f.write(json.dumps(default, ensure_ascii=False))
            return default
    else:
        with open(user_profile_path, "r", encoding='utf-8') as f:
            return json.loads(f.read())

async def upload(data: UploadData, hot=True):
    uid = data.用户名
    pw = data.密码
    row = conn.execute(
        text("SELECT 密码 FROM 用户数据 WHERE 用户名=:uid;"),
        {"uid":uid}).fetchone()
    user_profile_path = Path(os.path.dirname(__file__)).parent.parent / "profiles" / f"{uid}.json"
    with open(user_profile_path, "w", encoding='utf-8') as f:
        f.write(json.dumps({"userdata":data.钓鱼}, ensure_ascii=False))


    # row = conn.execute(
    #     text("SELECT 钓鱼 FROM 用户数据 WHERE 用户名=:uid AND 密码=:pw;"),
    #     {"uid":data.用户名, "pw":data.密码}).fetchone()
    # default = {
    #             "userdata": json.dumps({
    #                     "游戏中": False,
    #                     "钓鱼力": 1.00,
    #                     "钓鱼次数": 0,
    #                     "空军次数": 0,
    #                     "钓到的鱼": [],
    #                     "我的鱼篓": [],
    #                     "钓鱼图鉴": {},
    #                     "开始游戏时间": None,
    #                     "第一次钓到鱼": "",
    #                     "第一次钓到的鱼": {},
    #                     "第一次空军时间": "",
    #                     "经过的消息数量": 0,
    #                     "累计的消息数量": 0,
    #                     "被鱼跑掉的次数": 0,
    #                     "被鱼跑掉的总次数": 0,
    #                     "最近的 10000 条日志": [],
    #                 }, ensure_ascii= False)
    #             }
    # default_txt = json.dumps(default["userdata"], ensure_ascii=False)

    # try:
    #     print(row)
    #     print("1")
    #     # return {"userdata": row[0][1:-1].replace('\\"', '"')}
    #     return {"userdata": row[0][1:-1]}
    # except IndexError:
    #     print("2")
    #     return default
    # # except TypeError:
    # #     print("3")
    # #     conn.execute(
    # #         text("REPLACE INTO 用户数据 (用户名, 密码, 钓鱼) VALUES (:uid,:pw,:fish_state)"),
    # #         {"uid":data.用户名, "pw":data.密码, "fish_state":default_txt}
    # #     )
    # #     conn.commit()
    #     return default

# async def upload(obj: UploadData, hot=True):
#     conn.execute(
#         text("REPLACE INTO 用户数据 (用户名, 密码, 钓鱼) VALUES (:uid,:pw,:fish_state)"),
#         {"uid":obj.用户名, "pw":obj.密码, "fish_state":obj.钓鱼}
#     )
#     conn.commit()