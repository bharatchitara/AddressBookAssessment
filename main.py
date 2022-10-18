import models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from models import Item
from database import SessionLocal, engine ,SQLALCHEMY_DATABASE_URL
from schema import locationData
from flask_sqlalchemy import SQLAlchemy


app = FastAPI()

models.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/api/createlocation",status_code=201)
def createRecord(create: locationData):
    
    session = Session(bind=engine, expire_on_commit=False)

    createLocation  = Item(location = create.location)

    session.add(createLocation)
    session.commit()
    session.close()
    
    id = createLocation.id
    
    if(id):
    
        msg  = [
        {
        "success" : "true",
        "message": "location added succssfully",
        "id": createLocation.id,
        "City Name": createLocation.location
    }
        ]
        
    else:
        
         msg  = [
        {
        "success" : "false",
        "message": "Some Error occured"
    }
        ]
        
    
    return msg



@app.get("/api/getcity",status_code=200)
def getLocationByCityName(location: str):
    
    session = Session(bind=engine, expire_on_commit=False)
    
    reqLocation = location.lower()
    
    
    
    rows=  session.query(Item).filter(Item.location.contains(reqLocation)).all()
    
    session.close()
    
    if(rows):
    
        message = "Fetched Records with CityName: "+ reqLocation
    
        msg = [{
         "success" : "true",
        "message": message ,
        "data": rows
        }]
        
    else:
        
        msg = [{
            "success" : "false",
            "message": "No data found" 
        }]
        

    return msg
    


@app.get("/api/getcordinates",status_code=200)
def getLocationByCordinates(latitude: int, longitude : int, accuracyLevel: int):
    
    session = Session(bind=engine, expire_on_commit=False)
    
    reqlatitude = latitude
    reqlongitude = longitude
    
    reqAccuracy = accuracyLevel
    
    level = 0
    
    if(reqAccuracy < 0): 
        level = 5
        
    elif(reqAccuracy >=0 and reqAccuracy <=20):
        level = 4
        
    elif(reqAccuracy >=21 and reqAccuracy <=40):
        level =3
    
    elif(reqAccuracy>= 41 and reqAccuracy <=60 ):
        level = 2
        
    elif(reqAccuracy >=61 and reqAccuracy <=80):
        level = 1
    
    elif(reqAccuracy >=81 ):
        level = 0.5
        
    else: 
        level = 2 
        
        
    latitudemin  = reqlatitude-level
    latitudemax  = reqlatitude+level
    longitudemin  = reqlongitude-level
    longitudemax  = reqlongitude+level
    
    print(latitudemin,latitudemax, longitudemin , longitudemax)
        
    
    # rows=  session.query(Item).filter( (Item.Latitude >=  latitudemin & Item.Latitude <= latitudemax) & (Item.longitude >= longitudemin & Item.longitude <= longitudemax )).all()
    
    counter  = 0
    rows=  session.query(Item).filter((  Item.Latitude >=  latitudemin ) & ( Item.Latitude <= latitudemax  ) & (Item.Longitude >= longitudemin ) & (Item.Longitude <= longitudemax
                                                                                                                                                    )).all()
    
    session.close()
    lst = []
    for i in rows:
        
        lst.append(i)
        
    print(len(lst))
    
    
    return rows



@app.get("/api/getAll",status_code=200)
def getAllRecords():
    
    session = Session(bind=engine, expire_on_commit=False)

    allLocationData = session.query(Item).all()
    
    session.close()
    
    if(allLocationData):
        
        msg = [{
         "success" : "true",
        "message": "Fetched all records successfully",
        "data": allLocationData
            }]
        
    else:
        msg = [{
         "success" : "false",
        "message": "No records found"
            }]

    return msg



@app.get("/")
async def root():
    return {"message": "Hello World"}