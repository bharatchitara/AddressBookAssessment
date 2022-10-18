from typing import Optional
import models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from models import Item
from database import SessionLocal, engine ,SQLALCHEMY_DATABASE_URL
from schema import locationData


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#create API
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

#get api by city name
@app.get("/api/getcity",status_code=200)
def getLocationByCityName(location: str):
    
    session = Session(bind=engine, expire_on_commit=False)
    
    reqLocation = location.lower()
    
    #location is case-insensiive and search using contanins method 
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
    

#get api by cordinates
@app.get("/api/getcordinates",status_code=200)
def getLocationByCordinates(latitude: int, longitude : int, accuracyLevel: int):
    
    session = Session(bind=engine, expire_on_commit=False)
    
    #latitude, longitude and accuracyLevel are required
    
    reqlatitude = latitude
    reqlongitude = longitude
    
    reqAccuracy = accuracyLevel
    
    level = 0
    
    #based on accuracy level the result will displayed, acceracy level input - (0 to 100)
    
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
        
    
        
        
    latitudemin  = reqlatitude-level
    latitudemax  = reqlatitude+level
    longitudemin  = reqlongitude-level
    longitudemax  = reqlongitude+level
    
    print(latitudemin,latitudemax, longitudemin , longitudemax)
        
    
    # rows=  session.query(Item).filter( (Item.Latitude >=  latitudemin & Item.Latitude <= latitudemax) & (Item.longitude >= longitudemin & Item.longitude <= longitudemax )).all()
    
    counter  = 0
    rows=  session.query(Item).filter((  Item.Latitude >=  latitudemin ) & ( Item.Latitude <= latitudemax  ) & (Item.Longitude >= longitudemin ) & (Item.Longitude <= longitudemax)).all()
    
    lst  = []
    
    for i in rows: 
        lst.append(i)
    
    # print(rows)
    count = len(lst)
                                                                                                                                        
    if (rows):
    
        message = "Fetched " +str(count) + " matching Records"
        msg = [{
         "success" : "true",
        "message": message ,
        "data": rows
        }]
    
    else:
        
        #if not records are found above, this block will automatically find the nearest result with default accuracy of >40% to <80%. 
        
        level = 2
        latitudemin  = reqlatitude-level
        latitudemax  = reqlatitude+level
        longitudemin  = reqlongitude-level
        longitudemax  = reqlongitude+level
        
        rows_2=  session.query(Item).filter((  Item.Latitude >=  latitudemin ) & ( Item.Latitude <= latitudemax  ) & (Item.Longitude >= longitudemin ) & (Item.Longitude <= longitudemax)).all()

        level = 1
        latitudemin  = reqlatitude-level
        latitudemax  = reqlatitude+level
        longitudemin  = reqlongitude-level
        longitudemax  = reqlongitude+level
        
        rows_1=  session.query(Item).filter((  Item.Latitude >=  latitudemin ) & ( Item.Latitude <= latitudemax  ) & (Item.Longitude >= longitudemin ) & (Item.Longitude <= longitudemax)).all()

        
        lst,lst2  = [],[]
        for i in rows_2: 
            lst.append(i)
        count1 = len(lst)
        
        for i in rows_1: 
            lst2.append(i)
        count2 = len(lst2)
        
        if(count1 > count2):
            print(count1,count2)
        
            
            message = "Fetched " +str(count2) + " matching Records"
            msg = [{
            "success" : "true",
            "message": message ,
            "data": rows_1
            }]
        
        else:
            
            message = "Fetched " +str(count1) + " matching Records"
            msg = [{
            "success" : "true",
            "message": message ,
            "data": rows_2
            }]
        
    
   
    session.close()
    
    return msg


#delete by id 
@app.delete("/api/delete",status_code=200)
def deleteRecords(id:int):
    
    
    
    reqId = id
    session = Session(bind=engine, expire_on_commit=False)

    deleteData = session.query(Item).filter(Item.id == reqId).delete()
    session.commit()
    
    if(deleteData):
        
        msg = [{
        "success": "true",
        "message": "Record deleted successfully"
        
        }]
        
    else:
        
        msg = [{
        "success": "false",
        "message": "Record deletion failed"
        
        }]
        
    
    session.close()
    return msg
    

#update by id(also works with parial and full table data update)
@app.patch("/api/updatelocation/{id}",status_code=201)
def updateRecords(id:int, location:  Optional[str] = None,  latitude : Optional[int] = 0, longitude:  Optional[int] = 0 ):
    
    reqId= id
    reqlocation = location
    reqlatitude = latitude
    reqlongitude = longitude    
    
    session = Session(bind=engine, expire_on_commit=False)
    
    updateRecord = session.query(Item).filter(Item.id == reqId).update( {Item.location : reqlocation, Item.Latitude : reqlatitude, Item.Longitude : reqlongitude} )
    
    session.close()
    
    if(updateRecord == 1 ):
    
        msg = [{
        "success": "true",
        "message": "Record updated successfully"
        }]
        
    else:
        msg = [{
        "success": "false ",
        "message": "Record updation failed"
        }]
    
    return msg
    

#find all records(no input required)
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
