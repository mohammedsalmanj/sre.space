from fastapi import FastAPI

app = FastAPI(title="Insurance Backend")

@app.get("/")
def root():
    return {"service": "insurance-backend", "status": "running"}

@app.get("/login")
@app.post("/login")
def login():
    return {"message": "login successful"}

@app.get("/policy/{policy_id}")
def view_policy(policy_id: str):
    return {"policy_id": policy_id, "status": "ACTIVE"}

@app.post("/claim")
def file_claim():
    return {"claim_id": "CLM-101", "status": "SUBMITTED"}

@app.post("/payment")
def payment():
    return {"payment": "SUCCESS"}
