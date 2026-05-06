
SUSHI Order Service 

Overview: 
A full-stack event-driven ordering system built to demonstrate     
microservices architecture. Customers place sushi orders through a React
frontend, which flow through a Python order service into Kafka, then get      
consumed by a notification service and pushed back to the UI in real time via
WebSocket.

Architecture: 
a simple diagram in text:                                      
React Frontend → Order Service (FastAPI) → Kafka → Notification Service
(FastAPI)                                                                     
    ↓                 
WebSocket → Frontend

Tech Stack — React, Python/FastAPI, Apache Kafka, Kubernetes, Docker, Helm

How to run:
The steps someone would need to reproduce it locally (Docker     
Desktop with Kubernetes enabled, Helm, the local registry, kubectl apply      
commands, port-forwards)                                                      
                  
Key concepts demonstrated:
- Event-driven microservices with Kafka as the message broker
- Decoupled services — adding a new consumer requires no changes to existing  
services                                                                    
- Real-time UI updates via WebSocket                                          
- Containerized services orchestrated with Kubernetes