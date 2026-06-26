from fastapi import FastAPI

app = FastAPI(title="Home Services API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Home Services API"}

@app.get("/services")
def get_services():
    services = [
        {"id": 1, "name": "AC Technician"},
        {"id": 2, "name": "Plumber"},
        {"id": 3, "name": "Electrician"},
        {"id": 4, "name": "Painter"},
        {"id": 5, "name": "Daily Wage Worker"},
    ]
    return {"services": services}
