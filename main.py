from fastapi import FastAPI, HTTPException, Request, Response
import sqlite3
import logging
import json
import uuid
import time
import os

# Prometheus imports
from prometheus_client import Counter, Histogram, generate_latest

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# Setup OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "observability-ecommerce-app"})))
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAEGER_HOST", "localhost"),
    agent_port=int(os.getenv("JAEGER_PORT", 6831)),
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'])
response_latency = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds', ['method', 'endpoint'])
error_count = Counter('http_errors_total', 'Total HTTP errors', ['method', 'endpoint', 'status_code'])

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument SQLite3
SQLite3Instrumentor().instrument()

# Middleware for structured JSON logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Add request_id to request state for potential use in endpoints
    request.state.request_id = request_id
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Record Prometheus metrics
    endpoint = request.url.path
    request_count.labels(method=request.method, endpoint=endpoint, status_code=response.status_code).inc()
    response_latency.labels(method=request.method, endpoint=endpoint).observe(process_time)
    if response.status_code >= 400:
        error_count.labels(method=request.method, endpoint=endpoint, status_code=response.status_code).inc()
    
    log_data = {
        "request_id": request_id,
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "response_time": f"{process_time:.4f}s"
    }
    
    logger.info(json.dumps(log_data))
    
    return response

# Database connection helper
def get_db():
    conn = sqlite3.connect('ecommerce.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/products")
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return [dict(row) for row in products]

@app.post("/checkout")
def checkout(order: dict):
    product_id = order.get("product_id")
    quantity = order.get("quantity")
    
    if not product_id or not quantity:
        raise HTTPException(status_code=400, detail="product_id and quantity are required")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    
    price = product[0]
    total = price * quantity
    
    cursor.execute("INSERT INTO orders (product_id, quantity, total) VALUES (?, ?, ?)", (product_id, quantity, total))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    
    return {"order_id": order_id, "total": total}

@app.get("/orders")
def get_orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return [dict(row) for row in orders]

@app.get("/error")
def simulate_error():
    raise HTTPException(status_code=500, detail="Simulated application error")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
