# from locale import currency
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
import requests




def CatalogPage(request):
    product = Product.objects.all()
    paginator = Paginator(product,4)
    selected_pade_number = request.GET.get('page')
    page = paginator.page(selected_pade_number)
    product = page.object_list

    return render(request, 'Catalog.html' , {"products" : product, "paginator": paginator, "page_number" : page.number})




# Sa fie gasit clientul dupa email si parola (ar corespunde cu logarea pe site)

def LogIn(request,email = 'kevin@gmail.com', password = 'kev02937@'):
    db_qset = Client.objects.filter(email = email,password= password)
    if  len(db_qset) == 1:
        return HttpResponse(f"<h1 align ='center'>{db_qset[0].name}<br>{db_qset[0].phone}</h1>")
    return HttpResponse(f"<h1 align ='center'> This email {email} or pass {password} is incorrectly</h1>")


# Sa fie gasit cosul clientului dupa id-ul clientului
def searchBag(request,client__id= 1):
    Bag_client = Bag.objects.filter(client__id = 1)
    if  len(Bag_client) > 1:
        for i in range(Bag_client):
            return HttpResponse(f"<h1 align ='center'> Client{client__id} have bag_id: {Bag_client[i].client_id}<br>Cost_id:{Bag_client[i].cost_id}</h1>")
    # return HttpResponse(f"<h1 align ='center'> Client {client__id} have bag_id: {Bag_client[0].client_id}<br>Cost_id:{Bag_client[0].cost_id}</h1>")
    return Bag_client[0]
# Sa fie gasite toate itemurile din cosul clientului dupa id-ul clientului
def searchBagItems(request,client__id=1):
    bag = searchBag(client__id)
    Items = BagItem.objects.filter(bag_id = bag.id)
    return Items
    # Sa fie numarate toate itemurile din cosul clientului dupa id-ul clientului

def countItems(request,client__id = 1):
    Items = searchBagItems(client__id)
    return HttpResponse(f"<h1 align ='center'> Client {client__id} have bag_items: {len(Items)} </h1>")

    # Sa fie returnat True daca o cantitate dorita pentru un anumit produs este in stock si False daca nu 
def checkStock(request,product_id = 1,quantity_1 = 11):
    stock  = ProductStock.objects.filter(product__id=product_id ,quantity__gte=quantity_1)
    # print(stock)
    return True if len(stock) > 0 else False