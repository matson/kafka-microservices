from fastapi import FastAPI                                                   
from aiokafka import AIOKafkaProducer
import asyncio                                                                
import json     
                                                                                
  app = FastAPI() 

  producer = None

  @app.on_event("startup")  
  # connecting to Kafka                                                     
  async def startup_event():
      global producer                                                           
      producer = AIOKafkaProducer(
          bootstrap_servers="kafka.kafka.svc.cluster.local:9092"
      )                                                                         
      await producer.start()
                                                                                
  @app.on_event("shutdown")
  # disconnects from Kafka 
  async def shutdown_event():
      await producer.stop()

  @app.post("/orders")
  # POST route - publishes it to Kafka                                                        
  async def create_order(order: dict):
      await producer.send_and_wait(                                             
          "orders",
          json.dumps(order).encode("utf-8")
      )                                                                         
      return {"status": "order received", "order": order}
                                                                                
  