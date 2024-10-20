# Convertir un alumne en dict 
def alumne_schema(alumne) -> dict:
    return {"idAlumne": alumne[0],
            "idAula": alumne[1],
            "nomAlumne": alumne[2],
            "cicle": alumne[3],
            "curs": alumne[4], 
            "grup": alumne[5],
            "createdAt":alumne[6],
            "updatedAt":alumne[7]
            }
# Convertir un alumne en tablaAlumne 
def tabla_alumne_schema(alumne) -> dict:
    return {"NomAlumne": alumne[0],
            "Cicle": alumne[1],
            "Curs": alumne[2], 
            "Grup": alumne[3],
            "DescAula":alumne[4]
            }

def alumne_all_schema(datos) -> dict:
    return {
            "idAlumne":datos[0],
            "idAula":datos[1],
            "nomAlumne":datos[2],
            "cicle":datos[3],
            "curs":datos[4],
            "grup":datos[5],
            "descAula":datos[6],
            "edifici":datos[7],
            "pis":datos[8],
            }

def tabla_alumnes_schema(alumnes) -> dict:
    return [tabla_alumne_schema(alumne) for alumne in alumnes]

def alumnes_schema(alumnes) -> dict:
    return [alumne_schema(alumne) for alumne in alumnes]

# Es posible usar estos metodos desde aula.py para agregarlos a alumno y construir un dict conjunto en lugar de hacerlo todo en uno?
def alumnes_all_schema(alumnes) -> dict:
    return [alumne_all_schema(alumne) for alumne in alumnes]