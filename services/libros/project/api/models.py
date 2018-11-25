from sqlalchemy.sql import func

from project import db


class Libro(db.Model):

    __tablename__ = 'libros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    categoria = db.Column(db.String(128), nullable=False)
    costo = db.Column(db.String(128), nullable=False)
    autor = db.Column(db.String(128), nullable=False)
    descripcion = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'costo': self.costo,
            'autor': self.autor,
            'descripcion': self.descripcion,
            'active': self.active
        }

    def __init__(self, nombre, categoria, costo, autor, descripcion):
        self.nombre = nombre
        self.categoria = categoria
        self.costo = costo
        self.autor = autor
        self.descripcion = descripcion
