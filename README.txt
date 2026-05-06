
  - React frontend — order form that posts to a REST API                        
  - Order Service — Python/FastAPI microservice that publishes events to Kafka
  - Notification Service — Python/FastAPI microservice that consumes events from
   Kafka          
  - Kafka — message broker running in Kubernetes handling async communication   
  between services                                                              
  - Kubernetes — orchestrating all of it with deployments and services

 - The microservices are decoupled — order service doesn't know or care about  
  notification service                                                          
  - Kafka acts as the event bus — if you add a third service (billing,
  inventory), it just subscribes to the same topic                              
  - Everything is containerized and orchestrated with Kubernetes manifests written by myself
