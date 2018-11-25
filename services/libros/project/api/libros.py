from flask import Blueprint, jsonify, request, render_template
from project.api.models import Libro
from project import db
from sqlalchemy import exc


libros_blueprint = Blueprint('libros', __name__, template_folder='./templates')


@libros_blueprint.route('/libro/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'exito',
        'mensaje': 'probando!!!'
    })


@libros_blueprint.route('/libros', methods=['POST'])
def add_libros():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    categoria = post_data.get('categoria')
    costo = post_data.get('costo')
    autor = post_data.get('autor')
    descripcion = post_data.get('descripcion')
    try:
        libro = Libro.query.filter_by(nombre=nombre).first()
        if not libro:
            db.session.add(Libro(nombre=nombre,
                                 categoria=categoria,
                                 costo=costo,
                                 autor=autor,
                                 descripcion=descripcion))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{nombre} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'Este libro ya esta registrado.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@libros_blueprint.route('/libro/<user_id>', methods=['GET'])
def get_single_libros(user_id):
    """Obteniendo detalles de un unico libro"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Libro no existe'
    }

    try:
        libro = Libro.query.filter_by(id=int(user_id)).first()
        if not libro:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': libro.id,
                    'nombre': libro.nombre,
                    'categoria': libro.categoria,
                    'costo': libro.costo,
                    'descripcion': libro.descripcion,
                    'autor': libro.autor
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@libros_blueprint.route('/libros', methods=['GET'])
def get_all_libros():
    """Todos los libros"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'libros': [libro.to_json() for libro in Libro.query.all()]
        }
    }
    return jsonify(response_object), 200


@libros_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        costo = request.form['costo']
        categoria = request.form['categoria']
        autor = request.form['autor']

        if not nombre:
            print("no hay data de libro")
        if not categoria:
            print("no hay categoria")
        if not autor:
            print("no hay autor")
        if not costo:
            print("no hay costo")
        if not descripcion:
            print("no hay descripcion")
        else:
            print("se registro correctamente")
            db.session.add(Libro(nombre=nombre,
                                 descripcion=descripcion,
                                 costo=costo,
                                 categoria=categoria,
                                 autor=autor))
            db.session.commit()
    libro = Libro.query.all()
    return render_template('index.html', libros=libro)
