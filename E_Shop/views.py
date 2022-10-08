# from locale import currency
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
import requests

def countItemsinBag(request):
    if request.session['bag_id']:
        bag_id =request.session['bag_id']
        items = BagItem.objects.filter(bag_id=bag_id)
        items_count =len(items) 
        return items_count


def CatalogPage(request):
    product = Product.objects.all()
    paginator = Paginator(product,4)
    selected_pade_number = request.GET.get('page') or 1
    page = paginator.page(selected_pade_number)
    product = page.object_list

    return render(request, 'Catalog.html' , {"products" : product, "paginator": paginator, "page_number" : page.number, "bag_items_count": countItemsinBag(request)})

def homePag(request):

    return render(request, 'home.html' , {"bag_items_count": countItemsinBag(request)})
def contactPag(request):

    return render(request, 'Contact.html' , {"bag_items_count": countItemsinBag(request)})
def aboutPag(request):

    return render(request, 'about.html' , {"bag_items_count": countItemsinBag(request)})
def cartPag(request):

    return render(request, 'cart.html' , {"bag_items_count": countItemsinBag(request)})

def getProduct(request):
    prod_id = request.GET.get('prod')
    product = Product.objects.get(pk=prod_id)
    stock = ProductStock.objects.get(pk=prod_id)
    return render(request, 'product.html' , {"range_stock":range(stock.quantity+1),"product": product ,"stock":stock ,"bag_items_count": countItemsinBag(request)})

def buyProduct(request):
    product_id = request.GET.get('prod_id') 
    quantity = request.GET.get('quantity') or 0
    product = Product.objects.get(pk=product_id)
    stock = ProductStock.objects.filter(product_id=product_id)
    if request.session['bag_id']:
        bag_id = request.session['bag_id']
        bag = Bag.objects.get(pk=bag_id)
    else:
        cost = Money.objects.create(amount=0,currency="EUR")
        bag = Bag.objects.create(cost=cost)
        request.session['bag_id'] = bag.id

    bag_item = BagItem.objects.create(quantity=quantity,product=product,bag=bag)

    return redirect(request.META.get('HTTP_REFERER'))





# Sa fie gasit clientul dupa email si parola (ar corespunde cu logarea pe site)

def LogIn(request,email = 'kevin@gmail.com', password = 'kev02937@'):
    db_qset = Client.objects.filter(email = email,password= password)
    if  len(db_qset) == 1:
        return HttpResponse(f"<h1 align ='center'>{db_qset[0].name}<br>{db_qset[0].phone}</h1>")
    return HttpResponse(f"<h1 align ='center'> This email {email} or pass {password} is incorrectly</h1>")


# Sa fie gasit cosul clientului dupa id-ul clientului
def searchBag(request,client_id):
    Bag_client = Bag.objects.filter(client_id)
    if  len(Bag_client) == 1:
        return True
    else:
        return False
        # for i in range(Bag_client):
        #     return HttpResponse(f"<h1 align ='center'> Client{client__id} have bag_id: {Bag_client[i].client_id}<br>Cost_id:{Bag_client[i].cost_id}</h1>")
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