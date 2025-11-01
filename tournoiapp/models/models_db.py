from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from tournoiapp import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JoueurDB(db.Model):
    __tablename__ = 'joueurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    niveau = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Joueur {self.nom} ({self.niveau})>"


class TournoiDB(db.Model):
    __tablename__ = 'tournois'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<Tournoi {self.nom}>"
