import email
import json
# from locale import currency
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import requests



# this_cart = {"Prod1":['iPhone',
#                     'ML1.0.1',
#                     299,
#                     'USD'],
#                 "Prod2":['Samsung',
#                          'Galaxy 2.0.1',
#                            399,
#                           'USD']
#                     }
    


def homePage(request):
    response = "<h1 align ='center'>Welcom to e-shop!</h1>"
    return render(request, 'home.html' ,{'version':'1.0.0'})


def CatalogPage(request):
    product = Product.objects.all()
    return render(request, 'Catalog.html' , {"products" : product })

def seedData(request):

    # for id in range(5,7):
            ####### Produs generate ############
            # r = requests.get(f"https://api.escuelajs.co/api/v1/products/{id}")
            # json_data = r.json()
            # # print(json_data)
            # price = Money.objects.create(
            #     amount= json_data['price'], currency = 'EUR')
            # product = Product.objects.create(
            #     id = json_data['id'],
            #     name = json_data['title'],
            #     description = json_data['description'][:280],
            #     price = price
            #     )
            # stock = ProductStock.objects.create(quantity=5*id, product=product) 
            ####### Produs generate ############

            ####### Client generate ############
            # r = requests.get(f"https://api.storerestapi.com/users")
            # json_data = r.json()

            # Client.objects.create(
            #     name = json_data['data'][id]['name'],
            #     email = json_data['data'][id]['email'],
            #     phone = json_data['data'][id]['number'],
            #     is_vip = False,
            #     password = json_data['data'][id]['password'],
            #     )

            ####### Client generate ############
            ####### Bag/Items generate ############




            ####### Bag/Items generate ############
    return HttpResponse(f"<h3 align = 'center'> aa </h3>")



def addProdBag(request,Client_id=1,produs_id=11,quantity=10):
    
    Produs = Product.objects.get(pk =produs_id)
    money = Money.objects.get(pk=Produs.price_id)
    # cost = int(money.amount) * quantity 
    client = Client.objects.get(pk=Client_id)   
    client_bag = Bag.objects.create(cost_id=money.id, client = client ) 
    BagItem.objects.create(quantity = quantity, product= Produs , bag = client_bag )    

    return HttpResponse(f"<h3 align = 'center'> The final cost of the product {Produs.name} =  {money.amount * quantity}  </h3>")