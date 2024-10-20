from client import db_client

def read_alumnes(order=None,contain=None,skip=None,limit=None):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select a.NomAlumne, a.Cicle, a.Curs, a.Grup, l.DescAula from alumne a JOIN aula l ON (a.IdAula=l.IdAula)"
        if contain is not None:
            query = query + "WHERE NomAlumne LIKE '%"+contain+"%'"
        if order is not None:
            query = query + " ORDER BY NomAlumne " + order
        if skip is not None and limit is not None:
            query = query + (f"LIMIT {limit} OFFSET {skip}")
        cur.execute(query)
        alumnes = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return alumnes

def create_alumne(idAula,nomAlumne,cicle,curs,grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "insert into alumne (IdAula,NomAlumne,Cicle,Curs,Grup) VALUES (%s,%s,%s,%s,%s);"
        values=(idAula,nomAlumne,cicle,curs,grup)
        cur.execute(query,values)
    
        conn.commit()
        alumne_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return alumne_id

# Seleccionar un alumno usando su id
def read_id_alumne(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select * from alumne WHERE IdAlumne = %s"
        value = (id,)
        cur.execute(query,value)
    
        alumne = cur.fetchone()

    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return alumne

def read_alumne_all():
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select a.idAlumne, a.idAula, a.NomAlumne, a.Cicle, a.Curs, a.Grup, u.descAula, u.Edifici, u.Pis from alumne a JOIN aula u ON a.idAula = u.idAula"
        cur.execute(query)
    
        alumne = cur.fetchall()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return alumne

def create_alumne(idAula,nomAlumne,cicle,curs,grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "insert into alumne (IdAula,NomAlumne,Cicle,Curs,Grup) VALUES (%s,%s,%s,%s,%s);"
        values=(idAula,nomAlumne,cicle,curs,grup)
        cur.execute(query,values)
    
        conn.commit()
        alumne_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return alumne_id

def create_aula(descAula,edifici,pis):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "insert into aula (DescAula, Edifici, Pis) VALUES (%s,%s,%s);"
        values=(descAula,edifici,pis)
        cur.execute(query,values)
        conn.commit()
        aula_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return aula_id

def update_alumne(id,idAula=None,nom=None,cicle=None,curs=None,grup=None):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = []
        values = []
        if idAula is not None:
            query.append("IdAula = %s")
            values.append(idAula)
        if nom is not None:
            query.append("NomAlumne = %s")
            values.append(nom)
        if cicle is not None:
            query.append("Cicle = %s")
        if curs is not None:
            query.append("Curs = %s")
            values.append(curs)
        if grup is not None:
            query.append("Grup = %s")
            values.append(grup)
        if not query:
            return {"status": -1, "message": "No se proporcionaron datos para actualizar"}
        query = (f"UPDATE Alumne SET {', '.join(query)} WHERE IdAlumne ={id};")
        values.append(id)
        cur.execute(query,tuple(values))
        updated_recs = cur.rowcount
    
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"+ " "+query }
    
    finally:
        conn.close()

    return updated_recs

def delete_alumne(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM Alumne WHERE IdAlumne = %s;"
        cur.execute(query,(id,))
        deleted_recs = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_recs
def checkAula(desc):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT IdAula FROM aula WHERE DescAula= %s;"
        cur.execute(query,(desc,))
        aula = cur.fetchone()
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return aula

def checkAlumneInAula(descAula,nomAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT COUNT(*) as id FROM Alumne JOIN Aula ON (Alumne.IdAula=Aula.IdAula) WHERE Aula.DescAula= %s AND Alumne.NomAlumne= %s;"
        cur.execute(query,(descAula,nomAlumne))
        aula = cur.fetchone()
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return aula
