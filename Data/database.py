import sqlite3





def create_database():            #base de datos
    
    conn = sqlite3.connect('data/predicciones.db')
    c = conn.cursor()
    c.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='predicciones'
    """)
    if not c.fetchone():
        c.execute('''CREATE TABLE predicciones
                     (id INTEGER PRIMARY KEY, Titulo text, URL text,Predict text)''')
        conn.commit()
    conn.close()

def add_customer(titulo, url, predict):
    conn = sqlite3.connect('data/predicciones.db')
    c = conn.cursor()
    c.execute("INSERT INTO predicciones (Titulo, URL, Predict) VALUES (?, ?, ?)", (titulo, url, predict))
    conn.commit()
    conn.close()

def delete_predict(titulo,registro_id):
    conn = sqlite3.connect('data/predicciones.db')
    c = conn.cursor()
    c.execute("DELETE FROM predicciones WHERE titulo=? OR id=?", (titulo, registro_id))
    conn.commit()
    conn.close()


def view_customers():
    conn = sqlite3.connect('data/predicciones.db')
    c = conn.cursor()
    c.execute("SELECT * FROM predicciones")
    customers = c.fetchall()
    conn.close()
    return customers

def search_customer(titulo, registro_id):
    conn = sqlite3.connect('data/predicciones.db')
    c = conn.cursor()
    c.execute("SELECT * FROM predicciones WHERE titulo=? OR id=?", (titulo, registro_id))
    customers = c.fetchall()
    conn.close()
    return customers
