from fastapi import FastAPI, Depends, status, Response
from pydantic import BaseModel
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from checkExist import check
from typing import List

class Car(BaseModel):
    make: str
    modelName: str

class Rate(BaseModel):
    rate: int
    model: str

class ShowAvgCar(BaseModel):
    make: str
    model: str
    avgRate: float

# class ShowPopluarCar(BaseModel):
#     make: str
#     model: str
#     amount_of_rate: float

class avgCar():
    make: str
    model: str
    avgRate: float
    def __init__(self,make,model,avgRate) -> None:
        self.make = make
        self.model = model
        self.avgRate = avgRate

class countCar():
    make: str
    model: str
    number_of_rates: int
    def __init__(self,make,model,number_of_rates) -> None:
        self.make = make
        self.model = model
        self.number_of_rates = number_of_rates
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/cars/", response_model=List[ShowAvgCar],  status_code=200)
def all_cars(response: Response,db: Session = Depends(get_db) ):
    
    cars = db.query( models.Car.make,models.Car.model, func.avg(models.Rate.rate).label("average")).join(models.Rate).group_by(models.Car.model).all()
    tab = []
    for i in cars:
        tab.append(avgCar(i[0],i[1],i[2]))

    if not tab:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Car is not available"}

    return tab

@app.get("/popular/",  status_code=200) #response_model=List[ShowPopluarCar],
def all_cars(response: Response,db: Session = Depends(get_db) ):
    cars = db.query( models.Car.make, models.Car.model, func.count(models.Rate.rate).label("suma")).join(models.Rate).group_by(models.Car.model).order_by(func.count(models.Rate.rate).desc()).all()
    tab = []
    for i in cars:
        tab.append(countCar(i[0],i[1],i[2]))
    
    if not tab:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Car is not available"}

    return tab

@app.post("/cars/", status_code=status.HTTP_201_CREATED)
def create_cars(r:Car, db: Session = Depends(get_db)):
    if(check(r.make, r.modelName)):
        try:
            new_car = models.Car(make = r.make, model = r.modelName)
            db.add(new_car)
            db.commit()
            db.refresh(new_car)
            return new_car
        except:
            return {"message": "SQL ERROR"}
    else:
        return {"message":"Car Not Found"}
    
@app.post("/rate/", status_code=status.HTTP_201_CREATED)
def add_rate(r:Rate, db: Session = Depends(get_db)):
    try:
        if(r.rate >=1 and r.rate <=5):
            new_rate = models.Rate(rate = r.rate, carModel = r.model)
            db.add(new_rate)
            db.commit()
            db.refresh(new_rate)
            return new_rate
        else:
            return {"message": "Rate must be between 1 and 5"}
    except:
        return {"message": "SQL ERROR"}
    

