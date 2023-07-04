from flask import Flask, jsonify, render_template,request,redirect
#Para conectar con la base de datos
from psycopg2 import connect, extras

#Instanciar la clase de flask
app = Flask(__name__)

#Contantes la base de datos
host = 'localhost'
port = 5432
dbname = 'justin'
username = 'postgres'
password = 2003

#Funcion para conectar a la base de datos
def get_database():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn


#Consultar todos los usuarios
@app.get('/app/users')
def get_users():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from pacientes")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    #Paso 5 convertir un objeto diccionario en un objeto json``
    print(user)    
    return jsonify(user)

#Mostrando datos en html
#Consultar todos los usuarios
@app.route('/api/users', methods=['GET'])
def get_users_html():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from pacientes")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    return render_template('select.html',pacientes=user)

#Delete
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete_users(id):
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("DELETE FROM pacientes where id = %s RETURNING *", (id,))
    #Paso 4 sacar datos a pantalla
    user_deleting = cursor.fetchone()

    if request.method == 'POST':
        if user_deleting:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/users')
        #abort(404)
    return render_template('delete.html', user=user_deleting)

#Update
@app.route('/<int:id>/edit', methods=['GET','POST'])
def update_user(id):

    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from pacientes where id = %s", (id,)) 
    # Paso 4 sacar datos a pantalla
    user_select = cursor.fetchone()
    cursor.close()
    conn.close()

    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        cedula = request.form['ci']
        nombre = request.form['name']
        telefono = request.form['cell']
        correo = request.form['correo']
        direccion = request.form['direc']
        alergia = request.form['alergia']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute("UPDATE pacientes SET cedula=%s, nombres=%s, telefono=%s, correo=%s, direccion=%s, alergia=%s WHERE id=%s RETURNING *",
                    (cedula,nombre,telefono,correo,direccion,alergia, id))
        #Paso 4 sacar datos a pantalla
        user_updating = cursor.fetchone()    
        if user_updating:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/users')
        #abort(404)
    return render_template('update.html', user=user_select)

#Create
@app.route("/", methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create.html')
    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        cedula = request.form['ci']
        nombre = request.form['name']
        telefono = request.form['cell']
        correo = request.form['correo']
        direccion = request.form['direc']
        alergia = request.form['alergia']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute('INSERT INTO pacientes (cedula,nombres,telefono,correo,direccion,alergia) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *',
                (cedula,nombre,telefono,correo,direccion,alergia))
        #Paso 4 sacar datos a pantalla
        user_creating = cursor.fetchone()    
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/api/users')
        #abort(404)






#DOCTORES

#Consultar todos los usuarios
@app.get('/app/docs')
def get_docs():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from doctores")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    #Paso 5 convertir un objeto diccionario en un objeto json``
    print(user)    
    return jsonify(user)

#Mostrando datos en html
#Consultar todos los usuarios
@app.route('/api/docs', methods=['GET'])
def get_docs_html():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from doctores")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    return render_template('selectdoc.html',doctores=user)

#Delete
@app.route('/<int:id>/docs/delete', methods=['GET','POST'])
def delete_docs(id):
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("DELETE FROM doctores where id = %s RETURNING *", (id,))
    #Paso 4 sacar datos a pantalla
    user_deleting = cursor.fetchone()

    if request.method == 'POST':
        if user_deleting:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/docs')
        #abort(404)
    return render_template('deletedoc.html', user=user_deleting)

#Update
@app.route('/<int:id>/docs/edit', methods=['GET','POST'])
def update_docs(id):

    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from doctores where id = %s", (id,)) 
    # Paso 4 sacar datos a pantalla
    user_select = cursor.fetchone()
    cursor.close()
    conn.close()

    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        cedula = request.form['cidocs']
        nombre = request.form['namedocs']
        telefono = request.form['celldocs']
        correo = request.form['correodocs']
        direccion = request.form['direcdocs']
        especialidad = request.form['especialidad']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute("UPDATE doctores SET cedula=%s, nombre=%s, telefono=%s, correo=%s, direccion=%s, especialidad=%s WHERE id=%s RETURNING *",
                    (cedula,nombre,telefono,correo,direccion,especialidad, id))
        #Paso 4 sacar datos a pantalla
        user_updating = cursor.fetchone()    
        if user_updating:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/docs')
        #abort(404)
    return render_template('updatedoc.html', user=user_select)

#Create
@app.route("/docs", methods=['GET','POST'])
def create_doc():
    if request.method == 'GET':
        return render_template('createdoc.html')
    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        cedula = request.form['cidocs']
        nombre = request.form['namedocs']
        telefono = request.form['celldocs']
        correo = request.form['correodocs']
        direccion = request.form['direcdocs']
        especialidad = request.form['especialidad']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute('INSERT INTO doctores (cedula,nombre,telefono,correo,direccion,especialidad) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *',
                (cedula,nombre,telefono,correo,direccion,especialidad))
        #Paso 4 sacar datos a pantalla
        user_creating = cursor.fetchone()    
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/api/docs')
        #abort(404)



#Citas

#Consultar todos los usuarios
@app.get('/app/citas')
def get_citas():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from citas")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    #Paso 5 convertir un objeto diccionario en un objeto json``
    print(user)    
    return jsonify(user)

#Mostrando datos en html
#Consultar todos los usuarios
@app.route('/api/citas', methods=['GET'])
def get_citas_html():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from citas")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    return render_template('selectcita.html',citas=user)

#Delete
@app.route('/<int:id>/citas/delete', methods=['GET','POST'])
def delete_citas(id):
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("DELETE FROM citas where id = %s RETURNING *", (id,))
    #Paso 4 sacar datos a pantalla
    user_deleting = cursor.fetchone()

    if request.method == 'POST':
        if user_deleting:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/citas')
        #abort(404)
    return render_template('deletecita.html', user=user_deleting)

#Update
@app.route('/<int:id>/citas/edit', methods=['GET','POST'])
def update_citas(id):

    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from citas where id = %s", (id,)) 
    # Paso 4 sacar datos a pantalla
    user_select = cursor.fetchone()
    cursor.close()
    conn.close()

    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        dia = request.form['dia']
        hora = request.form['hora']
        servicio = request.form['servicio']
        receta = request.form['receta']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute("UPDATE citas SET cedula=%s, nombre=%s, telefono=%s, dia=%s, hora=%s, servicio=%s, receta=%s WHERE id=%s RETURNING *",
                    (cedula,nombre,telefono,dia,hora,servicio,receta, id))
        #Paso 4 sacar datos a pantalla
        user_updating = cursor.fetchone()    
        if user_updating:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/citas')
        #abort(404)
    return render_template('updatecita.html', user=user_select)

#Create
@app.route("/citas", methods=['GET','POST'])
def create_cita():
    if request.method == 'GET':
        return render_template('createcita.html')
    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        dia = request.form['dia']
        hora = request.form['hora']
        servicio = request.form['servicio']
        receta = request.form['receta']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute('INSERT INTO citas (cedula,nombre,telefono,dia,hora,servicio,receta) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *',
                (cedula,nombre,telefono,dia,hora,servicio,receta))
        #Paso 4 sacar datos a pantalla
        user_creating = cursor.fetchone()    
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/api/citas')
        #abort(404)

#Para colocar en modo debug, modo desarrallador
if __name__ == '__main__':
    app.run(debug=True)