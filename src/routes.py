from flask import Blueprint, jsonify, request
from models import db, Character, Planet, FavoriteCharacter, FavoritePlanet, User

api = Blueprint('api', __name__)

# ----------------------------------------
# GET /people - Listar todos los personajes
# ----------------------------------------
@api.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([
        {
            "id": person.id,
            "name": person.name,
            "gender": person.gender,
            "birth_year": person.birth_year,
            "eye_color": person.eye_color
        } for person in people
    ]), 200

# ----------------------------------------
# GET /people/<id> - Personaje por ID
# ----------------------------------------
@api.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify({
        "id": person.id,
        "name": person.name,
        "gender": person.gender,
        "birth_year": person.birth_year,
        "eye_color": person.eye_color
    }), 200

# ----------------------------------------
# GET /planets - Listar todos los planetas
# ----------------------------------------
@api.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([
        {
            "id": planet.id,
            "name": planet.name,
            "climate": planet.climate,
            "terrain": planet.terrain,
            "population": planet.population
        } for planet in planets
    ]), 200

# ----------------------------------------
# GET /planets/<id> - Planeta por ID
# ----------------------------------------
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify({
        "id": planet.id,
        "name": planet.name,
        "climate": planet.climate,
        "terrain": planet.terrain,
        "population": planet.population
    }), 200

# ----------------------------------------
# GET /users - Listar todos los usuarios
# ----------------------------------------
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# ----------------------------------------
# GET /users/favorites - Favoritos del usuario actual (simulado como ID=1)
# ----------------------------------------
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(1)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorites = []

    for fav in user.favorite_characters:
        favorites.append({
            "type": "character",
            "name": fav.character.name
        })

    for fav in user.favorite_planets:
        favorites.append({
            "type": "planet",
            "name": fav.planet.name
        })

    return jsonify(favorites), 200

# ----------------------------------------
# POST /favorite/planet/<planet_id> - Añadir planeta favorito
# ----------------------------------------
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.get(1)
    if not Planet.query.get(planet_id):
        return jsonify({"msg": "Planet not found"}), 404

    fav = FavoritePlanet(user_id=user.id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 201

# ----------------------------------------
# POST /favorite/people/<people_id> - Añadir personaje favorito
# ----------------------------------------
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user = User.query.get(1)
    if not Character.query.get(people_id):
        return jsonify({"msg": "Character not found"}), 404

    fav = FavoriteCharacter(user_id=user.id, character_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Character added to favorites"}), 201

# ----------------------------------------
# DELETE /favorite/planet/<planet_id> - Eliminar planeta favorito
# ----------------------------------------
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user = User.query.get(1)
    fav = FavoritePlanet.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

# ----------------------------------------
# DELETE /favorite/people/<people_id> - Eliminar personaje favorito
# ----------------------------------------
@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user = User.query.get(1)
    fav = FavoriteCharacter.query.filter_by(user_id=user.id, character_id=people_id).first()
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted"}), 200