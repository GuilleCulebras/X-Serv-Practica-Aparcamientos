from django.shortcuts import render
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from aparcamientos.models import Aparcamiento, Comentario, Seleccionado, CSS
from django.http import HttpResponse, HttpResponseRedirect
from aparcamientos.xmlParser import myContentHandler
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
from operator import itemgetter
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags

# Create your views here.

def parse():
	theParser = make_parser()
	theHandler = myContentHandler()
	theParser.setContentHandler(theHandler)

	# Ready, set, go!

	xmlFile = urllib.request.urlopen('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
	theParser.parse(xmlFile)

	lista = theHandler.getLista()

	return lista #Devuelve lista de diccionarios de los parkings

def loadData(lista):
	for dicParking in lista:
		nombre = dicParking['NOMBRE']
		try:
			descripcion = dicParking['DESCRIPCION']
		except KeyError:
			descripcion = "-"
		accessibilidad = dicParking['ACCESIBILIDAD']
		enlace = dicParking['CONTENT-URL']
		try:
			numero = dicParking['NUM']
		except KeyError:
			numero = "-"
		try:
			codigo = dicParking['CODIGO-POSTAL']
		except KeyError:
			codigo = "-"

		direccion = dicParking['NOMBRE-VIA'] + ', ' + numero + ', ' + codigo
		
		try:
			distrito = dicParking['DISTRITO']
		except KeyError:
			distrito = "-"
		try:
			barrio = dicParking['BARRIO']
		except KeyError:
			barrio = "-"
		try:
			latitud = dicParking['LATITUD']
		except KeyError:
			latitud = "-"
		try:
			longitud = dicParking['LONGITUD']
		except KeyError:
			longitud = "-"
		try:
			contacto = dicParking['TELEFONO'] + ', ' + dicParking['EMAIL']
		except KeyError:
			contacto = "-"
		aparcamiento = Aparcamiento(nombre = nombre, descripcion = descripcion, access = accessibilidad, enlace = enlace, direccion = direccion, contacto = contacto, barrio = barrio, distrito = distrito, latitud = latitud, longitud = longitud)
		aparcamiento.save()


def sortParkings(aparcamientos):
	dic = {}
	parkings_ordenado = []
	for aparcamiento in aparcamientos:
		identificador = aparcamiento.id
		try:
			comentarios = Comentario.objects.filter(aparcamiento_id = identificador)
			dic[identificador] = len(comentarios)
		except Comentario.DoesNotExist:
			print("No tiene comentarios")	
	parkings_ordenado = sorted(dic.items(), key = itemgetter(1), reverse = True)

	return parkings_ordenado #Devuelve una lista de diccionarios del tipo [(idAparcamiento, numComents),...]

############# /pagina principal ###################
@csrf_exempt
def pagina_principal(request):
	parkings_ordenado = []

	users = []
	aparcamientos = Aparcamiento.objects.all()

	if len(aparcamientos)<1:		
		lista_parkings = parse()
		loadData(lista_parkings)

	parkings_ordenado = sortParkings(aparcamientos)
	parkins_pagina = 5
	lista_parkings_aux = []

	for elem in parkings_ordenado:

		if parkins_pagina > 0 and elem[1]>0:#Si hay un coment o mas y contador mayor que 0
			parkins_pagina = parkins_pagina -1

			try:
				aparcamiento = Aparcamiento.objects.get(id = elem[0])#Cogemos el aparcamiento con esa id
				usuarios = User.objects.all()

				for usuario in usuarios:
					try:
						css = CSS.objects.get(user = usuario.username)
						if len(users) < len(usuarios): #Si hay menos usuarios en la lista que en la base de datos
							users.append((css.user, css.titulo))#añadimos al final de la lista el nombre y el titulo del usuario
					except CSS.DoesNotExist:
						if len(users) < len(usuarios):
							users.append((usuario.username,('Pagina de ' + usuario.username)))

				lista_parkings_aux.append(aparcamiento)

			except ObjectDoesNotExist:
				print ("Aparcamiento no disponible")
	template = get_template('index_extension.html')
	context = {'aparcamientos':lista_parkings_aux,
				'usuarios':users}
	respuesta = template.render(context,request)
	return HttpResponse(respuesta)

@csrf_exempt
def logIN(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)
	if user is not None:
		login(request, user)
	else:
		pass

	return HttpResponseRedirect("/")

########################     /USUARIO     ########################
@csrf_exempt
def usuario(request, user):
	try:
		lista_parkings = []
		try:
			css = CSS.objects.get(user = user)
			titulo = css.titulo
			us = user
			usuario = User.objects.get(username = user)
		except CSS.DoesNotExist:
			usuario = User.objects.get(username = user)
			us = usuario.username
			titulo = ""

		try:
			parking_seleccionados = Seleccionado.objects.filter(user = usuario)
			for aparcamiento in parking_seleccionados:
				lista_parkings.append((aparcamiento))
		except ObjectDoesNotExist:
			print ("No hay aparcamientos seleccionados")

		template = get_template('aparcamientos/plantilla_usuario.html')
		context = {'aparcamientos': lista_parkings,
					'usuario': us,
					'titulo':titulo}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse("404 Not Found", status = 404)

@csrf_exempt
def cambiarTitulo(request):
	lista_parkings = []

	if request.user.is_authenticated():
		titulo = request.POST.get('titulo')
		username = request.user.username
		try:
			css = CSS.objects.get(user = username)
			css.titulo = titulo
			css.save()
			usuario = User.objects.get(username = username)
		except CSS.DoesNotExist:
			css = CSS(user = request.user.username, titulo = titulo, color = "#3b913d", size = 0.0)
			css.save()

			usuario = User.objects.get(username = username)
	else:
		titulo = ""
		usuario = User.objects.get(username = request.user.username)
		username = usuario.username
	try:
		parking_seleccionados = Seleccionado.objects.filter(user = usuario)
		for aparcamiento in parking_seleccionados:
			lista_parkings.append((aparcamiento))
	except ObjectDoesNotExist:
		print("No hay aparcamientos seleccionados")
	template = get_template('aparcamientos/plantilla_usuario.html')
	context = {'aparcamientos': lista_parkings,
				'usuario': username,
				'titulo':titulo}

	return HttpResponse(template.render(context, request))


@csrf_exempt
def myPage(request):
	if request.user.is_authenticated():
		username = request.user.username
		return HttpResponseRedirect('/' + username)

#################### 	/APARCAMIENTOS    #####################

@csrf_exempt
def allParkings(request):
	aparcamientos = Aparcamiento.objects.all()
	template = get_template('aparcamientos/plantilla_aparcamientos.html')
	context = {'aparcamientos': aparcamientos}

	return HttpResponse(template.render(context, request))

@csrf_exempt
def filtParking(request):
	lista_parkings = []
	distrito = request.POST.get('distrito')
	accesible = request.POST.get('accesible')
	todos = Aparcamiento.objects.all()

	if distrito in ['CENTRO','CHAMARTIN','TETUAN','MONCLOA-ARAVACA','RETIRO','SALAMANCA','MORATALAZ','CHAMBERI','SAN BLAS-CANILLEJAS','CIUDAD LINEAL','FUENCARRAL-EL PARDO','ARGANZUELA','VILLA DE VALLECAS','LATINA','HORTALEZA','PUENTE DE VALLECAS','CARABANCHEL','VILLAVERDE','BARAJAS','VICALVARO','USERA']:
		lista_parkings = Aparcamiento.objects.filter(distrito = distrito)
	elif distrito == 'todos':
		lista_parkings = Aparcamiento.objects.all()
	elif accesible in ['SI','NO']:
		lista_parkings = Aparcamiento.objects.filter(access = accesible)
	elif accesible == 'todos':
		lista_parkings = Aparcamiento.objects.all()

	template = get_template('aparcamientos/plantilla_aparcamientos.html')
	context = {'aparcamientos': lista_parkings,
				'todos': todos}

	return HttpResponse(template.render(context, request))

@csrf_exempt
def parkingId(request, id):
	try:
		aparcamiento = Aparcamiento.objects.get(id = id)
		comentarios = Comentario.objects.filter(aparcamiento_id = aparcamiento)
		if len(comentarios) == 0:
			comentarios = []
	except ObjectDoesNotExist:
		pass

	template = get_template('aparcamientos/plantilla_aparcamientoid.html')
	context = {'aparcamiento': aparcamiento,
				'comentarios': comentarios}

	return HttpResponse(template.render(context, request))


@csrf_exempt
def addSelected(request,id):
	if request.user.is_authenticated():
		username = request.user.username
		try:
			user = User.objects.get(username = username)
			aparcamiento = Aparcamiento.objects.get(id = id)
			comentarios = Comentario.objects.filter(aparcamiento_id = aparcamiento)

			if len(comentarios) == 0:
				comentarios = []

			try:#Vemos si el aparcamiento ya esta seleccionado
				Seleccionado.objects.get(aparcamiento_id = aparcamiento)
				
				template = get_template('aparcamientos/plantilla_aparc_solicitado.html')
				context = {'aparcamiento': aparcamiento,
							'comentarios': comentarios}
				
				return HttpResponse(template.render(context, request))

			except Seleccionado.DoesNotExist:#Si no esta seleccionado, lo guardamos
				seleccionado = Seleccionado(aparcamiento_id = aparcamiento, user = user)
				seleccionado.save()

				template = get_template('aparcamientos/plantilla_aparcamientoid.html')
				context = {'aparcamiento':aparcamiento,
							'comentarios': comentarios}

				return HttpResponse(template.render(context, request))

		except ObjectDoesNotExist:
			pass

@csrf_exempt
def addComment(request, id):
	if request.user.is_authenticated():
		aparcamiento = Aparcamiento.objects.get(id = id)
		texto = request.POST.get('comentario')
		newCom = Comentario(texto = texto, aparcamiento_id = aparcamiento)
		newCom.save()

		return HttpResponseRedirect('/aparcamientos/' + str(id))

	else:
		return HttpResponseRedirect('/aparcamientos/' + str(id))



#################### /USUARIO/XML ######################

@csrf_exempt
def userXml(request, user):
	parking_seleccionados = []

	try:
		user = User.objects.get(username = user)
	except ObjectDoesNotExist:
		return HttpResponse("404 Not Found. No estas loggeado")

	seleccionados = Seleccionado.objects.filter(user = user)
	for seleccionado in seleccionados:
		parking_seleccionados.append(seleccionado)

	template = get_template('aparcamientos/plantilla_xml.xml')
	context = {'seleccionados': parking_seleccionados}

	return HttpResponse(template.render(context, request), content_type = 'text/xml')




######################## /ABOUT #######################

@csrf_exempt
def aboutPage(request):
	template = get_template('aparcamientos/about.html')
	context = {}

	return HttpResponse(template.render(context, request))


######################################################
######################################################
######################################################

##################### OPCIONAL #######################
##################### CANAL RSS ######################

@csrf_exempt
def rssChannel(request):
	lista_comment = []
	comentarios = Comentario.objects.all()

	template = get_template('aparcamientos/plantilla_rss.html')
	context = {'comentarios': comentarios}

	return HttpResponse(template.render(context, request))


###################  CANAL XML PAGINA PRINCIPAL ############
@csrf_exempt
def mainXml(request):
	if request.method == 'GET':
		parkings_ordenado = []
		lista_users = []
		lista_parkings = []
		aparcamientos = Aparcamiento.objects.all()
		parkings_ordenado = sortParkings(aparcamientos)
		counter = 5
		for elem in parkings_ordenado:
			if counter > 0 and elem[1] > 0:
				counter = counter - 1
				try:
					aparcamiento = Aparcamiento.objects.get(id = elem[0])
					usuarios = User.objects.all()
					for usuario in usuarios:
						try:
							css = CSS.objects.get(user = usuario.username)
							if len(lista_users) < len(usuarios): #Si hay menos usuarios en la lista que en la base de datos
								lista_users.append((css.user, css.titulo))#añadimos al final de la lista el nombre y el titulo del usuario
						except CSS.DoesNotExist:
							if len(lista_users) < len(usuarios):
								lista_users.append((usuario.username,('Pagina de ' + usuario.username)))

					lista_parkings.append(aparcamiento)
				except ObjectDoesNotExist:
					pass

		template = get_template('aparcamientos/plantilla_mainxml.xml')
		context = {'aparcamientos':lista_parkings,
					'usuarios':lista_users}
		return HttpResponse(template.render(context,request), content_type='text/xml')

	else:
		return HttpResponse("Not Found", status = 404)

################## REGISTRO DE USUARIOS ######################

@csrf_exempt
def register(request):
	if request.method == "GET":
		template = get_template('aparcamientos/plantilla_registro.html')
		context = {}
		return HttpResponse(template.render(context, request))
	elif request.method == "POST":
		username = request.POST.get('username')
		password = make_password(request.POST.get('password'))
		titulo = "Pagina de " + username

		user = User(username = username, password = password)
		user.is_staff = True
		user.save()

		user = User.objects.get(username = username)
		css = CSS(user = user, titulo = titulo)
		css.save()

		return HttpResponseRedirect('/')

	else:
		return HttpResponse("No funciona", status = 404)








