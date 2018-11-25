# services/users/project/tests/test_users.py

from project import db
from project.api.models import Libro

import json
import unittest

from project.tests.base import BaseTestCase


def add_libro(nombre, descripcion, costo, categoria, autor):
    libro = Libro(nombre=nombre,
                  descripcion=descripcion,
                  costo=costo,
                  categoria=categoria,
                  autor=autor)
    db.session.add(libro)
    db.session.commit()
    return libro


class TestLibroService(BaseTestCase):
    """Prueba para el servicio de libros."""

    def test_libros(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/libro/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('probando!!!', data['mensaje'])
        self.assertIn('exito', data['estado'])

    def test_add_libro(self):
        """Asegurando de que se pueda agregar un nuevo registro a la base de
        datos."""
        with self.client:
            response = self.client.post(
                '/libros',
                  data=json.dumps({
                    'nombre': 'los amantes son dementes',
                    'categoria': 'terror',
                    'costo': '20',
                    'autor': 'gabo',
                    'descripcion': 'desc1'
                                 }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('los amantes son dementes ha sido agregado!',
                          data['mensaje']
                          )
            self.assertIn('satisfactorio', data['estado'])

    def test_add_libro_invalid_json(self):
        """Asegurando de que se arroje un error si el objeto json esta
        vacio."""
        with self.client:
            response = self.client.post(
                '/libros',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_libro_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene
        un key de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/libros',
                data=json.dumps({'nombre': 'los amantes son dementes'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_libro_duplicate_libro(self):
        """Asegurando de que se produce un error si el nombre del libro ya
        existe."""
        with self.client:
            self.client.post(
                '/libros',
                data=json.dumps({
                    'nombre': 'los amantes son dementes',
                    'categoria': 'terror',
                    'costo': '20',
                    'autor': 'gabo',
                    'descripcion': 'desc1'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/libros',
                data=json.dumps({
                    'nombre': 'los amantes son dementes',
                    'categoria': 'terror',
                    'costo': '20',
                    'autor': 'gabo',
                    'descripcion': 'desc1'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Este libro ya esta registrado.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_libro(self):
        """Asegurando de que el primer registro individual se comporte
        correctamente."""
        libros = add_libro('los amantes son dementes',
                           'terror', '20', 'gabo', 'desc1')
        with self.client:
            response = self.client.get(f'/libro/{libros.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('los amantes son dementes', data['data']['nombre'])
            self.assertIn('20', data['data']['costo'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_libro_no_id(self):
        """Asegurando de que se lanze un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/libro/sss')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Libro no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_libro_incorrect_id(self):
        """Asegurando de que se lanze un error si el id no existe."""
        with self.client:
            response = self.client.get('/libro/sss')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Libro no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_vista_con_registros(self):
        """Probamos la vista"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro de libros', response.data)
        self.assertIn(b'<p>No hay libros registrados!</p>', response.data)

    def test_vista_sin_registros(self):
        """Asegurandose de que la vista se comporte
           correctamente cuando ingresamos datos."""
        add_libro('los amantes son dementes',
                  'terror', '20', 'gabo', 'desc1')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Registro de libros', response.data)
            self.assertNotIn(b'<p>No hay libros registrados!</p>',
                             response.data)
            self.assertIn(b'los amantes son dementes', response.data)

    def test_vista_add_libros(self):
        """Aseguramos que un nuevo libro puede
           ser añadido a la base de datos."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(nombre='los amantes son dementes',
                          categoria="terror",
                          costo="20",
                          autor="gabo",
                          descripcion="desc1"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Registro de libros', response.data)
            self.assertNotIn(b'<p>No hay libros registrados!</p>',
                             response.data)
            self.assertIn(b'los amantes son dementes', response.data)


if __name__ == '__main__':
    unittest.main()
