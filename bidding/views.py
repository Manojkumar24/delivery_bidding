import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
import requests
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from bidding.models import Product, biddedAmount, pending_orders
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .forms import RegisterForm, BiddingForm, EditForm

product_api_key = '6mYgSqoG0PY7p4Eot1PjmI5urgZpl9'

bidding_api_key = 'tJpwBjBDrJU2zti0buD4tEu6CteaG2'


@login_required
def home(request):
    url = 'http://127.0.0.1:8000/shopping/product_list/?api_key=' + product_api_key
    response = requests.get(url)
    products = response.json()
    print('in home')
    for product in products:
        if not Product.objects.filter(prod_name=product['prod_name'],
                                      prod_id=product['pk']).exists():
            print('added new product')

            p = Product.objects.create(prod_name=product['prod_name'],
                                       prod_id=product['pk'],
                                       description=product['description'],
                                       weight=product['weight'])
            p.save()
        else:
            p = Product.objects.filter(prod_name=product['prod_name'], prod_id=product['pk'])
            p[0].description = product['description'],
            p[0].weight = product['weight']
            p[0].save()
    prod_list = Product.objects.all()
    return render(request, 'bidding/homepage.html', {'prod_list': prod_list})


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('bidding:home')

    return render(request, 'bidding/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('bidding:home')


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('bidding:login')

    return render(request, 'bidding/register.html', {'form': form})


@login_required
def bid_list(request, p_id):
    if p_id:
        form = BiddingForm()
        bidded_list = biddedAmount.objects.filter(product__prod_id=p_id)
        return render(request, 'bidding/bid_list.html', {'bidded_list': bidded_list, 'pk': p_id, 'form': form})


def user_bid_list(request):
    bidded_list = biddedAmount.objects.filter(name=request.user)
    return render(request, 'bidding/user_bid_list.html', {'bidded_list': bidded_list})


def delete_bid_list(request, p_id, location):
    if p_id and location:
        try:
            product = Product.objects.get(pk=p_id)
            instance = biddedAmount.objects.get(product=product, name=request.user, location=location.lower())
            url = 'http://127.0.0.1:8000/shopping/delivery_bid/?api_key=' + bidding_api_key

            data = json.dumps(
                {'name': request.user.username, 'name_id': request.user.pk, 'product': product.prod_id,
                 'location': location.lower(),
                 'msg': 'delete', 'days': instance.days, 'cost': instance.cost, })
            print('sending to sportshub')

            requests.post(url=url, data=data)
            instance.delete()
        except:
            pass
        return redirect('bidding:user_bid_list')


def edit_bid_list(request, p_id, location):
    if p_id and location:
        product = Product.objects.get(pk=p_id)
        instance = biddedAmount.objects.get(product=product, name=request.user, location=location.lower())
        form = EditForm(instance=instance)
        if request.method == 'POST':
            form = EditForm(request.POST)
            if form.is_valid():
                product = Product.objects.get(pk=p_id)
                name = request.user
                days = form.cleaned_data['days']
                cost = form.cleaned_data['cost']
                instance = biddedAmount.objects.get(product=product, name=request.user, location=location.lower())
                instance.days = days
                instance.cost = cost
                instance.save()
                url = 'http://127.0.0.1:8000/shopping/delivery_bid/?api_key=' + bidding_api_key

                data = json.dumps(
                    {'name': request.user.username, 'name_id': request.user.pk, 'product': product.prod_id,
                     'days': days, 'cost': cost, 'location': location.lower()})
                requests.post(url=url, data=data)
                return redirect('bidding:user_bid_list')

        return render(request, 'bidding/user_bid.html', {'form': form})


@login_required
def user_bid(request, p_id):
    if p_id:
        form = BiddingForm()
        if request.method == 'POST':
            form = BiddingForm(request.POST)
            if form.is_valid():
                product = Product.objects.get(prod_id=p_id)
                name = request.user
                days = form.cleaned_data['days']
                cost = form.cleaned_data['cost']
                location = form.cleaned_data['location']
                if biddedAmount.objects.filter(product=product, name=request.user, location=location.lower()).exists():
                    instance = biddedAmount.objects.get(product=product, name=request.user, location=location.lower())
                    instance.days = days
                    instance.cost = cost
                    instance.save()
                else:
                    biddedAmount.objects.create(name=name, product=product, days=days,
                                                cost=cost, location=location.lower())

                url = 'http://127.0.0.1:8000/shopping/delivery_bid/?api_key=' + bidding_api_key

                data = json.dumps({'name': request.user.username, 'name_id': request.user.pk, 'product': p_id,
                                   'days': days, 'cost': cost, 'location': location.lower()})
                requests.post(url=url, data=data)
                return redirect('bidding:bid_list', p_id)
        return render(request, 'bidding/user_bid.html', {'form': form})


@api_view(['POST'])
def ordered_log(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # t = Tournaments.objects.get(name=data['tournament'])
        # data['tournament'] = t.pk

        # tournament = get_object_or_404(Tournaments, title=request.data.get('tournament'))
        product = data['product']
        name = data['name']
        pincode = data['pincode']
        product_name = data['prod_name']
        address = data['address']
        phonenum = data['phonenum']
        customer_name = data['customer_name']
        mail = data['mail']
        location = data['location']
        order_id = data['order_id']
        print('prod_id', product)
        print('name_id', name)
        print('pincode', pincode)
        print('in ordered log')
        try:

            user = biddedAmount.objects.get(product__prod_id=product, name_id=name, location=location.lower())
            print('got user')
            pending_orders.objects.create(product=product_name, address=address, pincode=pincode, phone_num=phonenum,
                                          customer=customer_name, name=user.name, mail=mail, order_id=order_id)
            print('created pending order')
            return Response({'created'}, status=status.HTTP_201_CREATED)
        except:
            print('bad request')
            return Response({'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def user_pending_orders(request):
    pendingorders = pending_orders.objects.filter(name=request.user).exclude(status='Delivered')
    return render(request, 'bidding/user_pending_orders.html', {'orders': pendingorders})


@login_required
def delivered_orders(request):
    pendingorders = pending_orders.objects.filter(name=request.user, status='Delivered')
    return render(request, 'bidding/delivered_orders.html', {'orders': pendingorders})


@login_required
def changestatus(request, pk):
    if pk:
        pending_order = pending_orders.objects.get(pk=pk)
        new_status = ''
        if pending_order.status == 'Order Received':
            pending_order.status = 'Order Shipped'
            new_status = 'Order Shipped'
        elif pending_order.status == 'Order Shipped':
            pending_order.status = 'Out for delivery'
            new_status = 'Out for delivery'
        elif pending_order.status == 'Out for delivery':
            pending_order.status = 'Delivered'
            new_status = 'Delivered'

        if new_status != '':
            subject = 'Your order status: ' + new_status
            body = '''Dear User,
                                You order with Order Id ''' + pending_order.order_id + ''' is changed its status to ''' + new_status + ''' You will receive your order soon.  
                                Thank You for ordering'''
            try:
                send_mail(subject, body, settings.EMAIL_HOST_USER, [pending_order.mail], fail_silently=True)

            except:
                pass
        pending_order.save()
        return redirect('bidding:user_pending_orders')
