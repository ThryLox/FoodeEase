from django.shortcuts import redirect, render
from django.views import View
from .models import MenuItem, Category, OrderModel
from .forms import CreateUserForms
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class Index(LoginRequiredMixin,View):
   
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(LoginRequiredMixin,View):
   
    def get(self, request, *args, **kwargs):
        # get every item from each category

        items = []

        items = MenuItem.objects.all()
        
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        

       
        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'drinks': drinks,
            'items' : items,
        }

     

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        street = request.POST.get('street')
        province = request.POST.get('province')
        zip_code = request.POST.get('zip_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        user = request.user
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
                'user': user
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        
    
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        

        order = OrderModel.objects.create(
            price=price, 
            name=name, email=email,
            street=street,
            city=city,
            province=province,
            zip_code=zip_code)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price,
            'user':user
        }

        if price == 0:
            messages.success(request, 'Please Select atleast One Item')
            order = OrderModel.objects.last()
            print(order)
            order.delete()
            return redirect('order')
        else:
            return redirect('order_confirmation', pk = order.pk)
    
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwards):
        order= OrderModel.objects.get(pk=pk)

        context  = {
            'pk' : order.pk,
            'items' : order.items,
            'price' : order.price 
        }

        return render(request, 'customer/order_confirmation.html', context)
    def post(self, request, pk, *args, **kwards):
        order = OrderModel.objects.last()
        print(order)
        order.delete()
        return redirect('order')
    
class OrderPayConfirmation(View):
    def get(self, request, pk, *args, **kwards):
        return render(request, 'customer/order_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items= MenuItem.objects.all()
        context = {
            'menu-items':menu_items
        }
        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        menu_items=MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context ={
            'menu_items':menu_items
        }

        return render(request, 'customer/menu.html', context)
