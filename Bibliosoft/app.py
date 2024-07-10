from flask import Flask, flash,jsonify, render_template, request, redirect, url_for, session
from flask_login import login_required
from flask_mysqldb import MySQL
from functools import wraps
import os

# Models:
from models.ModelUser import ModelUser
# Entities:
from models.entities.User import User

app = Flask(__name__)

app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'bibliosoft'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


#************************************|||  NOTICIAS O MENU DE LA PAGINA
#?PAGINA DE NOTICIAS
@app.route('/inicio')
def inicio():
    idUser = session.get('idUser');
    modul = modules(str(idUser))
    return render_template('inicio.html',moduls=modul)

#************************************||| INICIO DE SESION
#? PAGINA DE INICIO
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['Username'], request.form['Password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            session['idUser'] =logged_user[0]
            return redirect(url_for('inicio'))  # Redirige a la ruta perfil
        else:
            flash("Usuario no encontrado o contraseña incorrecta.", "error")

    return render_template('index.html')

#************************************||| PERFIL DE USUARIO
#?PERFIL DEL USUARIO
@app.route('/perfil')
def perfil():
    idUser = session.get('idUser');
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM datauser WHERE id=%s and status=1',(idUser,))
    data = cur.fetchone()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM perfil')
    perfiles = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT datauser.*, perfil.nombre as perfil_nombre
        FROM datauser
        INNER JOIN perfil ON datauser.id_perfilFK = perfil.id
        WHERE datauser.status = 1
    ''')
    data = cur.fetchone()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM perfil')
    perfil = cur.fetchall()
    cur.close()
    usuario = session.get('usuario')
    rest = restricciones(str(idUser),'perfil')
    modul = modules(str(idUser))
    return render_template('perfil.html', data=data, perfil=perfiles, moduls=modul,rests = rest)

#? ACTUALIZAR LOS DATOS DEL USUARIO
@app.route('/Update/perfil', methods=['GET', 'POST'])
def UpdatePerfil():
    if request.method == 'POST':
        user_id =session.get('idUser')
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        curp = request.form['curp'] 
        correo = request.form['correo'] 

        cur = mysql.connection.cursor()
        cur.execute('UPDATE datauser SET nombre = %s, telefono = %s, curp = %s, correo = %s WHERE id = %s', (nombre, telefono, curp, correo, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect('/perfil')

#************************************||| PAGINA DE USUARIO
#?ENTRADA DE URL PARA AFREFAR USUARIOS
@app.route('/usuarios')
def inicioUsuario():
    idUser = session.get('idUser');
    rest = restricciones(str(idUser),'usuarios')
    modul = modules(str(idUser))
    return render_template('usuarios.html',moduls=modul,rests = rest)


#? OBTENER LOS DATOS PARA LA TABLA
@app.route('/usuarios/data')
def inicioData():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vw_usertable WHERE status=1')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#? CREACION DE UN NUEVO USUARIO A LA BASE DE DATOS
@app.route('/usuarios', methods=['POST'])
def createUser():
    print(request.form)
    if request.method == 'POST':
        nombre = request.form['nombre'];
        username =request.form['username'];
        fechanaci= request.form['fechanaci'];
        curp= request.form['curp'];
        psw= request.form['psw'];
        telefono= request.form['telefono'];
        correo= request.form['correo'];
        genero= request.form['genero'];
        perfil= request.form['perfil'];

        user = User(0, username, psw)
        password = user.create_password(psw)
        cur = mysql.connection.cursor();
        try:

            cur.execute("INSERT INTO user (username, password, fullname, curp, telefono, correo, fechanacimiento, fechacreacion, id_direccionFK, id_generoFK, id_perfilFK, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,password,nombre,curp,telefono,correo,fechanaci,'2001-09-09',1,genero,perfil,1));
            cur.connection.commit()
            id_user = cur.lastrowid;
            print(id_user)
            if perfil == '1':
                cur.execute('INSERT INTO secretario (id_userFK,estatus) value(%s,1)',(id_user,))
                cur.connection.commit()
            if perfil == '2':
                cur.execute('INSERT INTO afiliado (id_userFK,estatus) value(%s,1)',(id_user,))
                cur.connection.commit()

            flash('Usuario Añadido Correctamente', 'success')
        except:
            print('IS NOT CREATED THE USER')

    cur.close()

    return  redirect(url_for('inicioUsuario'))

#?ELIMINAR UN USUARIO DE LA BASE DE DATOS
@app.route('/usuarios/delete/<string:id>', methods=['POST'])
def delete_user(id):
    if request.method == 'POST':

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE user SET status="0" WHERE user_id = %s ',(id,))
            cur.connection.commit()
            flash('Usuario Borrado Correctamente', 'success')
        except:
            print('ERROR DELETE')
    cur.close()

    return  redirect(url_for('inicioUsuario'))

#? BUSQUEDA DE UN ID DE USUARIO PARA ACTUALIZAR Y LLEVAR LOS DATOS A LA INTERFAZ
@app.route('/usuarios/update/<string:id>', methods=['POST'])
def update_get_user(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM datauser WHERE id = %s ",(id,))
            data = cur.fetchall()

            flash('Usuario seleccionado Correctamente', 'success')
        except:
            print('ERROR UPDATE')
    cur.close()
    return jsonify({"datos":data});  #redirect(url_for('inicio'))

#? DATOS ACTUALIZADOS ENVIADOS POR EL USUARIO
@app.route('/usuarios/update/<string:id>/', methods=['POST'])
def update_set_user(id):
    if request.method == 'POST':

        nombre = request.form['nombre'];
        username =request.form['username'];
        fechanaci= request.form['fechanaci'];
        curp= request.form['curp'];
        telefono= request.form['telefono'];
        correo= request.form['correo'];
        genero= request.form['genero'];
        perfil= request.form['perfil'];
        cur = mysql.connection.cursor()

        try:
            cur.execute('UPDATE user SET fullname=%s,username=%s,fechanacimiento=%s,curp=%s,telefono=%s,correo=%s,id_generoFK=%s,id_perfilFK=%s WHERE user_id = %s ',(nombre,username,fechanaci,curp,telefono,correo,genero,perfil,id,))
            cur.connection.commit()
            flash('Usuario Actualizado Correctamente', 'success')
        except:
            print('ERROR AL ACTUALIZAR')
    cur.close()
    return  redirect(url_for('inicioUsuario'))

#***********************************||| CATALOGO DE LIBROS
#?PAGINA DE INCIO PARA EL CATALOGO
@app.route('/catalogo')
def inicioCatalogo():
    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'catalogo')
    return render_template('catalogo.html',moduls=modul,rests = rest)

#? LLEVAR LOS DATOS A LA INTERFAZ DE LA TABLA
@app.route('/catalogo/data')
def dataCatalogo():
    cur = mysql.connection.cursor()
    cur.execute('select * from vw_catalogo')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#*************************************||| PRESTAMOS
#?PAGINA DE INICIO DEL CATALOGO
@app.route('/prestamo')
def inicioPrestamo():

    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'prestamo')
    return render_template('prestamo.html',moduls=modul,rests = rest)

#?LLEVAR DATOS A LA TABLA DE PRESTAMO
@app.route('/prestamo/data')
def dataPrestamo():
    cur = mysql.connection.cursor()

    idUser = session.get('idUser');
    cur.execute('select id_perfilFK from datauser where id=%s',(idUser,))
    perfilFK = cur.fetchall()
    
    data = {}

    if perfilFK[0][0] == 2:
        cur.execute('select * from vw_prestamo where user_id=%s',(idUser,));
        data = cur.fetchall()

    if perfilFK[0][0] == 1:
        cur.execute('select * from vw_prestamo');
        data = cur.fetchall()

    cur.close()

    return jsonify({"datos":data});

#? VER LOS DATOS DE UN PRESTAMO
@app.route('/prestamo/detalle/<string:id>', methods=['POST'])
def detalle_post_user(id):
    if request.method == 'POST':
        data = {}
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM vw_dtprestamo WHERE id_prestamo = %s ",(id,))
            data = cur.fetchall()

            flash('Detalle enconntrado', 'success')
        except:
            print('ERROR BUSQUEDA')
    cur.close()
    return jsonify({"datos":data});

#? CREAR UN NUEVO PRESTAMO
@app.route('/prestamo/nuevoprestamo',methods=['POST'])
def prestamo_nuevo():
    idUser = session.get('idUser');

    if request.method == 'POST':
        cur =mysql.connection.cursor()

        secre = 'null'
        id_prestamo = 'null'
        try:
            cur.execute('SELECT id FROM secretario WHERE id_userFK='+str(idUser));
            secre = cur.fetchall()
        except:
            print('no exist')
        try:
            afiliado =request.form['afiliado'];
            cur.execute('SELECT id FROM afiliado where id_userFK=%s',(str(afiliado),))
            id_afilado = cur.fetchall();
            fechEntrega =request.form['fechaEntrega'];

            sql = 'INSERT INTO prestamo (id_afiliadoFK, id_secretarioFK, fechaprestamo, fechaentrega, estatus) VALUES ('+str(id_afilado[0][0])+','+str(secre[0][0])+',date(NOW()),"'+str(fechEntrega)+'",1)'
            print(sql)
            cur.execute(sql);
            cur.connection.commit()
            id_prestamo = cur.lastrowid;

        except:
            print('ERROR WHEN CREATING THE NEW LOAN')

        tamano = len( request.form)
        try:
            for i in range(1,tamano):
                idLibro = request.form.get('numeroSerie'+ str(i),None)
                #//! SOLUCIONAR EL "1" DEL IDESTADO POR "None"
                #//! BUSCAR PORQUE DA "None" AL INICIO (SE COLOCO 1 CUANDO SEA VACIO)
                idEstado = request.form.get('estadoLibro'+ str(i),1)

                if idLibro:
                    sql = 'INSERT INTO det_prestamo (id_libroFK, id_estadoFK, id_prestamoFK, estatus) VALUES ('+str(idLibro)+','+str(idEstado)+' ,'+str(id_prestamo)+' ,1 )';
                    cur.execute(sql)
                    cur.connection.commit()
        except:
            print('error detalle')

    return redirect(url_for('inicioPrestamo'))

#? LIBRO ENTREGADO
@app.route('/prestamo/entregado/<string:id>',methods=['POST'])
def libroEntregado(id):
    cur = mysql.connection.cursor()

    try:
        cur.execute('UPDATE prestamo SET estatus = %s WHERE id=%s',(0,id));
        cur.connection.commit()
    except:
        print('error')

    return redirect(url_for('inicioPrestamo'))


#todo SECCION DE LIBRO (Libro, editorial, pais, categoria, autor, area)

#***************LIBRO**********************

#?PAGINA PRINCIPAL DE LIBRO (PARECIDA AL CATALOGO)
@app.route('/libro')
def libro():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM editorial WHERE estatus=1;');
    editoriales = cur.fetchall()
    cur.execute('SELECT * FROM pais WHERE estatus=1;');
    paises = cur.fetchall()
    cur.execute('SELECT * FROM tipolibro WHERE estatus=1;');
    categorias = cur.fetchall()
    cur.execute('SELECT * FROM autor WHERE estatus=1;');
    autores = cur.fetchall()
    cur.execute('SELECT * FROM area WHERE estatus=1;');
    areas = cur.fetchall()


    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'libro')
    return render_template('libros.html', paises = paises,
    editoriales = editoriales,
    categorias = categorias, autores = autores,
    areas = areas, moduls=modul,rests = rest
    )

#? CREAR UN UEVO LIBRO
@app.route('/libro/create',methods=['POST'])
def create_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        image = request.files["portada"]
        ISBN = request.form['ISBN']
        editorial = request.form['editorial']
        pais = request.form['pais']
        categoria = request.form['categoria']
        fechaLanza = request.form['fechalanza']
        edicion = request.form['edicion']
        existencia = request.form['existencia']
        autor = request.form['autor']
        area = request.form['area']
        id_libro = ''
        cur = mysql.connection.cursor()

        if image and image.filename:
            nameImg = image.filename
            image.save(os.path.join('./static/imgl',nameImg))
        
        try:
            sql = 'INSERT INTO libro (titulo, ISBN, id_editorialFK,if_paisFK,id_tipolibroFK,fechalanzamiento,edicion,existencia,estatus,imgl) VALUE ("'+str(titulo)+'",'+str(ISBN)+','+str(editorial)+','+str(pais)+','+str(categoria)+',"'+str(fechaLanza)+'",'+str(edicion)+','+ str(existencia)+',1,"'+str(image.filename)+'")'
            print(sql)
            cur.execute(sql)
            cur.connection.commit()
            id_libro = cur.lastrowid;
            flash('LIBRO Añadido Correctamente', 'success')
        except:
            print('ERROR CREATED BOOK')
        
        try:
            sql = 'INSERT INTO libroautor(id_libroFK,id_autorFK,estatus) VALUE ('+str(id_libro)+','+str(autor)+', 1)';
            print(sql)
            cur.execute(sql)
            cur.connection.commit()

            sql = 'INSERT INTO libroarea(id_libroFK,id_areaFK,estatus) VALUE ('+str(id_libro)+','+str(area)+', 1)';
            print(sql)
            cur.execute(sql)
            cur.connection.commit()
        except:
            print('Autor y area FALLIDOS')
    return redirect(url_for('libro'))

#? LLEVA DATOS A LA INTERFAZ PARA ACTUALIZAR
@app.route('/libro/update/<string:id>',methods=['get'])
def get_data_id_libro(id):
    data = {};
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT l.id, l.titulo,l.ISBN,l.id_editorialFK,l.if_paisFK,l.id_tipolibroFK,fn_fecha(l.fechalanzamiento) as fechalanzamiento, l.edicion,l.existencia,l.estatus,l.imgl, lar.id_areaFK,lau.id_autorFK FROM libro as l join libroarea as lar on l.id=lar.id_libroFK join  libroautor as lau on l.id=lau.id_libroFK WHERE l.id=%s',(id,))
        data = cur.fetchall()
        print(data)
    except Exception as e:
        print('ERROR SELECT ')

    return jsonify({"datos":data});

#? ACTUALIZA LOS DATOS DEL LIBRO
@app.route('/libro/update/<string:id>/',methods=['POST'])
def datas_id_libro_update(id):

    if request.method=='POST':
        cur = mysql.connection.cursor()
        print(request.form)
        print(id)
        try:
            cur.execute('UPDATE libro SET titulo="'+str(request.form['titulo'])+'",ISBN="'+str(request.form['ISBN'])+'",id_editorialFK='+str(request.form['editorial'])+',if_paisFK='+str(request.form['pais'])+',id_tipolibroFK='+str(request.form['categoria'])+',fechalanzamiento="'+str(request.form['fechalanza'])+'",edicion='+str(request.form['edicion'])+',existencia='+str(request.form['existencia'])+' WHERE id=%s;',(id,))
            cur.connection.commit()

            cur.execute('UPDATE libroarea SET id_areaFK=%s WHERE id_libroFK=%s',(str(request.form['area']),id));
            cur.connection.commit()

            cur.execute('UPDATE libroautor SET id_autorFK=%s WHERE id_libroFK=%s',(str(request.form['autor']),id))
            cur.connection.commit()

            flash('Editorial Actualizado Correctamente', 'success')

        except:
            print('ERROR UPDATE BOOK')
    return redirect(url_for('libro'))

#*************************||| EDITORIAL

#? EDITORIAL DEL LIBRO
@app.route('/libro/editorial')
def libroEditoria():
    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'libro')
    return render_template('editorial.html',moduls=modul,rests = rest)

#? LLEVAR DATOS A LOS LIBROS
@app.route('/libro/editorial/data')
def libroEditoriaData():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM editorial WHERE estatus=1')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#? CREAR UNA NUEVA EDITORIAL
@app.route('/libro/editorial/create',methods=['POST'] )
def libroEditorialCreate():
    if request.method == 'POST':
        nombre = request.form['nombre'];
        cur = mysql.connection.cursor();
        try:
            cur.execute("INSERT INTO editorial (editorial, estatus) VALUES (%s,%s)",(nombre,1));
            cur.connection.commit()
            flash('Editorial Añadido Correctamente', 'success')
        except:
            print('IS NOT CREATED THE EDITORIAL')
    cur.close()
    return  redirect(url_for('libroEditoria'))

#? LLEVAR LOS DATOS DE UNA EDITORIAL A ACTUALIZAR
@app.route('/libro/editorial/update/<string:id>', methods=['POST'])
def update_get_editorial(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM editorial WHERE id = %s ",(id,))
            data = cur.fetchall()

            flash('editorial seleccionado Correctamente', 'success')
        except:
            print('ERROR UPDATE')
    cur.close()
    return jsonify({"datos":data});

#? ACTUALIZAR UNA EDITORIAL
@app.route('/libro/editorial/update/<string:id>/', methods=['POST'])
def update_set_editorial(id):
    if request.method == 'POST':

        nombre = request.form['nombre'];
        estatus =request.form['estatus'];

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE editorial SET editorial=%s, estatus=%s WHERE id = %s ',(nombre,estatus,id,))
            cur.connection.commit()
            flash('Editorial Actualizado Correctamente', 'success')
        except:
            print('ERROR AL ACTUALIZAR')
    cur.close()
    # return jsonify({"datos":request.form});  #redirect(url_for('inicio'))
    return  redirect(url_for('libroEditoria'))

#? ELIMINAR UNA EDITORIAL
@app.route('/libro/editorial/delete/<string:id>', methods=['POST'])
def delete_editorial(id):
    if request.method == 'POST':

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE editorial SET estatus="0" WHERE id = %s ',(id,))
            cur.connection.commit()
            flash('Editorial Borrado Correctamente', 'success')
        except:
            print('ERROR DELETE')
    cur.close()

    return  redirect(url_for('libroEditoria'))
#*************************||| PAIS

#? PAGINA PRINCIPAL DEL PAIS
@app.route('/libro/pais')
def libroPais():
    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'libro')
    return render_template('pais.html',moduls=modul,rests = rest)

#? LLEVAR LOS DATOS DE UN LIBRO A LA PAGINA
@app.route('/libro/pais/data')
def libroPaisData():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pais WHERE estatus=1')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#? CREAR UN NUEVO PRINCIPAL
@app.route('/libro/pais/create',methods=['POST'] )
def libroPaisCreate():
    if request.method == 'POST':
        nombre = request.form['nombre'];
        cur = mysql.connection.cursor();
        try:
            cur.execute("INSERT INTO pais (pais, estatus) VALUES (%s,%s)",(nombre,1));
            cur.connection.commit()
            flash('Pais Añadido Correctamente', 'success')
        except:
            print('IS NOT CREATED THE PAIS')
    cur.close()
    return  redirect(url_for('libroPais'))

#? LLEVAR LOS DATOS DE UN PAIS PARA ACTUALIZAR
@app.route('/libro/pais/update/<string:id>', methods=['POST'])
def update_get_pais(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM pais WHERE id = %s ",(id,))
            data = cur.fetchall()

            flash('Pais seleccionado Correctamente', 'success')
        except:
            print('ERROR UPDATE')
    cur.close()
    return jsonify({"datos":data});

#? DATOS ACTUALIZADOS DEL PAIS
@app.route('/libro/pais/update/<string:id>/', methods=['POST'])
def update_set_pais(id):
    if request.method == 'POST':

        nombre = request.form['nombre'];
        estatus =request.form['estatus'];

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE pais SET pais=%s, estatus=%s WHERE id = %s ',(nombre,estatus,id,))
            cur.connection.commit()
            flash('Pais Actualizado Correctamente', 'success')
        except:
            print('ERROR AL ACTUALIZAR')
    cur.close()
    # return jsonify({"datos":request.form});  #redirect(url_for('inicio'))
    return  redirect(url_for('libroPais'))

#? ELIMINAR UN PAIS
@app.route('/libro/pais/delete/<string:id>', methods=['POST'])
def delete_pais(id):
    if request.method == 'POST':

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE pais SET estatus="0" WHERE id = %s ',(id,))
            cur.connection.commit()
            flash('Pais Borrado Correctamente', 'success')
        except:
            print('ERROR DELETE')
    cur.close()

    return  redirect(url_for('libroPais'))
#*************************||| CATEGORIA

#? PAGINA PRINCIPAL DE CATEGORIA
@app.route('/libro/categoria')
def libroCategoria():
    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'libro')
    return render_template('categoria.html',moduls=modul,rests = rest)

#? LLEVAR LOS DATOS DEL LIRBO A LA TABLA
@app.route('/libro/categoria/data')
def libroCategoriaData():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tipolibro WHERE estatus=1')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#? CREAR UNA NUEVA CATEGORIA
@app.route('/libro/categoria/create',methods=['POST'] )
def libroCategoriaCreate():
    if request.method == 'POST':
        nombre = request.form['nombre'];
        cur = mysql.connection.cursor();
        try:
            cur.execute("INSERT INTO tipolibro (tipo, estatus) VALUES (%s,%s)",(nombre,1));
            cur.connection.commit()
            flash('Categoria Añadido Correctamente', 'success')
        except:
            print('IS NOT CREATED THE CATEGORIA')
    cur.close()
    return  redirect(url_for('libroCategoria'))

#? LLEVAR LOS DATOS PARA ACTUALIZAR LA CATEGORIA
@app.route('/libro/categoria/update/<string:id>', methods=['POST'])
def update_get_categoria(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM tipolibro WHERE id = %s ",(id,))
            data = cur.fetchall()

            flash('Categoria seleccionado Correctamente', 'success')
        except:
            print('ERROR UPDATE')
    cur.close()
    return jsonify({"datos":data});

#? LOS DATOS ACTUALIZADOS DE LA CATEGORIA
@app.route('/libro/categoria/update/<string:id>/', methods=['POST'])
def update_set_categoria(id):
    if request.method == 'POST':

        nombre = request.form['nombre'];
        estatus =request.form['estatus'];

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE tipolibro SET tipo=%s, estatus=%s WHERE id = %s ',(nombre,estatus,id,))
            cur.connection.commit()
            flash('Categoria Actualizado Correctamente', 'success')
        except:
            print('ERROR AL ACTUALIZAR')
    cur.close()
    # return jsonify({"datos":request.form});  #redirect(url_for('inicio'))
    return  redirect(url_for('libroCategoria'))

#? ELIMINAR UNA CATEGORIA
@app.route('/libro/categoria/delete/<string:id>', methods=['POST'])
def delete_categoria(id):
    if request.method == 'POST':

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE tipolibro SET estatus="0" WHERE id = %s ',(id,))
            cur.connection.commit()
            flash('Categoria Borrado Correctamente', 'success')
        except:
            print('ERROR DELETE')
    cur.close()

    return  redirect(url_for('libroCategoria'))

#*************************||| Autor
#? PAGINA PRINCIPAL DE AUTOR
@app.route('/libro/autor')
def libroAutor():
    idUser = session.get('idUser');
    rest = restricciones(str(idUser),'libro')
    modul = modules(str(idUser))
    return render_template('autor.html',moduls=modul,rests = rest)

#? LLEVAR LOS DATOS DE AUTOR PARA LA TABLA
@app.route('/libro/autor/data')
def libroAutorData():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM autor WHERE estatus=1')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#? CREAR UN AUTOR
@app.route('/libro/autor/create',methods=['POST'] )
def libroAutorCreate():
    if request.method == 'POST':
        nombre = request.form['nombre'];
        cur = mysql.connection.cursor();
        try:
            cur.execute("INSERT INTO autor (autor, estatus) VALUES (%s,%s)",(nombre,1));
            cur.connection.commit()
            flash('Autor Añadido Correctamente', 'success')
        except:
            print('IS NOT CREATED THE AUTOR')
    cur.close()
    return  redirect(url_for('libroAutor'))

#? LLEVAR LOS DATOS DEL AUTOR PARA ACTUALIZAR
@app.route('/libro/autor/update/<string:id>', methods=['POST'])
def update_get_autor(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM autor WHERE id = %s ",(id,))
            data = cur.fetchall()

            flash('Autor seleccionado Correctamente', 'success')
        except:
            print('ERROR UPDATE')
    cur.close()
    return jsonify({"datos":data});

#? DATOS ACTUALIZADOS PARA EL AUTOR
@app.route('/libro/autor/update/<string:id>/', methods=['POST'])
def update_set_autor(id):
    if request.method == 'POST':

        nombre = request.form['nombre'];
        estatus =request.form['estatus'];

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE autor SET autor=%s, estatus=%s WHERE id = %s ',(nombre,estatus,id,))
            cur.connection.commit()
            flash('Autor Actualizado Correctamente', 'success')
        except:
            print('ERROR AL ACTUALIZAR')
    cur.close()
    # return jsonify({"datos":request.form});  #redirect(url_for('inicio'))
    return  redirect(url_for('libroAutor'))

#? ELIMINAR EL AUTOR
@app.route('/libro/autor/delete/<string:id>', methods=['POST'])
def delete_autor(id):
    if request.method == 'POST':

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE autor SET estatus="0" WHERE id = %s ',(id,))
            cur.connection.commit()
            flash('Autor Borrado Correctamente', 'success')
        except:
            print('ERROR DELETE')
    cur.close()

    return  redirect(url_for('libroAutor'))

#****************************||| Area

#? PAGINA PRINCIPAL DEL AREA
@app.route('/libro/area')
def libroArea():
    idUser = session.get('idUser');
    modul = modules(str(idUser))
    rest = restricciones(str(idUser),'libro')
    return render_template('area.html',moduls=modul,rests = rest)

#? DATOS PARA LA TABLA
@app.route('/libro/area/data')
def libroAreaData():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM area WHERE estatus=1')
    data = cur.fetchall()
    cur.close()

    return jsonify({"datos":data});

#? CREAR UNA NUEVA AREA
@app.route('/libro/area/create',methods=['POST'] )
def libroAreaCreate():
    if request.method == 'POST':
        nombre = request.form['nombre'];
        cur = mysql.connection.cursor();
        try:
            cur.execute("INSERT INTO area (area, estatus) VALUES (%s,%s)",(nombre,1));
            cur.connection.commit()
            flash('Area Añadido Correctamente', 'success')
        except:
            print('IS NOT CREATED THE AREA')
    cur.close()
    return  redirect(url_for('libroArea'))

#? LLEVAR LOS DATOS DE UNA AREA PARA ACTUALIZAR
@app.route('/libro/area/update/<string:id>', methods=['POST'])
def update_get_area(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM area WHERE id = %s ",(id,))
            data = cur.fetchall()

            flash('Area seleccionado Correctamente', 'success')
        except:
            print('ERROR UPDATE')
    cur.close()
    return jsonify({"datos":data});

#? DATOS ACTUALIZADOS DE UN AREA
@app.route('/libro/area/update/<string:id>/', methods=['POST'])
def update_set_area(id):
    if request.method == 'POST':

        nombre = request.form['nombre'];
        estatus =request.form['estatus'];

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE area SET area=%s, estatus=%s WHERE id = %s ',(nombre,estatus,id,))
            cur.connection.commit()
            flash('area Actualizado Correctamente', 'success')
        except:
            print('ERROR AL ACTUALIZAR')
    cur.close()
    # return jsonify({"datos":request.form});  #redirect(url_for('inicio'))
    return  redirect(url_for('libroArea'))

#? ELIMINAR UNA AREA
@app.route('/libro/area/delete/<string:id>', methods=['POST'])
def delete_area(id):
    if request.method == 'POST':

        cur = mysql.connection.cursor()
        try:
            cur.execute('UPDATE area SET estatus="0" WHERE id = %s ',(id,))
            cur.connection.commit()
            flash('Area Borrado Correctamente', 'success')
        except:
            print('ERROR DELETE')
    cur.close()

    return  redirect(url_for('libroArea'))

#**************************************** FUNCIONES

#? FUNCION DE SEGURIDAD PARA EL ACCESO A LOS MODULOS DEPENDE EL PERFIL
def modules(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute('SELECT modulo,icons FROM vw_modules WHERE user_id=%s',(id,))
        data = cur.fetchall()
        print(data)
        return data
    except:
        return status_404();

#? RESTRICCIONES DE CADA PERFIL
def restricciones(id,modulo):
    cur = mysql.connection.cursor()
    try:
        cur.execute('SELECT modulo,descripcion FROM vw_resticciones WHERE user_id=%s and modulo=%s',(id,modulo))
        data = cur.fetchall()
        print(data)
        return data
    except:
        return status_404();

#? SALIR DEL PROGRAMA O CERRAR SESION
@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('index'))

#? ERRORES DE ESTATUS
def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)