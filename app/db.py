import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime


from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float,text
from sqlalchemy.orm import declarative_base
from sqlalchemy import func

from sqlalchemy.orm import relationship, sessionmaker


DATABASE_URL = "postgresql://admin:rajarabii1@db:5432/immobilier_db"

engine = create_engine(DATABASE_URL)


Session = sessionmaker(bind=engine)
session = Session()

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.fetchone())  

Base = declarative_base()


class Annonce(Base):
    __tablename__ = 'annonces'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    datetime = Column(DateTime)
    nb_rooms = Column(Integer)
    nb_baths = Column(Integer)
    surface_area = Column(Float)
    link = Column(String)
    city_id = Column(Integer, ForeignKey('villes.id'))

    ville = relationship("Ville", back_populates="annonces")
    equipements = relationship("AnnonceEquipement", back_populates="annonce")


class Ville(Base):
    __tablename__ = 'villes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float, nullable=True)  # Nouvelle colonne pour la latitude
    longitude = Column(Float, nullable=True)
    
    
    annonces = relationship("Annonce", back_populates="ville")


class Equipement(Base):
    __tablename__ = 'equipements'

    id = Column(Integer, primary_key=True)
    name = Column(String)  

    annonces = relationship('AnnonceEquipement', back_populates='equipement')


class AnnonceEquipement(Base):
    __tablename__ = 'annonce_equipement'

    annonce_id = Column(Integer, ForeignKey('annonces.id'), primary_key=True)
    equipement_id = Column(Integer, ForeignKey('equipements.id'), primary_key=True)

    annonce = relationship('Annonce', back_populates='equipements')
    equipement = relationship('Equipement', back_populates='annonces')



#df_orm = load_data("SELECT  a.id AS annonce_id, a.title, a.price, a.datetime, a.nb_rooms, a.nb_baths,   a.surface_area,  v.name,v.longitude,v.latitude FROM annonces a join villes v on a.city_id=v.id")
df_orm = session.query(Annonce.id,Annonce.title,Annonce.price,Annonce.datetime,Annonce.nb_rooms,Annonce.nb_baths,Annonce.surface_area,Ville.name,Ville.longitude,Ville.latitude).join(Ville,Annonce.city_id==Ville.id).all()



df_orm_equipement = session.query(
    Equipement.name.label('equipement'),  # Sélectionne le nom de l'équipement
    func.count(func.distinct(AnnonceEquipement.annonce_id)).label('nombre_annonces')  # Compte le nombre distinct d'annonces
).join(
    AnnonceEquipement, Equipement.id == AnnonceEquipement.equipement_id  # Jointure avec la table annonce_equipement
).join(
    Annonce, AnnonceEquipement.annonce_id == Annonce.id  # Jointure avec la table annonces
).group_by(
    Equipement.name  # Grouper par le nom de l'équipement
).order_by(
    func.count(func.distinct(AnnonceEquipement.annonce_id)).desc()  # Trier par le nombre d'annonces
).all()