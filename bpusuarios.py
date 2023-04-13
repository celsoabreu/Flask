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

from flask import Flask, render_template, request, redirect
from flask import Blueprint
from datetime import date
from datetime import datetime
from app.models.tabels import Usuario
from database import db
from Cpf_cnpj import Cpf_cnpj

data_atual = date.today()
data_em_texto = data_atual.strftime('%d/%m/%Y')
dt_ini = data_atual.strftime('%d/%m/%Y')
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
duracao = data_e_hora_atuais.strftime('%d/%m/%Y')

bp_usuarios = Blueprint("usuarios", __name__, template_folder="app/templates") 

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
	msg = {}
	if request.method=='GET':
		return render_template('cad_user.html', msg=msg)
	
	if request.method=='POST':
		vnome    = request.form.get('nome')
		vuser    = request.form.get('user')
		vemail   = request.form.get('email')
		vcelular = request.form.get('celular')
		vcpf     = request.form.get('cpf')
		obj_cpf = Cpf_cnpj(vcpf)
		print(obj_cpf)	
		vdt_nasc = request.form.get('dt_nasc')
		vdt_ini  = dt_ini
		vduracao = duracao
		vsenha   = request.form.get('senha')
		vcsenha  = request.form.get('csenha')
		if obj_cpf == 'nok':
			msg['msg'] = 'CPF Invalido !!!'
			msg['class'] = 'alert-danger'
		else:
			msg['msg'] = 'CPF Valido !!!'
			msg['class'] = 'alert-success'
			i = Usuario(vnome, vuser, vemail, vcelular, vcpf, vdt_nasc, vdt_ini, vduracao, vsenha, vcsenha)
			db.session.add(i)
			db.session.commit()
		return redirect('/usuarios/lst_usu')

#	return '''  <html>
#    <head><title>Hello Flask</title></head>
#    <body>
#        ''' +  vnome     + ''' '<br>' 
#        ''' +  vuser     + ''' '<br>'
#        ''' +  vemail    + ''' '<br>'
#        ''' +  vcelular  + ''' '<br>'
#        ''' +  vcpf      + ''' '<br>'
#        ''' +  vdt_nasc  + ''' '<br>'
#        ''' +  vdt_ini   + ''' '<br>'
#	     ''' +  vduracao  + ''' '<br>'
#        ''' +  vsenha    + ''' '<br>'
#        ''' +  vcsenha   + '''
#    </body>
# </html> '''      

@bp_usuarios.route('/lst_usu')
def lst_usu():
	db = Usuario.query.all()
	return render_template('lst_user.html', db=db)

@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	msg = {}
	dt = Usuario.query.get(id)
	#dt = Usuario.query.filter_by(id=id).first()
	if request.method == 'GET':
		return render_template('cad_user.html', dt=dt, msg=msg)
		
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			vnome    = request.form.get('nome')
			vuser    = request.form.get('user')
			vemail   = request.form.get('email')
			vcelular = request.form.get('celular')
			vcpf     = request.form.get('cpf')
			obj_cpf = Cpf_cnpj(vcpf)
			print(obj_cpf)
			vdt_nasc = request.form.get('dt_nasc')
			vdt_ini  = dt_ini
			vduracao = duracao
			vsenha   = request.form.get('senha')
			vcsenha  = request.form.get('csenha')
			if obj_cpf == 'nok':
				msg['msg'] = 'CPF Invalido !!!'
				msg['class'] = 'alert-danger'
			else:
				u = Usuario(nome=vnome, user=vuser, email=vemail, celular=vcelular, cpf=vcpf, dt_nasc=vdt_nasc, dt_ini=vdt_ini, duracao=vduracao, senha=vsenha, csenha=vcsenha)
				#db.session.execute(f" UPDATE Usuario SET nome='{vnome}', user='{vuser}', celular='{vcelular}', dt_nasc='{vdt_nasc}', dt_ini='{vdt_ini}', duracao='{vduracao}' WHERE id='{id}' ")
				db.session.add(u)
				db.session.commit()
				return redirect('/usuarios/lst_usu')
		else:
			return HTTPResponse('Usuario nao Encontrado!')


@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	msg = {}
	d = Usuario.query.get(id)
	if request.method == 'POST':
		if d:
			db.session.delete(d)
			db.session.commit()
			return redirect('/usuarios/lst_usu')
	#	abort(404)
	return render_template('confElimina.html')






