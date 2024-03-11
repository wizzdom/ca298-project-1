import re
from django.shortcuts import render, get_object_or_404
import random
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now 


# Create your views here.
@login_required
def index(request):
    return redirect ('orders/')

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {'orders': orders})

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')




class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")

@login_required
def create_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            request.session['pizza_id'] = pizza.id
            return redirect('checkout')
    else:
        form = PizzaForm()
    return render(request, 'create_pizza.html', {'form': form})

@login_required
def checkout(request):
    pizza_id = request.session.get('pizza_id')
    if not pizza_id:
        return redirect('create_pizza')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.pizza = get_object_or_404(Pizza, id=pizza_id)
            order.user = request.user
            order.save()
            return redirect('confirmation')
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form})

@login_required
def confirmation(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')[:1]
    return render(request, 'confirmation.html', {'orders': orders})