from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))

    # Relaciones
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    followers: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")
    following: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")

    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="user")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    post: Mapped["Post"] = relationship("Post", back_populates="media")

class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class Follower(db.Model):
    __tablename__ = "follower"

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    follower: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

# Modelos de Star Wars

class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(20))

    favorites: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="character")

class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[int] = mapped_column()

    favorites: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="planet")

class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorite_characters")
    character: Mapped["Character"] = relationship("Character", back_populates="favorites")

class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorites")