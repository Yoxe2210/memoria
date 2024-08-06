import sqlite3


conexion = sqlite3.connect('JUEGO.db')

cursor = conexion.cursor()
cursor.execute('''CREATE TABLE PADRES(ID INTEGER PRIMARY KEY,
                    NOMBRE VARCHAR NOT NULL,
                    APELLIDO VARCHAR,
                    EDAD INTEGER,
                    CEDULA INTEGER,
                    SEXO VARVCHAR,
                    DIRECCION VARCHAR
                    )''')

conexion.commit()
conexion.close()





