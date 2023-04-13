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

from app import app
from flask import Flask, render_template, request, redirect, flash

#from flask_login import login_user, logout_user

from database import db

from app.models.tabels import Usuario
from app.models.forms import LoginForm 


@app.route('/')
def index():
    return render_template('index.html') 
       
 #   numero = '10'
 #   return '''
 #   <html>
 #       <head> <title>CA Jogos</title> </read>
 #       <header> Birro Da Sorte  <header>
 #       <body>
 #           <h6> Resultado '''+numero+''' </h6>
 #       </body>
 #   </html>
 #   '''


@app.route('/rota/<rota>', methods=['GET','POST'])
def rota(rota):
    print(rota)
    if request.method=='GET':
        return redirect({{rota}})
    
    if request.method=='POST':
        return redirect({{rota}})
        #return HttpResponse('Valor da variavel', {{rota}} )
         

@app.route('/login', methods=['GET','POST'])
def login():
    data = {}
    msg = {}
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # and Usuario.verify_password(senha)
#Testa  User.query.filter((User.email == email) | (User.name == name)).first()
#Abre session   db.session.query(User).filter(or_(User.email=='useremail@example.com', User.name=="username")).first()
        u = Usuario.query.filter_by(email=email).first()
        print(email, senha, u)
        if u:
            s = Usuario.query.filter_by(senha=senha).first()
            if s:
                #console.log(s);
                return render_template("logado.html", u=u, msg=msg)
            else:
                msg['msg'] = 'Senha Incorreta !!!'
                msg['class'] = 'alert-danger'
        else:
            msg['msg'] = 'Usuario nao Cadastrado !!!'
            msg['class'] = 'alert-danger'
    return render_template("login.html", form=form, msg=msg)

@app.route('/usercorr/<int:id>')
def usercorr(id):
    User_id = Usuario.query.filter_by(id=id).first()
    return redirect('logout')

@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/autenticar/<id>', methods=['GET','POST'])
def autenticar(id):
    return render_template("logado.html", id=id)



@app.route('/teste/<info>')
@app.route('/teste', defaults={'info': None})
def teste(info):
# Inclusao registro 
#    i = Usuario('Magaly', "Tw8858", 'magaly.ilma@gmail.com', '5571992558749', '45566889968', '15/06/1968', '2023/03/20', '2023/03/20 16:22','123456', '123456' )
#    db.session.add(i)
#    db.session.commit()
# Select ou leitura
    r = Usuario.query.filter_by(nome='Bob').first()
    print(r)
# Update o registro apos selecionar podemos substituir o conteudo
#   r.nome = "Claudio Copque" 
#   db.session.add(r)
#   db.commit()   
# Deleção seria apos o registro selecionado agente elimina-lo
#   db.session.delete(r)
#   db.commit() 
    return '''
    <html>
        <head> <title>CA Jogos</title> </read>
        <header> Registro criado com sucesso <header>
        <body>
            <h1> Registro criado com sucesso </h1> <br>
           
        </body>
    </html>
    '''

@app.route('/autent/<user>')
def autent(user):
    return render_template("autent.html", user=user)

@app.route('/homepage')
def homepage():
    nome = "Celso"
    dados = {"professor": 'Celso' , "canal": '@CA ' } 
    return render_template("logado.html", nome=nome, dados=dados)

#@app.route('/usuarios', defaults={"cpf":"EMBRANCO"})
#@app.route('/usuarios/<cpf>')
#def usuarios():
#    return render_template("usuarios.html", cpf=cpf)

#Recebendo dados via metothod GET
@app.route('/autentic_get', methods=['GET'])
def autentic_get():
    cpf = request.args.get('cpf')
    senha = request.args.get('senha')
    return render_template("usuarios.html", cpf=cpf, senha=senha)

#Recebendo dados via metothod POST
@app.route('/autentic_post', methods=['POST'])
def autentic_post():
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')
    return render_template("usuarios.html", cpf=cpf, senha=senha)


@app.route('/busca')
def busca(request):
    data = {}
    place1 = 'parque sao braz, cj 16 federacao, Ba'
    place2 = 'rua euler pereira cardoso, Ba'
    geolocator = Nominatim(user_agent="ca_on")
    location = geolocator.geocode(place1)
    return HttpResponse(location[0], location[1])
    return '''
           <html>
                <head> <title>CA Jogos</title> </read>
                <header> Birro Da Sorte  <header>
                <body>
                    <h6> Resultado '''+numero+''' </h6>
                </body>
            </html>
        '''

# print(location.adress)
# print("POINT({}.{})".format(local.latitude,local.longitude))
@app.route('/pedido')
def pedido(request):
    data = {}
    return render(request, 'tax/pedido.html', data )


@app.route('/geoloc')    
def geoloc(request):
    data = {}
    destino = request.GET.get('destino')
    origem = request.GET.get('origem')
#   location2 = str(gpds.tools.geocode(origem , provider="nominatim", user_agent="Geolocation2"))
#   location = locator.geocode(“Champ de Mars, Paris, França”)
# Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/ 
    API_KEY = "YOUR_API_KEY"
    if destino:
        location1 = geolocator.geocode(destino)
        url = f"https://api.geoapify.com/v1/geocode/search?text={destino}&limit=1&apiKey={API_KEY}"
        # Send the API request and get the response
        response = requests.get(url)
        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data from the response
            dat = response.json()
            # Extract the first result from the data
            result = dat["features"][0]
            # Extract the latitude and longitude of the result
            latitude = result["geometry"]["coordinates"][1]
            longitude = result["geometry"]["coordinates"][0]
        data['destino'] = str(location1.address)
        data['lat_dest'] = latitude
        data['log_dest'] = longitude
        #   data['alt_dest'] = altitude
    else:
        data['msg'] = 'Destino invalido !!!'
        data['class'] = 'alert-danger'
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    if origem:  
        location2 = geolocator.geocode(origem)
        url = f"https://api.geoapify.com/v1/geocode/search?text={origem}&limit=1&apiKey={API_KEY}"
        # Send the API request and get the response
        response = requests.get(url)
        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data from the response
            dat = response.json()
            # Extract the first result from the data
            result = dat["features"][0]
            # Extract the latitude and longitude of the result
            latitude = result["geometry"]["coordinates"][1]
            longitude = result["geometry"]["coordinates"][0]
#           altitude = result["geometry"]["coordinates"][3]
        data['origem'] = str(location2.address)
        data['cor_orig'] = result
        data['lat_orig'] = latitude
        data['log_orig'] = longitude
#       data['alt_orig'] = altitude
        data['msg'] = 'Origem invalida !!!'
        data['class'] = 'alert-danger'
    
    data['user_cli'] = 'Teste'
    data['user_mot'] = 'A5658'
    data['dt_pedcar'] = datetime
    data['vl_calc'] = 10.00
    data['vl_neg'] =  20.00
    data['status'] = True
    data['obs'] = 'Teste de coordenadas geometricas'
    if data:
        data['form'] = CapedcarForm(initial={'origem':data['origem'],
                                            'user_cli':data['user_cli'],
                                            'user_mot':data['user_mot'],
                                            'lat_orig':data['lat_orig'],
                                            'log_orig':data['log_orig'], 
                                            'destino':data['destino'], 
                                            'lat_dest':data['lat_dest'],
                                            'log_dest':data['log_dest'],
                                            'dt_pedcar':data['dt_pedcar'], 
                                            'qtd_pedcar':data['vl_calc'], 
                                            'vl_calc':data['vl_calc'], 
                                            'vl_neg':data['vl_neg'], 
                                            'status':data['status'],
                                            'obs':data['obs'] })
        return render(request, 'tax/pedcar.html', data )
    else:
        return HttpResponse('Arquivo nao carregado')

@app.route('/celular')
def celular(request):
    data = {}
    return render(request, 'tax/pedcel.html', data )

@app.route('/infocel')
def infocel():
    data = {}
    number = int(request.GET.get('phone'))
    if number:
        ch_number = phonenumbers.parse(number, "CH")
        data['descricao'] = geocoder.get_description_for_number(ch_number, 'pt')
        service_number = phonenumbers.parse(number, "RO")
        data['servico'] = carrier.name_for_number(service_number, 'pt')
        return render(request, 'tax/infocel.html', data )
    else:
        return HttpResponse('Info de celular nao carregadas')


lat1 = 40.6976637
lon1 = -74.1197643
lat2 = 25.7825453
lon2 = -80.2994985
@app.route('/haversine_distance')
def haversine_distance(lat1, lon1, lat2, lon2):
    data = {}
    r = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 -a)))
    km = str(np.round(res, 2))
    return HttpResponse( 'Kilometros:', {{ km }}  )

#print(haversine_distance(lat1, lon1, lat2, lon2))

#loc1=(40.6976637, -74.1197643)
#loc2=(25.7825453, -80.2994985)

#print(hs.haversine(loc1,loc2))
# Usaemos a API Nominatim, e libs Geopandas, Geopy e Shapely, Openstreetmep
# Usar o pandas so pra carregar planilhas

# Criando chamadas de API REST

@app.before_first_request
def create_table():
    db.create_all()