from fastapi import FastAPI, HTTPException
from routers import routers
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.include_router(routers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend ko allow karega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers)



