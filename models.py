from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Car(Base):
    __tablename__ = "cars"
    make = Column(String)
    model = Column(String, primary_key=True)

    rates = relationship("Rate", back_populates="car")

class Rate(Base):
    __tablename__ = "rates"
    id = Column(Integer, primary_key=True)
    rate = Column(Integer)
    carModel = Column(String, ForeignKey("cars.model"))

    car = relationship("Car", back_populates="rates")