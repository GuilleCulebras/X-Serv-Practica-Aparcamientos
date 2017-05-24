from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Aparcamiento(models.Model):
	nombre = models.CharField(max_length = 200)
	descripcion = models.TextField(default = "")
	access = models.CharField(max_length = 2)
	enlace = models.TextField()
	direccion = models.CharField(max_length = 120,default = "")
	contacto = models.CharField(max_length = 150, default = "")
	barrio = models.CharField(max_length = 50)
	distrito = models.CharField(max_length = 50)
	latitud = models.TextField(blank = True)
	longitud = models.TextField(blank = True)	

class Comentario(models.Model):
	aparcamiento_id = models.ForeignKey(Aparcamiento)
	texto = models.TextField()	

class Seleccionado(models.Model):
	user = models.ForeignKey(User, default = "")
	aparcamiento_id = models.ForeignKey(Aparcamiento)
	fecha = models.DateField(auto_now = True)

class CSS(models.Model):
	user = models.CharField(max_length = 50, blank = True)
	titulo = models.CharField(max_length = 50, blank = True, null = True)
	color = models.CharField(max_length = 50, blank = True, null = True)
	size = models.IntegerField(blank = True, null = True)

