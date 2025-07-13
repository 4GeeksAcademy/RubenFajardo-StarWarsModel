from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    Subscription_date: Mapped[str] = mapped_column(String(120), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            'full_name': self.full_name,
            "email": self.email,
        }

class Favorite(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    usuario: Mapped["User"] = relationship(back_populates="favorites")

    planets: Mapped[List["Planet"]] = relationship(secondary="favorite_planet", back_populates="favorites")
    characters: Mapped[List["Character"]] = relationship(secondary="favorite_character", back_populates="favorites")


class Planet(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    population: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    gravity: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(120), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(secondary="favorite_planet", back_populates="planets")

    def serialize(self):
        return {
            "id": self.id,
            "population": self.population,
            'climate': self.climate,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period
        }

class Character(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    height: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
    mass: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(secondary="favorite_character", back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "height": self.height,
            'eye_color': self.eye_color,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "gender": self.gender
        }
    
favorite_planet = Table(
    "favorite_planet",
    db.metadata,
    Column("favorite_id", ForeignKey("favorite.id")),
    Column("planet_id", ForeignKey("planet.id"))
)

favorite_character = Table(
    "favorite_character",
    db.metadata,
    Column("favorite_id", ForeignKey("favorite.id")),
    Column("character_id", ForeignKey("character.id"))
)