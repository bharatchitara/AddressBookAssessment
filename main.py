import models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from models import Item
from database import SessionLocal, engine
from schema import locationData


app = FastAPI()

models.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/api/create",status_code=status.HTTP_201_CREATED)
def createRecord(create: locationData):
    
    session = Session(bind=engine, expire_on_commit=False)

    createLocation  = Item(location = create.location)

    session.add(createLocation)
    session.commit()
    
    session.close()
    
    id = createLocation.id
    
    msg  = [
        {
        "success" : "true",
        "message": "location added succssfully",
        "id": createLocation.id,
        "location": createLocation.location
    }
        ]
    
    return f"{msg}"



@app.get("/api/get",status_code=200)
def getlocation():
    


@app.get("/api/getAll",status_code=200)
def getAllRecords():
    
    session = Session(bind=engine, expire_on_commit=False)

    allLocationData = session.query(Item).all()

    session.close()

    return allLocationData

@app.get("/")
async def root():
    return {"message": "Hello World"}