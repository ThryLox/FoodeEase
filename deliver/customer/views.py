from django.shortcuts import redirect, render
from django.views import View
from .models import MenuItem, Category, OrderModel
from .forms import CreateUserForms
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin



class Index( LoginRequiredMixin,View):
   
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
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            user = request.user
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
        

        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price,
            'user':user
        }

        return render(request, 'customer/order_confirmation.html', context)
    
class Register(View):
    def registerPage(request, *args, **kwargs):       

        form = CreateUserForms(request.POST)
        if request.method == 'POST':
              form = CreateUserForms(request.POST)
              if form.is_valid():
                  form.save(commit=True)
                  user =form.cleaned_data.get('username')
                  messages.success(request,'Account was created : ' + user )
                  return redirect('/accounts/login/')
        context = {'form': form}
        return render(request,'customer/register.html',context)
    

class Login(View):
    def loginPage(request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.info(request, "Username or password is incorrect")
                

        return render(request,'customer/login.html')

class Logout(View):

    def logoutUser(request):
        logout(request)
        return redirect('login')