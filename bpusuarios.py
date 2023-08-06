#-------------------------------------------------------------------------------
# Name:        bpusuarios.py
# Purpose:
#
# Author:      Celso Abreu
#
# Created:     12/03/2023
# Copyright:   (c) CA_ON 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from flask import Flask, Response, url_for, render_template, \
request, redirect, flash, session, abort, g
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from datetime import timedelta
                                
from flask import Blueprint
from datetime import date
from datetime import datetime
from app.models.tabels import CaUsuario, CaModulo, CaRotina, CaAplic
from werkzeug.security import generate_password_hash, check_password_hash

from database import db, conn, sql, sqlite3

from Val_cpf import validate


data_atual = date.today()
data_em_texto = data_atual.strftime('%d/%m/%Y')
dt_ini = data_atual.strftime('%d/%m/%Y')
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
duracao = data_e_hora_atuais.strftime('%d/%m/%Y')

bp_usuarios = Blueprint("usuarios", __name__, template_folder="app/templates", static_url_path='assets') 

@bp_usuarios.route('/create', methods=['GET', 'POST'])

def create():
	msg = {}
	db = CaUsuario.query.all() 
	if request.method=='GET':
		return render_template('usu/cad_user.html', msg=msg)
	
	if request.method=='POST':
		vnome    	= request.form.get('nome')
		vfirst_name = request.form.get('first_name')
		vlast_name 	= request.form.get('last_name')
		vuser    	= request.form.get('user')
		vemail   	= request.form.get('email')
		vcelular 	= request.form.get('celular')
		vcpf     	= request.form.get('cpf')
		obj_cpf 	= validate(vcpf)
		print(obj_cpf)	
		vdt_nasc 	= request.form.get('dt_nasc')
		vdt_ini  	= dt_ini
		vstatus  	= 'A'
		vduracao 	= duracao
		vcreated_datetime = data_e_hora_atuais
		vfoto 		= request.form.get('foto')
		vsenha   	= request.form.get('senha')
		vcsenha  	= request.form.get('csenha')
		if obj_cpf == False:
			msg['msg'] = 'CPF Invalido !!!'
			msg['class'] = 'alert-danger'
			return render_template('usu/cad_user.html', msg=msg)
		else:
			conn = sqlite3.connect('./instance/cadb.sqlite')
			sql = conn.cursor()
			sql.execute('INSERT into causuarios(nome, first_name, last_name, user, email, celular, cpf, dt_nasc, dt_ini, status, duracao, created_datetime, foto, senha, csenha) VALUES  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (vnome, vfirst_name, vlast_name, vuser, vemail, vcelular, vcpf, vdt_nasc, vdt_ini, vstatus, duracao, vcreated_datetime, vfoto, vsenha, vcsenha))
			conn.commit()
			conn.close()
			return redirect('/usuarios/lst_usu')

#			return '''  
#				<html>
#				    <head><title>Hello Flask</title></head>
#				    <body>
#				        ''' +  vnome     + ''' '<br>' 
#				    	''' +  vfirst_name  + ''' '<br>'
#				    	''' +  vlast_name  + ''' '<br>'
#				        ''' +  vuser     + ''' '<br>'
#				        ''' +  vemail    + ''' '<br>'
#				        ''' +  vcelular  + ''' '<br>'
#				        ''' +  vcpf      + ''' '<br>'
#				        ''' +  vdt_nasc  + ''' '<br>'
#				        ''' +  vdt_ini   + ''' '<br>'
#					    ''' +  vduracao  + ''' '<br>'
#					    ''' +  str(vstatus)   + ''' '<br>'
#				        ''' +  vsenha    + ''' '<br>'
#				        ''' +  vcsenha   + '''
#				    </body>
#				</html> '''
      

@bp_usuarios.route('/lst_usu/<int:id>/', methods=['GET', 'POST'])
@bp_usuarios.route('/lst_usu', defaults={'id': None}, methods=['GET', 'POST'])
#@bp_usuarios.route('/lst_usu/<int:id>/', methods=['GET', 'POST'])

def lst_usu(id):
	db = {}
	msg = {} 
	pesq = request.form.get('pesq')
	if pesq: #CaUsuario.query.filter(CaUsuario.nome.like('%pesq%') )
		db = CaUsuario.query.filter(CaUsuario.first_name.ilike(pesq))
	else:	
		db = CaUsuario.query.all()
	return render_template('usu/lst_user.html', db=db, msg=msg)

@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	msg = {}
	dt = CaUsuario.query.get(id)
	#dt = Usuario.query.filter_by(id=id).first()
	if request.method == 'GET':
		return render_template('usu/cad_user.html', dt=dt, msg=msg)
		
	if request.method == 'POST':
		if dt:
#			db.session.delete(dt)
#			db.session.commit()
			vnome    = request.form.get('nome')
			vfirst_name = request.form.get('first_name')
			vlast_name = request.form.get('last_name')			
			vuser    = request.form.get('user')
			vemail   = request.form.get('email')
			vcelular = request.form.get('celular')
			vcpf     = request.form.get('cpf')
			obj_cpf = validate(vcpf)
			print(obj_cpf)
			vdt_nasc = request.form.get('dt_nasc')
			vdt_ini  = dt_ini
			vstatus  = True  #request.form.get('status')
			vduracao = duracao
			vcreated_datetime = data_e_hora_atuais
			vfoto  = request.form.get('foto')
			vsenha   = request.form.get('senha')
			vcsenha  = request.form.get('csenha')
			if obj_cpf == False:
				msg['msg'] = 'CPF Invalido !!!'
				msg['class'] = 'alert-danger'
				return render_template('usu/cad_user.html', dt=dt, msg=msg)
			else:
				conn = sqlite3.connect('./instance/cadb.sqlite')
				sql = conn.cursor()
				query = 'UPDATE causuarios SET nome = ?, first_name = ?, last_name = ?, user = ?, email = ?, celular = ?, cpf = ?, dt_nasc = ?, dt_ini = ?, status = ?, duracao = ?, created_datetime = ?, foto = ?, senha = ?, csenha = ? where id = ? '
				columnValues = (vnome, vfirst_name, vlast_name, vuser, vemail, vcelular, vcpf, vdt_nasc, vdt_ini, vstatus, duracao, vcreated_datetime, vfoto, vsenha, vcsenha, id)
				sql.execute(query, columnValues)
				conn.commit()
				conn.close()
				return redirect('/usuarios/lst_usu')				
		else:
			msg['msg'] = 'Usuario nao encontrado !!!'
			msg['class'] = 'alert-danger'
			return render_template('usu/cad_user.html', dt=dt, msg=msg)

@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	msg = {}
	dt = {}
	db = CaUsuario.query.get(id)
	if request.method == 'POST':
		if db:
			conn = sqlite3.connect('./instance/cadb.sqlite')
			sql = conn.cursor()
			query = 'DELETE FROM usuarios where id = ?', id
			sql.execute(query)
			conn.commit()
			conn.close()
			return redirect('/usuarios/lst_usu')
#		abort(404)
	






