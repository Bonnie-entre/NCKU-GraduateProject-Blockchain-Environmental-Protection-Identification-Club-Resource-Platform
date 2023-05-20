from fastapi import FastAPI,  Depends
from fastapi.middleware.cors import CORSMiddleware

from app.models import *
from app.schemas import *
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.routers.user import *
from app.routers.resource import *
from app.routers.activity import *
from app.routers.transaction import *
from app.routers.picture import *

from config import settings

from blockchain.src.EFT_functions import *
from web3 import Web3# Web3 provider
w3 = Web3(Web3.HTTPProvider(settings.SEPOLIA_RPC_URL)) # Insert your RPC URL here

import time

from js.d3 import d3
d3.need()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_user)
app.include_router(router_resource)
app.include_router(router_activity)
app.include_router(router_transaction)
app.include_router(router_picture)


@app.get("/")
async def root():
    return {"message": "easy start"}


@app.get("/initClub")
async def init_setClub(db: Session = Depends(get_db)):
    club_list = [
        {'name': '區塊鏈研究社', 'address': '0x934DD74D3471eB97B5D41d4EAf60a9657480d9AE'},
        {'name': '流行舞蹈研究社', 'address': '0xD9F56159dC7dC3894c238686549FC9C3a3F5810C'},
        {'name': '創聯會', 'address': '0x99CAd929431Dc98F6cFB9953C9AB55f84d267a02'},
        {'name': '管理顧問社', 'address': '0xF516B6a1D51b508Fc5EDb8e3c1E77Cb05056Dc44'},
        {'name': '天文社', 'address': '0x39481F9A9747a28db1038aE8C1f1DCd46439898e'}
    ]
    for i in club_list:
        add_user = Club(
            name = i["name"],
            address = i["address"],
            password = '0000',
            token = 0
        )
        
        db.add(add_user)
        db.commit()
        db.refresh(add_user)
        hash = CreateClub(add_user.id, i["name"], i["address"])
        time.sleep(20)
        txn_receipt = w3.eth.get_transaction_receipt(hash)        
        while(txn_receipt is None or txn_receipt['status']==0):
            time.sleep(10)
        print(i, hash)

    return {"message": "Initialize Successfully!"}



@app.get("/initResource")
async def init_setResource(db: Session = Depends(get_db)):
    resource_list=[
        {'name': '芸青軒_1F-A', 'cost':5},
        {'name': '芸青軒_1F-B', 'cost':5},
        {'name': '芸青軒_2F-第一討論室', 'cost':3},
        {'name': '芸青軒_2F-第二討論室', 'cost':3},
        {'name': '活動中心_3F-A', 'cost':10},
        {'name': '活動中心_3F-B', 'cost':10},
        {'name': '國際會議廳_第一演講室', 'cost':20},
        {'name': '國際會議廳_第二演講室', 'cost':20},
        {'name': '成功廳', 'cost':60},
        {'name': '成杏廳 ', 'cost':40},
        {'name': '未來講堂', 'cost':20},
    ]
    for i in resource_list:
        add_resource = Resource(
            name = i["name"],
            cost = i["cost"]
        )
        db.add(add_resource)
        db.commit()
        db.refresh(add_resource)
        
        hash = CreateResource(add_resource.id, i["name"], i["cost"])
        time.sleep(20)
        txn_receipt = w3.eth.get_transaction_receipt(hash)
        while(txn_receipt is None or txn_receipt['status']==0):
            time.sleep(10)
        print(i, hash)

    return {"message": "Initialize Successfully!"}


@app.get("/initActivity")
async def init_setActivity(db: Session = Depends(get_db)):
    activity_list = [
        {'name': '流舞成發', 'date':'2023-06-17 18:30:00', 'club_id':2},
        {'name': '期末專案發表', 'date':'2023-05-26 19:00:00', 'club_id':1},
        {'name': '第4次社課', 'date':'2023-06-08 18:30:00', 'club_id':1},
        {'name': '第5次社課', 'date':'2023-06-15 18:30:00', 'club_id':1},
        {'name': '創業經驗分享', 'date':'2023-06-09 19:00:00', 'club_id':3},
        {'name': '創業提案競賽', 'date':'2023-06-16 18:00:00', 'club_id':3},
        {'name': '管顧經驗圓桌分享', 'date':'2023-06-10 13:00:00', 'club_id':4},
        {'name': '管顧面試衝刺讀書會', 'date':'2023-06-17 13:00:00', 'club_id':4},
        {'name': '第3次社課', 'date':'2023-06-08 19:00:00', 'club_id':5},
        {'name': '第4次社課', 'date':'2023-06-15 19:00:00', 'club_id':5},
    ]

    for i in activity_list:
        add_activity = Activity(
            name = i["name"],
            date = i["date"],
            club_id = i["club_id"]          
        )
        db.add(add_activity)
        db.commit()

    return {"message": "Initialize Successfully!"}
