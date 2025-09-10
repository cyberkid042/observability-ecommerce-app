# Observability Ecommerce App

This is a FastAPI-based e-commerce simulation instrumented with a full observability stack.

## Setup Instructions

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/cyberkid042/observability-ecommerce-app.git
   cd observability-ecommerce-app
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the database setup:
   ```
   python database.py
   ```

4. Run the development server:
   ```
   uvicorn main:app --reload
   ```

5. Access the API:
   - GET / : Returns a welcome message
   - GET /products : List all products
   - POST /checkout : Create new order (JSON: {"product_id": int, "quantity": int})
   - GET /orders : List all orders
   - GET /error : Simulate application error
   - GET /metrics : Prometheus metrics endpoint

### Docker Compose

1. Build and run all services:
   ```
   docker-compose up --build
   ```

2. Access services:
   - FastAPI: http://localhost:8000
   - Prometheus: http://localhost:9090
   - Jaeger UI: http://localhost:16686

## Testing

Run unit tests:
```
pytest
```

## Observability Features

- **Structured JSON Logging**: Request ID and response time logging
- **OpenTelemetry Tracing**: Distributed tracing with Jaeger
- **Prometheus Metrics**: Request count, latency histogram, error rate
- **Docker Compose**: Pre-configured services for full observability stack

## API Endpoints

- `GET /` - Welcome message
- `GET /products` - List all products
- `POST /checkout` - Create order (body: {"product_id": int, "quantity": int})
- `GET /orders` - List all orders
- `GET /error` - Simulate error
- `GET /metrics` - Prometheus metrics

## Usage Examples

- Start the server and visit http://127.0.0.1:8000/
- Use tools like curl or Postman to test endpoints
- View traces in Jaeger UI
- Query metrics in Prometheus

## Screenshots

Screenshots of Prometheus/Jaeger dashboards will be added as the observability stack is implemented.
