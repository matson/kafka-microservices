from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import asyncio
import json

# listens to Kafka - processes orders 

app = FastAPI()

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
            print(f"Received order: {order}")
    finally:
        await consumer.stop()

@app.get("/health")
async def health():
    return {"status": "ok"}
