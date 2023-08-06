'''
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
#!/usr/bin/env python  '''

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
engine = create_engine("sqlite:///cadb.sqlite")

#from sqlalchemy.orm import sessionmaker
#Session = sessionmaker(bind=engine)
#session = Session()

db = SQLAlchemy()

# Configuração de conexao para execução de comandos SQL
import sqlite3

conn = None
try:
	conn = sqlite3.connect('./instance/cadb.sqlite')
except sqlite3.Error as e:
	print("Ops... Deu um erro iniciando a conexao:", e)
sql = conn.cursor()

if conn:
	print( conn , 'Conexao efetuada com sucesso!')
	result = sql.execute('''SELECT * FROM causuarios''')
	for row in result:
		print ("ID = ", row[0], "NAME = ", row[1], "Primeiro Nome = ", row[2], "Ultimo Nome = ", row[3])
	print ("Operation done successfully")
	conn.close()
else:
	print(conn, "Nao conectado!")	


