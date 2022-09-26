from itertools import product
from locale import currency
from django.test import SimpleTestCase
from ..models import *
import requests



class DbFakeData(SimpleTestCase): 
    databases = '__all__'
    # 1. setup
    def setUp(self):
# HW7: truncate all the tables : bag, bagItem ..... Before importing data
#      hint: use django access to db or django ORM

        Money.objects.all().delete()
        Product.objects.all().delete()
        ProductStock.objects.all().delete()
        Client.objects.all().delete()
        Bag.objects.all().delete()
        BagItem.objects.all().delete()



        self.totalCount = 0

        print("Starting database seeding.... PRODUCTS")

        for id in range(1,11):
            r = requests.get(f"https://fakestoreapi.com/products/{id}")
            json_data = r.json()

            price = Money.objects.create(
                amount = json_data['price'] , currency = 'EUR'
            )
            product = Product.objects.create(
                id = json_data['id'],
                name = json_data['title'],
                description = json_data['description'][:280],
                price = price
            )
            stock = ProductStock.objects.create(quantity = 10 * id , product= product)
            self.totalCount += 1
        print("Done PRODUCTS")


        print("Starting database seeding.... USERS")
        for id in range(1,7):
            r = requests.get(f"https://fakestoreapi.com/users/{id}")
            json_data = r.json()

            client = Client.objects.create(
                id = json_data['id'],
                name = json_data['name']['firstname'] + ' ' + json_data['name']['lastname'],
                email = json_data['email'],
                phone = json_data['phone'],
                is_vip = 1 if id % 2 == 0 else 0,
                password= json_data['password']
           )
            self.totalCount += 1
        print("Done USERS")

        print("Starting database seeding.... BAGS")
        for id in range(1,4):
            r = requests.get(f"https://fakestoreapi.com/carts/{id}")
            json_data = r.json()

            client_id = json_data['id']
            client = Client.objects.get(pk=client_id)

            bag = Bag.objects.create(
                id = json_data['id'],
                client= client,
                # cost
            )
            bag_cost = 0
            for item in json_data['products']:
                product_id = item['productId']
                quantity = item['quantity']
                product = Product.objects.get(pk=product_id)
                bag_cost += product.price.amount * quantity
                bag_item = BagItem.objects.create(
                    quantity = quantity,
                    bag = bag,
                    product = product
                )
            self.totalCount += 1
            bag.cost = Money.objects.create(amount=bag_cost, currency="EUR")
            bag.save()




  
        print("Done BAGS")





    # 2. the actual test
    def test_data_integrity(self):
        print("Checking generated data integrity....")
        self.assertEquals(self.totalCount , 19 , f"Nu este egala cu  {self.totalCount}")



    # 3. clear

    def tearDown(self):
        print("Test data generated")

    