# Full Stack Developer Capstone Project

📋 Project Overview
* This capstone project is a full-stack, cloud-native web application for managing dealerships and customer reviews. The platform integrates multiple microservices, containerization, and cloud deployment to deliver a scalable SaaS solution.

🏗️ Architecture Overview
* The system follows a microservices architecture with the following components:

## Frontend & Main Service
* Technology: Django web application
* Database: SQLite (for Car Make/Model data)

### Key Endpoints:
* ```get_cars/``` – Retrieve car listings
* ```get_dealers/``` – List all dealerships
* ```get_dealers/static``` – Filter dealerships by state
* ```dealer/:id``` – Get dealership details by ID
* ```review/dealer/:id``` – Get reviews for a specific dealer
* ```add_review/``` – Submit a new review

## Backend Microservice
* Technology: Node.js (Express) with MongoDB
* Containerization: Docker

### Key Endpoints:
* ```GET /fetchDealers``` – Fetch all dealerships
* ```GET /fetchDealer/:id``` – Fetch dealer by ID
* ```GET /fetchReviews``` – Fetch all reviews
* ```GET /fetchReview/dealer/:id``` – Fetch reviews for a dealer
* ```POST /insertReview``` – Insert a new review

## Sentiment Analysis Service
* Deployment: IBM Cloud Code Engine
* Function: Analyzes review sentiment (positive/negative/neutral)
* Endpoint: ```GET /analyze/:text```

## Integration & Proxy Layer
* Django Proxy Service: Mediates communication between Django frontend and backend microservices
* Orchestration: Kubernetes for deployment and scaling

🛠️ Project Implementation Steps
### Phase 1: Setup & Foundation
* Fork and clone the GitHub repository
* Set up the Django project template in Cloud IDE
* Implement static pages for initial user stories
* Run the application locally for validation

### Phase 2: User Management
* Integrate Django authentication system
* Develop React-based frontend for user management

### Phase 3: Backend Services Development
* Build Express.js server with MongoDB for dealership/review management
* Dockerize the Node.js microservice
* Deploy sentiment analyzer on IBM Cloud Code Engine
* Create Django models/views for Car Make/Model management
* Implement Django proxy services to integrate all microservices

### Phase 4: Dynamic Frontend Development
* Create dealer listing page with Django templates
* Develop dealer-specific review display page
* Implement review submission interface

### Phase 5: DevOps & Deployment
* Set up CI/CD pipeline for automated testing and deployment
* Test application locally and in Cloud IDE
* Deploy full application stack on Kubernetes
* Validate end-to-end functionality

🧠 Skills Applied & Demonstrated
* Cloud-Native Development
* Microservices architecture design and implementation
* Containerization with Docker
* Orchestration with Kubernetes
* Cloud deployment (IBM Cloud)

## Full-Stack Development
* Frontend: Django templates, React
* Backend: Python/Django, Node.js/Express
* Databases: SQLite, MongoDB (NoSQL)
* API design and integration
* DevOps & CI/CD
* Continuous Integration/Continuous Deployment pipelines
* Container management and orchestration
* Cloud-native application deployment

## Software Engineering Practices
* Proxy service implementation
* Service-to-service communication
* Sentiment analysis integration
* Scalable SaaS solution delivery

✨ Key Features & Functions
## User-Facing Features
* Browse dealerships by state or specific ID
* View detailed dealership information
* Read customer reviews for each dealership
* Submit new reviews with automated sentiment analysis
* User authentication and management

## System Features
* Modular microservices architecture
* Independent scaling of components
* Containerized deployment
* Cloud-native resilience and scalability
* Integrated sentiment analysis for review moderation

