import mysql.connector

def db_client():
    
    try:
        dbname = "alumnat"
        user = "root"
        password = "used to be"
        host = "localhost"
        port = "3306"
        
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            collation ="utf8mb4_general_ci" 
        ) 
            
    except Exception as e:
            return {"status": -1, "message": f"Error de connexió:{e}" }
    