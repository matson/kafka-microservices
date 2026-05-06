from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())

async def consume():
    consumer = AIOKafkaConsumer(
        "orders",
        bootstrap_servers="kafka.kafka.svc.cluster.local:9092",
        group_id="notification-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            order = json.loads(message.value.decode("utf-8"))
            print(f"Received order: {order}", flush=True)
            for client in clients:
                await client.send_json(order)
    finally:
        await consumer.stop()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/health")
async def health():
    return {"status": "ok"}
