from models import db, User, Character, Planet
from app import app

with app.app_context():
    # Limpiar tablas
    Character.query.delete()
    Planet.query.delete()
    User.query.delete()
    db.session.commit()

    # Crear usuario
    user = User(
        email="test@example.com",
        password="123456",
        is_active=True,
        username="testuser",
        firstname="Luke",
        lastname="Skywalker"
    )
    db.session.add(user)

    # Crear personajes
    luke = Character(
        name="Luke Skywalker",
        gender="male",
        birth_year="19BBY",
        eye_color="blue"
    )
    leia = Character(
        name="Leia Organa",
        gender="female",
        birth_year="19BBY",
        eye_color="brown"
    )
    db.session.add(luke)
    db.session.add(leia)

    # Crear planetas (población dentro del rango válido para Integer)
    tatooine = Planet(
        name="Tatooine",
        climate="arid",
        terrain="desert",
        population=200000
    )
    naboo = Planet(
        name="Naboo",
        climate="temperate",
        terrain="grassy hills, swamps, forests, mountains",
        population=2000000000  # corregido para evitar "integer out of range"
    )
    db.session.add(tatooine)
    db.session.add(naboo)

    # Guardar cambios
    db.session.commit()

    print("✅ Base de datos poblada con éxito.")