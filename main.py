from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Service
from schemas import ServiceCreate, ServiceResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Services API")


# GET: Consultar todos los servicios
@app.get("/services", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


# GET: Consultar un servicio por ID
@app.get("/services/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# POST: Crear un servicio
@app.post("/services", response_model=ServiceResponse, status_code=201)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(
        name=data.name,
        price=data.price,
        description=data.description,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


# PUT: Actualizar un servicio existente
@app.put("/services/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    data: ServiceCreate,
    db: Session = Depends(get_db),
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    service.name = data.name
    service.price = data.price
    service.description = data.description

    db.commit()
    db.refresh(service)
    return service


# DELETE: Eliminar un servicio
@app.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}