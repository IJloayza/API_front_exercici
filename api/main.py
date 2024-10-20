from fastapi import FastAPI,HTTPException, Request, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Union
from fastapi.middleware.cors import CORSMiddleware

import db_alumnes
import alumnes
import csv
import io
from typing import List
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Añadido datetime como prueba para error de conversión de createdAt y updatedAt a string
class Alumne(BaseModel):
    idAlumne:int
    idAula:int
    nomAlumne:str
    cicle:str
    curs:str
    grup:str
    createdAt:datetime 
    updatedAt:datetime

class tablaAlumne(BaseModel):
    NomAlumne:str
    Cicle:str
    Curs:str
    Grup:str
    DescAula:str

@app.get("/")
def read_root():
    return {"alumnes API"}

@app.get("/alumne/list", response_model=List[tablaAlumne])
#@app.get("/alumne", response_model=List[tablaAlumne])
def read_alumnes(orderby: Union[str,None] = None, contain: Union[str,None] = None,skip: Union[int,None] =None, limit: Union[int,None]=None):
    order=orderby is not None and (orderby.lower() == "asc" or orderby.lower() == "desc")
    cont=contain is not None
    lim=skip is not None and limit is not None
    #Si mepasan todos los valores desde el inicio aplicare todos los valores en la busqueda 
    if order and cont and lim:
        adb = db_alumnes.read_alumnes(order,contain,skip,limit)
    elif order:
        adb = db_alumnes.read_alumnes(orderby,None)
    elif cont:
        #Si me pasa el contain paso el valor de order como nulo para evitar inyecciones
        adb = db_alumnes.read_alumnes(None, contain)
    elif lim:
        #Asi igualmente como en el ejemplo anterior pero con skip y limit
        adb = db_alumnes.read_alumnes(None,None,skip,limit)
    else:
        adb = db_alumnes.read_alumnes()
    alumnes_sch = alumnes.tabla_alumnes_schema(adb)
    if not alumnes_sch:
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne")
    return alumnes_sch

"""Mostrar un solo alumno a partir de un id retorna Internal server error"""
@app.get("/alumne/show/{id}", response_model=Alumne)
def read_alumnes_id(id:int):
    refAlumne = db_alumnes.read_id_alumne(id)
    if refAlumne is None:
        raise HTTPException(status_code=404, detail="No s'ha trobat l'alumne")
    alumne = alumnes.alumne_schema(refAlumne)
    return alumne
"""Encontrar una forma de iniciar el alumno y el aula y adjuntarlos para la respuesta"""
@app.get("/alumne/listAll", response_model=List[dict])
def read_alumnes_all():
    refAlumne = db_alumnes.read_alumne_all()
    alumne = alumnes.alumnes_all_schema(refAlumne)
    if alumne is None:
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne")
    return alumne
"""Crear un alumno recibiendo los datos como parametros"""
@app.post("/alumne/add")
async def create_alumne(data:Alumne):
    idAula=data.idAula
    nomAlumne=data.nomAlumne
    cicle=data.cicle
    curs=data.curs
    grup=data.grup
    alumne_id = db_alumnes.create_alumne(idAula,nomAlumne,cicle,curs,grup)
    return{
        "msg": "S'ha afegit correctament",
        "id alumne": alumne_id,
        "nomAlumne": nomAlumne
    }

"""Crear un metodo que recibira un csv como post y creara unos alumnos y sus respectivas aulas con la informacion dada"""
@app.post("/alumne/loadAlumnes")
async def loadAlumnes(csvAlum: UploadFile):
    #Este método permite saber el tipo de file recibido gracias a multiparter
    if csvAlum.content_type != "text/csv":
        #Si no es de tipo csv error de invalid input
        raise HTTPException(status_code=403, detail="El file introduït ha de ser de tipus csv")
    #Leer el archivo csv en su totalidad
    content = await csvAlum.read()
    #Decodificar en formato UTF-8
    decodContent = content.decode("utf-8")
    csv_reader=csv.reader(io.StringIO(decodContent))
    """ next(csv_reader) """
    ids = []
    for row in csv_reader:
        descAula = row[0]
        edifici = row[1]
        pis = row[2]
        idAulaIs = db_alumnes.checkAula(descAula)
        if idAulaIs is not None and isinstance(idAulaIs, dict):
            idAulaIs = idAulaIs.get("IdAula")
        if idAulaIs is None:
            idAulaIs = db_alumnes.create_aula(descAula,edifici,pis)
            if isinstance(idAulaIs, dict):
                idAulaIs = idAulaIs.get("IdAula")
        nomAlumne = row[3]
        cicle =row[4]
        curs =row[5]
        grup =row[6]
        alumneIsIn = db_alumnes.checkAlumneInAula(descAula,nomAlumne)
        if alumneIsIn[0] == 0:
            alumne = db_alumnes.create_alumne(idAulaIs[0],nomAlumne,cicle,curs,grup)
            ids.append(str(idAulaIs) + " "+ str(nomAlumne))
    return ids

        


"""Actualizar un alumno utilizando su id como llave para encontrarlo"""
@app.put("/alumne/update/{id}")
def update_alumne(id:int,idAula:Union[int,None]= None,nom:Union[str,None] =None,cicle:Union[str,None]=None,curs:Union[str,None]=None,grup:Union[str,None]=None):
    alumne = db_alumnes.read_id_alumne(id)
    if alumne is None:
        raise HTTPException(status_code=404, detail="Alumne no trobat")
    updated_records = db_alumnes.update_alumne(id,idAula,nom,cicle,curs,grup)
    if updated_records == 0:
       raise HTTPException(status_code=404, detail="Alumne no actualitzat")
    return alumne

"""Borrar alumnos por su id"""
@app.delete("/alumne/delete/{id}")
def delete_alumne(id:int):
    alumne = db_alumnes.read_id_alumne(id)
    if alumne is None:
       raise HTTPException(status_code=404, detail="Alumne no trobat")  
    deleted_records = db_alumnes.delete_alumne(id)
    if deleted_records == 0:
       raise HTTPException(status_code=404, detail="El alumne no ha estat esborrat") 
    return alumne
     
