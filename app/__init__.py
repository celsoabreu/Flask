''' 
#-------------------------------------------------------------------------------
# Name:        __init__.py
# Purpose:
#
# Author:      Celso Abreu
#
# Created:     12/03/2023
# Copyright:   (c) CA_ON 2023
# Licence:     <your licence>
#------------------------------------------------------------------------------- 
#!/usr/bin/env python   '''
from flask import Flask

from database import db
# Manager sera o nosso controlador de comando, ele ja possue varios comndos internos Gerenciador de comandos
#from flask_script import Manager  
# Migrate será que executara e fornecerá os comandos de Migração 
from flask_migrate import Migrate

#from flask_login import LoginManager


# Importar o arquivo bpusuarios.py 
from bpusuarios import bp_usuarios


app = Flask(__name__)

# Direcionamos o config 
app.config.from_object('config')

#db = SQLALchemy(app)

#Implementação da rota do arquivo Blueprint
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')


#login_manager = LoginManager(app)

db.init_app(app)

# Instanciando Migrate passando a aplicação e banco de dados
migrate = Migrate(app, db)
# Ira cuidar dos comandos que usaremos para inicializar a nossa aplicação, o primeiro deles é: Python runserver
#manager = Manager(app)






# Com esta linha ja passamos o comando DB junto com o MigrateCommand pois a lib ja possue um conjunto de comandos 
# de gerenciamento encapsulado nele.
#manager.add_command('db', MigrateCommand)

# Com isso estaremos alterando a linha de execução no arquivo (aplicação) drv_on.py
# Ao invez de : from app import app
# Será : from app import manager
# ao invez de : app.run(host='0.0.0.0', port = port)
# Será: manager.run(host='0.0.0.0', port = port)



from app.controllers import routes


