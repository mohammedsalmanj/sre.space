from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Identify the service
resource = Resource.create({
    "service.name": "insurance-backend",
    "service.domain": "insurance",
    "deployment.environment": "local-docker"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Export traces to the collector collector container
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4318/v1/traces"
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

app = FastAPI(title="Insurance Backend")
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
def root():
    return {"service": "insurance-backend", "status": "running"}

@app.post("/login")
def login():
    with tracer.start_as_current_span("CUJ-Login"):
        return {"message": "login successful"}

@app.get("/policy/{policy_id}")
def view_policy(policy_id: str):
    with tracer.start_as_current_span("CUJ-View-Policy"):
        return {"policy_id": policy_id, "status": "ACTIVE"}

@app.post("/claim")
def file_claim():
    with tracer.start_as_current_span("CUJ-File-Claim"):
        return {"claim_id": "CLM-101", "status": "SUBMITTED"}

@app.post("/payment")
def payment():
    with tracer.start_as_current_span("CUJ-Premium-Payment"):
        return {"payment": "SUCCESS"}
