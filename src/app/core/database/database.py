from sqlmodel import Field, Session, create_engine
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os
load_dotenv()

url_conecction = os.getenv("URL_CONECCION")
engine = create_engine(url_conecction,echo= True)



def get_session():
    with Session(engine) as session:
        yield session # Se usa a menudo con frameworks web como FastAPI
        


session_dep = Annotated[Session, Depends(get_session)]