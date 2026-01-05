from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Identify the service
resource = Resource.create({
    "service.name": "insurance-backend",
    "service.domain": "insurance",
    "deployment.environment": "local-docker"
})

# --- TRACING ---
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
)

# --- METRICS ---
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Define a counter
login_counter = meter.create_counter(
    "login_requests_total",
    description="Total number of login requests",
)

# --- LOGGING ---
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint="http://otel-collector:4318/v1/logs"))
)
LoggingInstrumentor().instrument(set_logging_packages=True)

# Attach OTel handler to root logger
logging.basicConfig(level=logging.INFO)
root_logger = logging.getLogger()
root_logger.addHandler(LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider))

app = FastAPI(title="Insurance Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes, allow all. In prod, specify the frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
def root():
    return {"service": "insurance-backend", "status": "running"}

@app.get("/login")
@app.post("/login")
def login():
    login_counter.add(1, {"method": "login"})
    logging.info("User login attempt detected")
    with tracer.start_as_current_span("CUJ-Login"):
        return {"message": "login successful"}

@app.get("/policy/{policy_id}")
def view_policy(policy_id: str):
    logging.info(f"Viewing policy {policy_id}")
    with tracer.start_as_current_span("CUJ-View-Policy"):
        return {"policy_id": policy_id, "status": "ACTIVE"}

@app.post("/claim")
def file_claim():
    logging.warning("New claim filed!")
    with tracer.start_as_current_span("CUJ-File-Claim"):
        return {"claim_id": "CLM-101", "status": "SUBMITTED"}

@app.post("/payment")
def payment():
    with tracer.start_as_current_span("CUJ-Premium-Payment"):
        return {"payment": "SUCCESS"}
