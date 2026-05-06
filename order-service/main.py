from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaProducer
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

producer = None

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers="kafka.kafka.svc.cluster.local:9092"
    )
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

@app.post("/orders")
async def create_order(order: dict):
    await producer.send_and_wait(
        "orders",
        json.dumps(order).encode("utf-8")
    )
    return {"status": "order received", "order": order}
