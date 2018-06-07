from django.shortcuts import render
from app.models import Historiainvernadero

def index(request):
    idInvernadero = request.session['idInvernadero']
    data = Historiainvernadero.objects.order_by('-p')