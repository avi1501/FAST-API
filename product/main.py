from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends

from . import models
from .database import engine, SessionLocal
from .routers import product, seller, login

app = FastAPI(
    title="Products API",
    description="This is sample fast API app use username: admin, password: admin to authorise",
    terms_of_service = "http://www.google.com/images/india",
    contact_the_developer = {
        "Developer Name":"Avinash Kumar Mehta",
        "website":"https://github.com/avi1501",
        "emaii":"dummyemail@gmail.com",
    },
    license = {
        'name':"xyz"
    },

)


app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)


models.Base.metadata.create_all(engine)