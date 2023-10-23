from paho.mqtt.client import Client
from django.shortcuts import render, redirect
import time
from django.shortcuts import render
from django.http import HttpResponseRedirect , HttpResponse
from datetime import datetime
from .models import Capteur
from .forms import CapteurForm
from . import models


def index(request):
    return render(request, 'index/index.html')


def plage(request):
    return render(request, 'plage/plage.html')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import CapteurForm  # Assure-toi d'importer correctement ton formulaire


def temp(request):
    liste_capteurs = models.Capteur.objects.all()
    return render(request, 'temp/temp.html', {"liste_capteurs": liste_capteurs})


def confirmationT(request):
    if request.method == 'POST':
        capteur_form = CapteurForm(request.POST)
        if capteur_form.is_valid():
            capteur = capteur_form.save()
            return HttpResponseRedirect('/temp/')

    return render(request, 'temp/createT.html', {"form": CapteurForm()})


def createT(request):
    if request.method == "POST":
        form = CapteurForm(request.POST)
        if form.is_valid():
            capteur = form.save()
            return render(request, 'temp/confirmationT.html', {"capteur": capteur})

    return render(request, 'temp/createT.html', {"form": CapteurForm()})


def readT(request, id):
    capteur = get_object_or_404(models.Capteur, pk=id)
    return render(request, 'temp/readT.html', {"capteur": capteur})


def deleteT(request, id):
    capteur = get_object_or_404(models.Capteur, pk=id)
    capteur.delete()
    return HttpResponseRedirect('/temp/')


def obtenir_heure_actuelle():
    return datetime.now().strftime('%H:%M:%S')

def comparer_heure_actuelle(plage_debut, plage_fin):
    heure_actuelle = datetime.now().time()
    plage_debut = datetime.strptime(plage_debut, '%H:%M').time()
    plage_fin = datetime.strptime(plage_fin, '%H:%M').time()

    if plage_debut <= heure_actuelle <= plage_fin:
        publish_data3("0")
        return "La plage horaire est en cours."
    else:
        publish_data3("1")
        return "La plage horaire n'est pas active actuellement."



def recuperer_date(request):
    if request.method == 'POST':
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')

        print(f"Heure début: {heure_debut}, Heure fin: {heure_fin}")

        if heure_debut and heure_fin:
            heure_debut = datetime.strptime(heure_debut, '%H:%M').strftime('%H:%M')
            heure_fin = datetime.strptime(heure_fin, '%H:%M').strftime('%H:%M')

            plage_horaire = f"{heure_debut} - {heure_fin}"
            heure_actuelle = obtenir_heure_actuelle()

            print(comparer_heure_actuelle(heure_debut, heure_fin))

            return render(request, 'plage/plage.html',
                          {'plage_horaire': plage_horaire, 'heure_actuelle': heure_actuelle})
        else:
            return HttpResponse("Veuillez remplir les champs heure correctement.")
    else:
        return HttpResponse("Utilisez la méthode POST pour soumettre le formulaire.")



def bouton(request):
    try:
        bouton_value1 = request.POST.get('bouton1')
        bouton_value2 = request.POST.get('bouton2')
        bouton_value3 = request.POST.get('bouton3')

        if bouton_value1 == "1":
            client.subscribe(prise1)
            publish_data1("1")
        elif bouton_value1 == "0":
            client.subscribe(prise1)
            publish_data1("0")
        elif bouton_value2 == "1":
            client.subscribe(prise2)
            publish_data2("1")
        elif bouton_value2 == "0":
            client.subscribe(prise2)
            publish_data2("0")
        elif bouton_value3 == "1":
            client.subscribe(prise2)
            publish_data2("1")
            client.subscribe(prise1)
            publish_data1("1")
        elif bouton_value3 == "0":
            client.subscribe(prise2)
            publish_data2("0")
            client.subscribe(prise1)
            publish_data1("0")

        time.sleep(0.5)
        global etat_prises
        return render(request, 'bouton/bouton.html', {'etat_prises': etat_prises})
    except Exception as e:
        print(e)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'toto' and password == 'toto':
            return render(request, 'index/index.html')
        else:

           return redirect(login_view)

    return render(request, 'auth/login.html')


BROKER = '213.166.214.70'
USERNAME = 'toto'
PASSWORD = 'BABA_SAE301'
PORT = 1883
prise1 = 'prise1'
prise2 = 'prise2'
plageh= 'plage'
etat_prises = {'prise1': 'Non défini', 'prise2': 'Non défini'}

client = Client()

def connexion(client, userdata, flags, rc):
    if rc == 0:
        print("Connection réussi.")
        client.subscribe(prise1)
        client.subscribe(prise2)
        client.subscribe(plageh)


        publish_data1("serveur web connecté")
        publish_data2("serveur web connecté")
        publish_data3("serveur web connecté")


    else :
        print("deconnexion.")
        client.subscribe(prise1)
        client.subscribe(prise2)
        publish_data1("serveur web deconnecté")
def deconnexion(client, userdata, rc):
    print("\nDisconnected from MQTT broker")

etat_prises = {'prise1': 'Non défini', 'prise2': 'Non défini'}


def message(client, userdata, msg):
    global etat_prises
    topic = msg.topic
    raw_message = msg.payload.decode('utf-8')

    if topic in etat_prises:
        print(f"Message reçu sur le topic {topic}: {raw_message}")
        if raw_message == '1':
            message = 'ON'
        elif raw_message == '0':
            message = 'OFF'
        else:
            message = raw_message
        etat_prises[topic] = message

def publish_data1(message):
    client.publish(prise1,message, qos=0, retain=False)
def publish_data2(message):
    client.publish(prise2,message, qos=0, retain=False)

def publish_data3(message):
    client.publish(plageh,message, qos=0, retain=False)
def initialize_mqtt():
    client.on_connect = connexion
    client.on_disconnect = deconnexion
    client.on_message = message
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT, 60)
    client.loop_start()

initialize_mqtt()
