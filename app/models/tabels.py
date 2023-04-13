# models.py
#-------------------------------------------------------------------------------
# Name:        Drv_on.py
# Purpose:
#
# Author:      Celso Abreu
#
# Created:     12/03/2023
# Copyright:   (c) CA_ON 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from database import db

from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
	__tablename__="usuarios"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	nome = db.Column(db.String(100))
	user = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(100), unique=True)
	celular = db.Column(db.String(100))
	cpf = db.Column(db.String(100), unique=True)
	dt_nasc = db.Column(db.String(100))
	dt_ini = db.Column(db.String(100))
	duracao = db.Column(db.String(100))
	senha = db.Column(db.String(100))
	csenha = db.Column(db.String(100))

#Toda classe tem um construtor nesse caso sera o __init__
	def __init__(self, nome, user, email, celular, cpf, dt_nasc, dt_ini, duracao, senha, csenha ):
		self.nome = nome
		self.user = user 
		self.email = email
		self.celular = celular
		self.cpf = cpf
		self.dt_nasc = dt_nasc 
		self.dt_ini = dt_ini 
		self.duracao = duracao
		self.senha = generate_password_hash(senha) 
		self.csenha = generate_password_hash(csenha) 

def verify_senha(self, senha):
	return check_password_hash(self.senha, senha)

#Definimos o metodo que representa o objeto de uma classe
	def __repr__(self):
		return "<Usuario %r>" % self.nome 

# Tabela de posts
class Post(db.Model):
	__tablename__= "posts"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	id_usu = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
	content = db.Column(db.Text())
	
	usu = db.relationship('Usuario', foreign_keys=id_usu)
	
	def __init__(self, content, id_user):
		self.id_usu = id_usu 
		self.content = content

	def __repr__(self):
		return "<Post %r>" % self.id 

# tabela de Seguidores
class Follow(db.Model):
	__tablename__="follows"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	id_usu = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
	id_foll = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

	r_usu = db.relationship('Usuario', foreign_keys=id_usu)
	r_foll = db.relationship('Usuario', foreign_keys=id_foll)

	def __init__(self, id_usu, id_foll):
		self.id_usu = id_usu 
		self.id_foll = id_foll

	def __repr__(self):
		return "<Follow %r>" % self.id 

# Tabela projeto API REST
class BookModel(db.Model):
    __tablename__ = 'books'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer())
    author = db.Column(db.String(80))
 
    def __init__(self, name, price, author):
        self.name = name
        self.price = price
        self.author = author 
     
    def json(self):
        return {"name":self.name, "price":self.price, "author":self.author}
