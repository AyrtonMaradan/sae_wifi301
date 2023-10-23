from django.urls import path
from .views import login_view, index, plage, bouton ,  recuperer_date ,confirmationT ,createT , deleteT , temp


urlpatterns = [
    path('', login_view),
    path('index/', index),
    path('plage/', plage),
    path('bouton/', bouton),
    path('deconnexion/',login_view),
    path('recuperer_date/', recuperer_date),
    path ('temp/',temp),
    path('createT/', createT),
    path('confirmationT/', confirmationT),
    path('deleteT/<str:id>/', deleteT),

]
