from fastapi import FastAPI, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {'message': 'Patient Management System'}

@app.get("/about")
def get_about():
    return {"message": "This is the about page."}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/view/ {patient_city}')
def view_by_city(patient_city: str):
    data = load_data()
    filtered_data = [patient for patient in data if patient['city'].lower() == patient_city.lower()]
    return filtered_data

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Sort patients by a height,weight or bmi"), order: str = Query('asc', description="Order of sorting: 'asc' for ascending, 'desc' for descending")):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: 'asc' or 'desc'")
    
    data = load_data()
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return sorted_data