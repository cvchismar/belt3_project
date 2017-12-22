# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

#views for login-registration

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    #once validations entered in managermodel: "if result[0]: success --- else: fail validation"
    if result[0]:
        #success
        request.session['user_id'] = result[1].id #this means they are logged in
        #can only get request.session from views.py not models.py
        return redirect ("/display")
    else:
    #if fail then show the errors on page
        for error in result[1]:
            messages.error(request, error)
        return redirect ("/")

def login(request):
    result = User.objects.validate_login(request.POST)
    #once validations entered in managermodel: "if result[0]: success --- else: fail validation"
    if result[0]:
        #success
        request.session['user_id'] = result[1].id #this means they are logged in
        #can only get request.session from views.py not models.py
        return redirect ("/display")
    else:
    #if fail then show the errors on page
        for error in result[1]:
            messages.error(request, error)
    return redirect("/")  

# Create your views here.
def display(request):
    context ={
        'users': User.objects.get(id=request.session['user_id']),
        'items' : Wish_Items.objects.filter(joined_by=User.objects.get(id=request.session['user_id'])),
        'others_items': Wish_Items.objects.exclude(joined_by=User.objects.get(id=request.session['user_id']))
    }
    return render(request, 'display.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
    return render(request, 'add_item.html')

def create(request):
    if request.method == 'POST':
        errors = Wish_Items.objects.product_validation(request.POST)
        if len(errors):  # if there's errors -- see models.py for error list!
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/add')
        else:
            user = User.objects.get(id=request.session['user_id'])
            product = Wish_Items.objects.create(
                product = request.POST['product'],
                created_by=user
            )
            product.joined_by.add(user)
            product.save()
            return redirect('/display')
    else:
        return redirect('/display')

def join(request, product_id):
    user = User.objects.get(id=request.session['user_id'])
    product = Wish_Items.objects.get(id=product_id)
    product.joined_by.add(user)
    product.save()
    return redirect('/display')

def info(request, product_id):
    product = Wish_Items.objects.get(id=product_id)
    context = {
        'product': product,
        'other_users' : User.objects.exclude(created_product__created_by=product.created_by)
    }
    return render(request, 'wish_item.html', context)

def delete(request, product_id):
    user = User.objects.get(id=request.session['user_id'])
    Wish_Items.objects.filter(id=product_id).delete()
    return redirect('/display')

def leave(request, product_id):
    user = User.objects.get(id=request.session['user_id'])
    product = Wish_Items.objects.get(id=product_id)
    product.joined_by.remove(user)
    product.save()
    return redirect('/display')


    #  user = User.objects.get(id=request.session['user_id'])
    # Wish_Items.objects.filter(id=product_id).delete()