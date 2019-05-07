from django.shortcuts import render, render_to_response, redirect

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView
from django import forms
from .forms import ArticleForm
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Article, ArticleOrder, Cart
from django.views import generic
from django.contrib.auth.decorators import login_required
import paypalrestsdk
from paypalrestsdk import Payment
from django.contrib import messages
from django.db import models
from django.utils import timezone
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the DIY Eco System")
    return render_to_response('index.html')

class DIYArticleListView(ListView):
    model = Article
    template_name = 'diylist.html'

class DIYArticleDetailView(DetailView):
    model = Article
    slug_field = 'pk'
    template_name = "article_details.html"
    slug_url_kwarg = 'article.id'

def article_details(request, article_id):
    context= {
            'article':Article.objects.get(pk=article_id),
    }
    return render(request,'article_details.html',context)

@csrf_protect
def create(request):
        if request.POST:
                form = ArticleForm(request.POST, request.FILES)
                if form.is_valid():
                        a = form.save()
                        a.user = request.user
    
                        return HttpResponseRedirect('/eco/list')
        else:
                form = ArticleForm()

        args = {}
        args['form'] = form
        return render(request,'create_article.html',args)

@login_required
def add_to_cart_new(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    cart,created = Cart.objects.get_or_create(user=request.user, active=True)
    order,created = ArticleOrder.objects.get_or_create(article=article,cart=cart)
    order.quantity = order.quantity or 0 + 1
    order.save()
    messages.success(request, "Cart updated!")
    print("Cart updated!")
    return redirect('cart')

@login_required
def add_to_cart(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        print (article)
    except ObjectDoesNotExist:
        pass
    else:
        try:
            cart= Cart.objects.get(user=request.user, active =True)
        except ObjectDoesNotExist:
            cart= Cart.objects.create(user=request.user)
            print("cart created")
        order,created = ArticleOrder.objects.get_or_create(article=article,cart=cart)    
    if order.article.package_quantity > 0:    
        order.quantity = (order.quantity or 0) + 1
       #order.quantity += 1
        order.save()
        messages.success(request, "Cart updated!")
    return redirect('cart')

def remove_from_cart(request,article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except ObjectDoesNotExist:
        pass
    else:
        cart= Cart.objects.get(user=request.user, active =True)
        cart.remove_from_cart(article_id)
    return redirect('cart')
        
def cart(request):
    cart=Cart.objects.get(user=request.user, active=True)
    orders= ArticleOrder.objects.filter(cart=cart)
    total = 0
    count= 0
    if (orders):
        for order in orders:
            if (order.article.package_quantity):   
                total += (order.article.diy_package * (order.quantity or 0))
                print(order.article.diy_package)            
                print(order.quantity)
                count += (order.quantity or 0)
    print(total)    
    context = {
        'cart' : orders,
        'total': total,
        'count': count,
    }
    return render(request, 'cart.html', context)
    

@login_required
@csrf_protect
def process_order(request,processor):
    if processor == "paypal":
        payment_id= request.GET.get('paymentId')
        cart = Cart.objects.get(payment_id=payment_id)
        orders= ArticleOrder.objects.filter(cart=cart)
        total=0
        for order in orders:
            total +=(order.article.diy_package * order.quantity)
            context= {
                'cart': orders,
                'total': total,
            }
            return render(request, 'process_order.html', context)

@login_required
def checkout(request,processor):
    cart=Cart.objects.get(user=request.user.id, active=True)
    orders= ArticleOrder.objects.filter(cart=cart)
    if processor == "paypal":
        redirect_url = checkout_paypal(request,cart,orders)
        return redirect(redirect_url)
        

@login_required
def checkout_paypal(request,cart,orders):
    items = []
    total=0
    for order in orders:
        total += (order.article.diy_package * (order.quantity or 0))
        recipe= order.article
        item= {
            'name': order.article.title,
            'price': str(order.article.diy_package),
            'currency': 'USD',
            'quantity': order.quantity
        }
        items.append(item)

    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": "AS13jFdFlw15SME5V0GgI9DpJDV16v11oSyPd6yy7ZjH_mJYeRX2sbiS9cBzLoNQlEJ2ZoWzZ2K4VMfU",
        "client_secret": "EI8QUaSf8VcyeUvIYIX00ZN0FEhSDrAbQg_DX_EZP--r6-GtKo7KXcNyKimaYy-dcJh5Acz2z55E_wlj",
    })

    payment = Payment({
    "intent": "sale",

    # Payer: A resource representing a Payer that funds a payment
    # Payment Method as 'paypal'
    "payer": {
        "payment_method": "paypal"},

    # Redirect URLs
    "redirect_urls": {
        "return_url": "http://localhost:8000/eco/process/paypal",
        "cancel_url": "http://localhost:8000/eco"},
   
    # Transaction
    "transactions": [{

        # ItemList
        "item_list": {
            "items": items},

        # Amount
        # Let's you specify a payment amount.
        "amount": {
            "total": str(total),
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})

# Create Payment and return status
    if payment.create():
        cart_instance = cart
        cart_instance.payment_id= payment.id
        cart_instance.save()
                   
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect_url
    else:
        print("Error while creating payment:")
        print(payment.error)


@login_required
def complete_order(request,processor):
    cart= Cart.objects.get(user=request.user.id,active=True)
    if processor == "paypal":

        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": "AS13jFdFlw15SME5V0GgI9DpJDV16v11oSyPd6yy7ZjH_mJYeRX2sbiS9cBzLoNQlEJ2ZoWzZ2K4VMfU",
            "client_secret": "EI8QUaSf8VcyeUvIYIX00ZN0FEhSDrAbQg_DX_EZP--r6-GtKo7KXcNyKimaYy-dcJh5Acz2z55E_wlj",
        })
        payment= paypalrestsdk.Payment.find(cart.payment_id)
        if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):               
            message= "Success! Your order has been completed, and is being processed. Payment id: %s" %(payment.id)
            cart.active =False
            cart.order_date= timezone.now()
            cart.save()
            context = {
                'message': message,
            }
            return render (request, 'order_complete.html', context)
        else:
            message = "There was a problem with the transaction. Error: %s" % (payment.error)
            context = {
                'message': message,
            }
            return render (request, 'order_complete.html',context)
    return render (request, 'order_complete.html')

@login_required
def order_error(request):
    return render(request, 'order_error.html')
        
