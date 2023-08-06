#-------------------------------------------------------------------------------
# Name:        bpadm.py
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
from flask import Blueprint

from datetime import date, datetime, timedelta

from app.models.tabels import CaUsuario, CaModulo, CaRotina, CaAplic, CaParam, CaAdress, \
CaCustomer, CaProduct, CaCategory, CaFornec, CaSupply, CaSale, CaItem, CaPayment, CaGrpemp, CaEmpresa, \
CaCentro, CaDeposito, CaPdv, CaPedserv, CaTpserv

from database import db

import tkinter as tk
import tkinter.messagebox as tkmsg


data_atual = date.today()
data_em_texto = data_atual.strftime('%d/%m/%Y')
dt_ini = data_atual.strftime('%d/%m/%Y')
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
duracao = data_e_hora_atuais.strftime('%d/%m/%Y')

bp_adm = Blueprint("adm", __name__, template_folder="app/templates", static_url_path='assets') 

@bp_adm.route('/c_mod', methods=['GET', 'POST'])
@login_required
def c_mod():
	msg = {}
	if request.method=='GET':
		return render_template('adm/cad_mod.html', msg=msg)
	
	if request.method=='POST':
		vmodulo    = request.form.get('modulo')
		if vmodulo:
			i = CaModulo(modulo=vmodulo)
			db.session.add(i)
			db.session.commit()
			return redirect('/adm/l_mod')
		else:
			msg['msg'] = 'CPF Invalido !!!'
			msg['class'] = 'alert-danger'
			return render_template('adm/cad_mod.html', msg=msg)

#			return '''  
#				<html>
#				    <head><title>Hello Flask</title></head>
#				    <body>
#				   		''' +  vuser     + ''' '<br>'
#				    </body>
#				</html> '''


@bp_adm.route('/l_mod/<int:id>', methods=['GET', 'POST'])
@bp_adm.route('/l_mod', defaults={'id': None}, methods=['GET', 'POST'])
@login_required
def l_mod(id):
	db = {}
	msg = {} 
	pesq = request.form.get('pesq')
	print(pesq)
	if pesq: #CaUsuario.query.filter(nome==pesq)
		db = CaModulo.query.filter(CaModulo.modulo.ilike(pesq))
	else:	
		db = CaModulo.query.all()
	return render_template('adm/lst_mod.html', db=db, msg=msg)

@bp_adm.route('/u_mod/<int:id>', methods=['GET', 'POST'])
@login_required
def u_mod(id):
	msg = {}
	dt = CaModulo.query.get(id)
	vid = id
	#dt = CaModulo.query.filter_by(id_mod=id).first()
	if request.method == 'GET':
		return render_template('adm/cad_mod.html', dt=dt, msg=msg)
		
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			vmodulo = request.form.get('modulo')
			u = CaModulo(id_mod=vid, modulo=vmodulo)
			#db.session.execute(f" UPDATE Usuario SET nome='{vnome}', user='{vuser}', celular='{vcelular}', dt_nasc='{vdt_nasc}', dt_ini='{vdt_ini}', duracao='{vduracao}' WHERE id='{id}' ")
			db.session.add(u)
			db.session.commit()
			return redirect('/adm/l_mod')
		else:
			return HTTPResponse('Usuario nao Encontrado!')


@bp_adm.route('/d_mod/<int:id>', methods=['GET', 'POST'])
@login_required
def d_mod(id):
	msg = {}
	d = CaModulo.query.get(id)
	if request.method == 'POST':
		if d:
			db.session.delete(d)
			db.session.commit()
			return redirect('/adm/l_mod')
	#	abort(404)
	return render_template('confElimina.html', msg=msg)


@bp_adm.route('/c_rot', methods=['GET', 'POST'])
@login_required
def c_rot():
	msg = {}
	tb = CaModulo.query.all()
	dt = {}
	if request.method=='GET':
		return render_template('adm/cad_rot.html', tb=tb, dt=dt, msg=msg)
	
	if request.method=='POST':
		vid_mod = request.form.get('id_mod')
		vrotina = request.form.get('rotina')
		i = CaRotina(id_mod=int(vid_mod),rotina=vrotina)
		if i:
			print(vid_mod, vrotina)
			db.session.add(i)
			db.session.commit()
			return redirect('/adm/l_rot')
		else:
			msg['msg'] = 'Rotina nao cadastrada !!!'
			msg['class'] = 'alert-danger'
			return render_template('adm/cad_rot.html', tb=tb, dt=dt, msg=msg)

#			return '''  
#				<html>
#				    <head><title>Hello Flask</title></head>
#				    <body>
#				   		''' +  vuser     + ''' '<br>'
#				    </body>
#				</html> '''


@bp_adm.route('/u_rot/<int:id>', methods=['GET', 'POST'])
@login_required
def u_rot(id):
	msg = {}
	dt = CaRotina.query.get(id)
	vid_rot = dt.id_rot
	tb = CaModulo.query.filter_by(id_mod=dt.id_mod).first()
	vid_mod = tb.id_mod
	if request.method == 'GET':
		return render_template('adm/cad_rot.html', tb=tb, dt=dt, msg=msg)
		
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			vid_mod = request.form.get('id_mod')
			vrotina = request.form.get('rotina')
			u = CaRotina(vid_rot, vid_mod, vrotina)
			#db.session.execute(f" UPDATE Usuario SET nome='{vnome}', user='{vuser}', celular='{vcelular}', dt_nasc='{vdt_nasc}', dt_ini='{vdt_ini}', duracao='{vduracao}' WHERE id='{id}' ")
			db.session.add(u)
			db.session.commit()
			return redirect('/adm/l_rot')
		else:
			return ('Usuario nao Encontrado!')


@bp_adm.route('/d_rot/<int:id>', methods=['GET', 'POST'])
@login_required
def d_rot(id):
	msg = {}
	dt = CaRotina.query.get(id)
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			return redirect('/adm/l_rot')
	#	abort(404)
	return render_template('confElimina.html', msg=msg)


@bp_adm.route('/l_rot', methods=['GET', 'POST'])
@bp_adm.route('/l_rot', defaults={'id': None}, methods=['GET', 'POST'])
@login_required
def l_rot(id):
	dt = {}
	tb = {}
	msg = {} 
	pesq = request.form.get('pesq')
	print(pesq)
	if pesq: #CaUsuario.query.filter(nome==pesq)
		dt = CaRotina.query.filter(CaRotina.rotina.ilike(pesq))
	else:	
		dt = db.session.query(CaRotina.id_rot, CaRotina.rotina, CaRotina.id_mod, CaModulo.modulo). \
		select_from(CaRotina).join(CaModulo).all() 
	#dt = CaRotina.query.all()
	#sql = 'Select a.id_rot, a.rotina, b.modulo From CaRotina a INNER JOIN CaModulo b on a.id_mod = b.id_mod'
	#sql = db.session.query((a.id_rot, a.rotina, b.modulo).join(CaRotina a).join(CaModulo b).all()
	return render_template('adm/lst_rot.html', tb=tb, dt=dt, msg=msg)

@bp_adm.route('/c_apl', methods=['GET', 'POST'])
@login_required
def c_apl():
	msg = {}
	dt = {}
	tb = CaRotina.query.all()
	if request.method=='GET':
		return render_template('adm/cad_apl.html', tb=tb, dt=dt, msg=msg)
	
	if request.method=='POST':
		vid_mod = request.form.get('id_mod')
		vid_rot = request.form.get('id_rot')
		vaplic = request.form.get('aplic')
		vroteiro = request.form.get('roteiro')
		vcaminho = request.form.get('caminho')
		vhtml = request.form.get('html')
		vdata = request.form.get('data')
		i = CaAplic(vid_mod, vid_rot, vaplic, vroteiro, vcaminho, vhtml, vdata)
#		return '''  
#		<html>
#		    <head><title>Hello Flask</title></head>
#		    <body>
#		   		''' + vid_mod   + ''' '<br>'
#				''' + vid_rot  + ''' '<br>'
#				''' + vaplic   + ''' '<br>'
#				''' + vroteiro  + ''' '<br>'
#				''' + vcaminho  + ''' '<br>'
#				''' + vhtml   + ''' '<br>'
#				''' + vdata   + ''' '<br>'
#		    </body>
#		</html> '''
		if i:
			db.session.add(i)
			db.session.commit()
			return redirect('/adm/l_apl')
		else:
			msg['msg'] = 'Aplicação nao cadastrada !!!'
			msg['class'] = 'alert-danger'
			return render_template('adm/cad_apl.html', tm=tm, tb=tb, dt=dt, msg=msg)

#			return '''  
#				<html>
#				    <head><title>Hello Flask</title></head>
#				    <body>
#				   		''' +  vuser     + ''' '<br>'
#				    </body>
#				</html> '''


@bp_adm.route('/u_apl/<int:id>', methods=['GET', 'POST'])
@login_required
def u_apl(id):
	msg = {}
	dt = CaAplic.query.get(id)
	tm = CaModulo.query.filter_by(id_mod=dt.id_mod).first()
	tr = CaRotina.query.filter_by(id_mod=dt.id_mod, id_rot=dt.id_rot).first()
	vid = id
	#console.log(tb)
	#dt = CaModulo.query.filter_by(id=id).first()
	if request.method == 'GET':
		return render_template('adm/cad_apl.html', dt=dt, tm=tm, tr=tr, msg=msg)
		
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			vid_mod = request.form.get('id_mod')
			vid_rot = request.form.get('id_rot')
			vid_apl = request.form.get('id_apl')
			vaplic = request.form.get('aplic')
			vrotiro = request.form.get('roteiro')
			vcaminho = request.form.get('caminho')
			vhtml = request.form.get('html')
			vdata = request.form.get('data')
			u =  CaAplic(id_apl=vid, id_mod=vid_mod, id_rot=vid_rot, aplic=vaplic, roteiro=vroteiro, caminho=vcaminho, html=vhtml, data=vdata)
			db.session.add(u)
			db.session.commit()
			return redirect('/adm/l_apl')
		else:
			return ('Registro nao Encontrado!')


@bp_adm.route('/d_apl/<int:id>', methods=['GET', 'POST'])
@login_required
def d_apl(id):
	msg = {}
	dt = CaAplic.query.get(id)
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			return redirect('/adm/l_apl')
	#	abort(404)
	return render_template('confElimina.html', msg=msg)


@bp_adm.route('/l_apl', methods=['GET', 'POST'])
@bp_adm.route('/l_apl', defaults={'id': None}, methods=['GET', 'POST'])
@login_required
def l_apl(id):
	msg = {}
	dt = {}
	tb = {}
	pesq = request.form.get('pesq')
	print(pesq)
	if pesq: #CaUsuario.query.filter(nome==pesq)
		dt = db.session.query(CaAplic.id_apl, CaAplic.id_mod, CaModulo.modulo, CaAplic.id_rot, CaRotina.rotina, CaAplic.aplic). \
		select_from(CaAplic).filter(CaAplic.aplic.ilike(pesq)).join(CaRotina).join(CaModulo).all()
	else:	
		dt = db.session.query(CaAplic.id_apl, CaAplic.id_mod, CaModulo.modulo, CaAplic.id_rot, CaRotina.rotina, CaAplic.aplic). \
		select_from(CaAplic).join(CaRotina).join(CaModulo).all() 
	return render_template('adm/lst_apl.html', tb=tb, dt=dt, msg=msg)

#ans = db.session.query(Survey.description, Question.description, Answer.description).join(Survey). \
#       join(Question).join(Answer).join(Person).filter(Survey.survey_id == survey_id).all()


# ++++++++++++ CaParam  ===========================

@bp_adm.route('/c_parm', methods=['GET', 'POST'])
@login_required
def c_parm():
	msg = {}
	tb = {}
	dt = CaParam.query.all()
	if request.method=='GET':
		return render_template('adm/cad_parm.html', tb=tb, dt=dt, msg=msg)
	
	if request.method=='POST':
		vparam = request.form.get('param')
		vdescr =  request.form.get('descr')
		vvalor = float(request.form.get('valor'))
		vcond =  request.form.get('cond')
		obj_date = Validate(request.form.get('dt_ini'))
#		print(type(obj_date))
#		print(obj_date.ano, obj_date.mes, obj_date.dia, obj_date.hh, obj_date.mm, obj_date.ss )
		vdt_ini = datetime.strptime(request.form.get('dt_ini'), '%d/%m/%Y').date()
		vdt_fim = datetime.strptime(request.form.get('dt_fim'), '%d/%m/%Y').date()
		vcreated_datetime = str(datetime.now())
		vusuario = current_user.email
#		INSERT INTO caparam (param, descr, valor, cond, dt_ini, dt_fim, created_datetime, usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?)]
#		[parameters: [{'created_datetime': '2023-07-10 21:12:59.911450', 'cond': '', 'dt_ini': datetime.datetime(2023, 1, 1, 0, 0), 'valor': '120', 'dt_fim': datetime.datetime(2024, 12, 31, 0, 0), 'usuario': 'celso.abreu@gmail.com', 'param': 'tmout', 'descr': 'Time Out'}]]
		i = CaParam(vparam, vdescr, vvalor, vcond, vdt_ini, vdt_fim, vcreated_datetime, vusuario)
		if i:
			db.session.add(i)
			db.session.commit()
			return redirect('/adm/l_parm')
		else:
			msg['msg'] = 'Parametro nao cadastrada !!!'
			msg['class'] = 'alert-danger'
			return render_template('adm/cad_parm.html', tb=tb, dt=dt, msg=msg)

#			return '''  
#				<html>
#				    <head><title>Hello Flask</title></head>
#				    <body>
#				   		''' +  vuser     + ''' '<br>'
#				    </body>
#				</html> '''


@bp_adm.route('/u_parm/<int:id>', methods=['GET', 'POST'])
@login_required
def u_parm(id):
	msg = {}
	dt = CaParam.query.get(id)
	vid = id
	tm = {}
	tr = {}
	#console.log(tb)
	#dt = CaModulo.query.filter_by(id=id).first()
	if request.method == 'GET':
		return render_template('adm/cad_parm.html', dt=dt, tm=tm, tr=tr, msg=msg)
		
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			vparam = request.form.get('param')
			vdescr =  request.form.get('descr')
			vvalor = float(request.form.get('valor'))
			vcond =  request.form.get('cond')
#			obj_date = strTodate(request.form.get('dt_ini'))
#			print( obj_date.ano, obj_date.mes, obj_date.dia)
			vdt_ini = datetime.strptime(request.form.get('dt_ini'), '%d/%m/%Y')
			vdt_fim = datetime.strptime(request.form.get('dt_fim'), '%d/%m/%Y')
			vcreated_datetime = str(datetime.now())
			vusuario = current_user.nome
			u =  CaParam(vid, vparam, vdescr, vvalor, vcond, vdt_ini, vdt_fim, vcreated_datetime, vusuario)
			db.session.add(u)
			db.session.commit()
			return redirect('/adm/l_parm')
		else:
			return ('Registro nao Encontrado!')


@bp_adm.route('/d_parm/<int:id>', methods=['GET', 'POST'])
@login_required
def d_parm(id):
	msg = {}
	dt = CaParam.query.get(id)
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			return redirect('/adm/l_parm')
	#	abort(404)
	return render_template('confElimina.html', msg=msg)


@bp_adm.route('/l_parm', methods=['GET', 'POST'])
@bp_adm.route('/l_parm', defaults={'id': None}, methods=['GET', 'POST'])
@login_required
def l_parm(id):
	msg = {}
	dt = {}
	tb = {}
	pesq = request.form.get('pesq')
	print(pesq)
	if pesq: #CaUsuario.query.filter(nome==pesq)
		dt = CaParam.query.filter(CaParam.descr.ilike(pesq))
		print(db)
	else:	
		dt = CaParam.query.all() 
	return render_template('adm/lst_parm.html', tb=tb, dt=dt, msg=msg)


# ++++++++++++ CaTpserv  ===========================

@bp_adm.route('/c_tps', methods=['GET', 'POST'])
@login_required
def c_tps():
	msg = {}
	tb = {}
	dt = {}
	if request.method=='GET':
		return render_template('adm/cad_tps.html', tb=tb, dt=dt, msg=msg)
	
	if request.method=='POST':
		vdescr = request.form.get('descr')
		vtipo = request.form.get('tipo')
		vadded_on = datetime.now()
		i = CaTpserv(descr=vdescr, tipo=vtipo, added_on=vadded_on )
		print(i)
		if i:
			db.session.add(i)
			db.session.commit()
			return redirect('/adm/l_tps')
		else:
			msg['msg'] = 'Tipo de Serviço Invalido!!'
			msg['class'] = 'alert-danger'
		return render_template('adm/cad_tps.html', tb=tb, dt=dt, msg=msg)


#			return '''  
#				<html>
#				    <head><title>Hello Flask</title></head>
#				    <body>
#				   		''' +  vuser     + ''' '<br>'
#				    </body>
#				</html> '''


@bp_adm.route('/l_tps/<int:id>', methods=['GET', 'POST'])
@bp_adm.route('/l_tps', defaults={'id': None}, methods=['GET', 'POST'])
@login_required
def l_tps(id):
	db = {}
	msg = {} 
	pesq = request.form.get('pesq')
	print(pesq)
	if pesq: #CaTpserv.query.filter(nome==pesq)
		db = CaTpserv.query.filter(CaTpserv.descr.ilike(pesq))
	else:	
		db = CaTpserv.query.all()
	return render_template('adm/lst_tps.html', db=db, msg=msg)

@bp_adm.route('/u_tps/<int:id>', methods=['GET', 'POST'])
@login_required
def u_tps(id):
	msg = {}
	dt = CaTpserv.query.get(id)
	vid = id
	#dt = CaTpserv.query.filter_by(id=id).first()
	if request.method == 'GET':
		return render_template('adm/cad_tps.html', dt=dt, msg=msg)
		
	if request.method == 'POST':
		if dt:
			db.session.delete(dt)
			db.session.commit()
			vdescr = request.form.get('descr')
			vtipo = request.form.get('tipo')
			vadded_on = datetime.now()
		#	session.execute("UPDATE catpservs SET descr = vdescr, tipo = vtipo, added_on = vadded_on  WHERE id_tps = id" )
			u = CaTpserv(id_tps=vid, descr=vdescr, tipo=vtipo, added_on=vadded_on)
			db.session.add(u)
			db.session.commit()
			return redirect('/adm/l_tps')
		else:
			return ('Usuario nao Encontrado!')


@bp_adm.route('/d_tps/<int:id>', methods=['GET', 'POST'])
@login_required
def d_tps(id):
	msg = {}
	d = CaTpserv.query.get(id)
	if request.method == 'POST':
		if d:
			db.session.delete(d)
			db.session.commit()
			return redirect('/adm/l_tps')
	#	abort(404)
	return render_template('confElimina.html', msg=msg)



