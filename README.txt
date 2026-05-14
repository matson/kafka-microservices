SUSHI Order Service

Overview:
A full-stack event-driven ordering system built to demonstrate microservices
architecture. Customers place sushi orders through a React frontend, which flow
through a Python order service into Kafka, then get consumed by a notification
service that persists orders to PostgreSQL and pushes real-time updates back to
the UI via WebSocket.

Architecture:

React Frontend → Order Service (FastAPI) → Kafka → Notification Service (FastAPI)
                                                            ↓                ↓
                                                       PostgreSQL      WebSocket
                                                      (persisted)      (live UI)

Tech Stack:
- React
- Python / FastAPI
- Apache Kafka
- PostgreSQL
- Kubernetes
- Docker
- Helm

How to run:
1. Install Docker Desktop and enable Kubernetes (Settings → Kubernetes)
2. Install Helm: brew install helm
3. Start a local registry: docker run -d -p 5001:5000 --name registry registry:2
4. Deploy Kafka: kubectl apply -f k8s/kafka.yaml
5. Deploy Postgres: kubectl apply -f k8s/postgres.yaml
6. Build and push services:
     docker build -t order-service:latest order-service/
     docker tag order-service:latest localhost:5001/order-service:latest
     docker push localhost:5001/order-service:latest
     docker build -t notification-service:latest notification-service/
     docker tag notification-service:latest localhost:5001/notification-service:latest
     docker push localhost:5001/notification-service:latest
7. Deploy services: kubectl apply -f k8s/order-service.yaml -f k8s/notification-service.yaml
8. Port-forward:
     kubectl port-forward deployment/order-service 8000:8000
     kubectl port-forward deployment/notification-service 8001:8000
9. Start frontend: cd frontend && npm start

Key concepts demonstrated:
- Event-driven microservices with Kafka as the message broker
- Decoupled services — adding a new consumer requires no changes to existing services
- Order persistence with PostgreSQL — history survives page refreshes and restarts
- Real-time UI updates via WebSocket
- Containerized services orchestrated with Kubernetes
