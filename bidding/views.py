import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse

from bidding.models import Product, biddedAmount
from .forms import RegisterForm, BiddingForm


@login_required
def home(request):
    url = 'http://127.0.0.1:8000/shopping/product_list'
    response = requests.get(url)
    products = response.json()

    for product in products:
        if not Product.objects.filter(prod_name=product['prod_name'], prod_id=product['pk']).exists():
            p = Product.objects.create(prod_name=product['prod_name'],
                                       prod_id=product['pk'],
                                       description=product['description'],
                                       weight=product['weight'])
            p.save()

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
        bidded_list = biddedAmount.objects.filter(product__pk=p_id)
        return render(request, 'bidding/bid_list.html', {'bidded_list': bidded_list, 'pk': p_id})


def user_bid_list(request):
    bidded_list = biddedAmount.objects.filter(name=request.user)
    return render(request, 'bidding/user_bid_list.html', {'bidded_list': bidded_list, })


def delete_bid_list(request, p_id, pincode):
    if p_id and pincode:
        try:
            product = Product.objects.get(pk=p_id)
            instance = biddedAmount.objects.get(product=product, name=request.user, pincode=pincode)
            url = 'http://127.0.0.1:8000/shopping/delivery_bid/'

            data = json.dumps(
                {'name': request.user.username, 'name_id': request.user.pk, 'product': p_id, 'pincode': pincode,
                 'msg': 'delete'})
            requests.post(url=url, data=data)
            instance.delete()
        except:
            pass
        return redirect('bidding:user_bid_list')


def edit_bid_list(request, p_id, pincode):
    if p_id and pincode:
        product = Product.objects.get(pk=p_id)
        instance = biddedAmount.objects.get(product=product, name=request.user, pincode=pincode)
        form = BiddingForm(instance=instance)
        if request.method == 'POST':
            form = BiddingForm(request.POST)
            if form.is_valid():
                product = Product.objects.get(pk=p_id)
                name = request.user
                days = form.cleaned_data['days']
                cost = form.cleaned_data['cost']
                pincode = form.cleaned_data['pincode']
                if biddedAmount.objects.filter(product=product, name=request.user, pincode=pincode).exists():
                    instance = biddedAmount.objects.get(product=product, name=request.user, pincode=pincode)
                    instance.days = days
                    instance.cost = cost
                    instance.save()
                else:
                    biddedAmount.objects.create(name=name, product=product, days=days,
                                                cost=cost, pincode=pincode)

                url = 'http://127.0.0.1:8000/shopping/delivery_bid/'

                data = json.dumps({'name': request.user.username, 'name_id': request.user.pk, 'product': p_id,
                                   'days': days, 'cost': cost, 'pincode': pincode})
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
                product = Product.objects.get(pk=p_id)
                name = request.user
                days = form.cleaned_data['days']
                cost = form.cleaned_data['cost']
                pincode = form.cleaned_data['pincode']
                if biddedAmount.objects.filter(product=product, name=request.user, pincode=pincode).exists():
                    instance = biddedAmount.objects.get(product=product, name=request.user, pincode=pincode)
                    instance.days = days
                    instance.cost = cost
                    instance.save()
                else:
                    biddedAmount.objects.create(name=name, product=product, days=days,
                                                cost=cost, pincode=pincode)

                url = 'http://127.0.0.1:8000/shopping/delivery_bid/'

                data = json.dumps({'name': request.user.username, 'name_id': request.user.pk, 'product': p_id,
                                   'days': days, 'cost': cost, 'pincode': pincode})
                requests.post(url=url, data=data)
                return redirect('bidding:bid_list', p_id)
        return render(request, 'bidding/user_bid.html', {'form': form})
