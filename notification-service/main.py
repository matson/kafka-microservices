from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer
import asyncio
import asyncpg
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []
db_pool = None

async def get_db_pool():
    return await asyncpg.create_pool(
        host="postgres",
        port=5432,
        database="orders",
        user="sushi",
        password="sushi123"
    )

async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                items JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

@app.on_event("startup")
async def startup_event():
    global db_pool
    db_pool = await get_db_pool()
    await init_db(db_pool)
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

            async with db_pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO orders (items) VALUES ($1)",
                    json.dumps(order.get("items", order))
                )

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

@app.get("/orders/history")
async def get_history():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, items, created_at FROM orders ORDER BY created_at DESC LIMIT 50"
        )
    return [
        {
            "id": row["id"],
            "items": json.loads(row["items"]),
            "created_at": row["created_at"].isoformat()
        }
        for row in rows
    ]

@app.get("/health")
async def health():
    return {"status": "ok"}
