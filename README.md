# aliments_crud
Aliments CRUD project using Django framemwork

Este es un code challenge solicitado por HLS (cliente Aeroméxico).
Se trata de un CRUD de alimentos y bebidas desarrollado en Django.

***********
Instalación
***********

1. Clonar el repositorio
2. Ejecutar docker-compose build
3. Ejecutar docker-compose up
4. El API se ejecuta en http://localhost:8000/api/aliments/

Se generan dos contenedores:

1. Django: aplicación con el API de alimentos
2. H2: Base de datos H2 en memoria para el almacenamiento.


***********
Uso
***********

1. Listado de alimentos y bebidas.

GET http://localhost:8000/api/aliments/

2. Crear un nuevo alimento/bebida.

PUT http://localhost:8000/api/aliments/

{
    "name": "food or drink",
    "description": "this is a very good plate",
    "status": True
}

3. Actualizar un alimento/bebida.

PUT http://localhost:8000/api/aliments/1

{
    "name": "new food or drink",
    "description": "new description",
    "status": False
}

4. Eliminar un alimento/bebida.

DELETE http://localhost:8000/api/aliments/1

***********
Testing
***********

Para ejecutar los test:

docker compose exec django python manage.py test

***********
Estructura
***********

Se usó una arquitectura hexagonal para el desarrollo de la API.
Ya que Django no tiene un driver nativo para H2, se usó un patrón de diseño repositorio para la comunicación con esta base de datos.

Módulos principales:

* domain/aliment.py
Contiene la clase Aliment que es la entidad principal del sistema.

* domain/aliment_repository.py
Contiene la clase abstracta AlimentRepository que define el acceso y almacenamiento de la entidad Aliment.

* api/adapters/h2_aliment_repository.py
Contiene la clase H2AlimentRepository que implementa la clase abstracta (interfaz) AlimentRepository para implementar el acceso a través de una BD H2 en memoria.

* api/serializer.py
Contiene la clase AlimentSerializer que usan los controllers para serializer/deserializar la data del API.

* api/views.py
Contiene los controllers que responden a las acciones de la API.
La clase ListCreateAlimentView que gestiona el listado y creación de alimentos.
La clase RetrieveUpdateDeleteAlimentView que gestiona el detalle, actualización y borrado de alimentos.

***********
Notas
***********

1. Se usó el término en inglés "aliments" ya que este término se puede referir tanto a un alimento como a una bebida.
2. Por simplicidad, la API no responde al verbo POST, solo al PUT.
3. Por simplicidad, no se añadió autenticación.