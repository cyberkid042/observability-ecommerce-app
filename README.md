# Observability Ecommerce App

This is a FastAPI-based e-commerce simulation instrumented with a full observability stack.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/cyberkid042/observability-ecommerce-app.git
   cd observability-ecommerce-app
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```
   uvicorn main:app --reload
   ```

4. Access the API:
   - GET / : Returns a welcome message

## Usage Examples

- Start the server as above.
- Open browser to http://127.0.0.1:8000/
- You should see: {"Hello": "World"}

## Screenshots

Screenshots of Prometheus/Jaeger dashboards will be added as the observability stack is implemented.
