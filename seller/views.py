from django.shortcuts import render

from .models import *
from store.models import Products, Category
from .forms import *


def index(request):
    if request.session.has_key('seller'):
        id = request.session['seller']
        dbuser = Sellers.objects.filter(id=id)
        products = Products.objects.filter(seller=dbuser[0])
        categories = Category.objects.all()
        if dbuser:
            context = {
                'dbuser': dbuser,
                'products':products,
                'categories': categories,
            }
            return render(request, 'seller/dashboard.html',context)
    return render(request, 'seller/index.html')


def register(request):
    if request.method == 'POST':
        MyRegisterForm = SellerDetails(request.POST)
        print(MyRegisterForm.errors)
        if MyRegisterForm.is_valid():
            name = MyRegisterForm.cleaned_data['name']
            emailid = MyRegisterForm.cleaned_data['emailid']
            contact = MyRegisterForm.cleaned_data['contact']
            address = MyRegisterForm.cleaned_data['address']
            password = MyRegisterForm.cleaned_data['password']
            dbuser = Sellers(name=name,emailid=emailid,address=address,password=password)
            dbuser.contact = contact
            dbuser.save()
            print(dbuser)

    return render(request, 'seller/register.html')


def dashboard(request):
    if request.session.has_key('seller'):
        print('yo')
        id = request.session['seller']
        dbuser = Sellers.objects.filter(id=id)
        products=Products.objects.filter(seller=dbuser[0])

        print(products)

        categories = Category.objects.all()


        if dbuser:
            context = {
                'dbuser': dbuser,
                'products': products,
                'categories': categories,
            }
            return render(request, 'seller/dashboard.html',context)
    if request.method == 'POST':
        MyLoginForm = LoginCheck(request.POST)
        if MyLoginForm.is_valid():
            emailid = MyLoginForm.cleaned_data['emailid']
            password = MyLoginForm.cleaned_data['password']
            dbuser = Sellers.objects.filter(emailid=emailid, password=password)
            print(dbuser)
            products = Products.objects.filter(seller=dbuser[0])
            if dbuser:
                if dbuser[0].verified :
                    request.session['seller'] = dbuser[0].id
                    categories = Category.objects.all()
                    context = {
                        'dbuser':dbuser,
                        'products':products,
                        'categories': categories,
                    }
                    return render(request, 'seller/dashboard.html',context)
                else:
                     return render(request, 'seller/registered.html')
    return render(request, 'seller/index.html')

def logout(request):
    try:
        del request.session['seller']
    except:
        pass
    return render(request, 'seller/index.html')


def add(request):
    if request.session.has_key('seller'):
        id = request.session['seller']
        if request.method == 'POST':

            MyLoginForm = ProductEntryForm(request.POST)
            print(MyLoginForm.errors)
            if MyLoginForm.is_valid():
                name = MyLoginForm.cleaned_data['name']
                company = MyLoginForm.cleaned_data['company']
                price = MyLoginForm.cleaned_data['price']
                availability=MyLoginForm.cleaned_data['availability']
                cat = MyLoginForm.cleaned_data['category']
                other = MyLoginForm.cleaned_data['other']

                dbuser = Sellers.objects.filter(id=id)
                if cat == "Other":
                    categ = Category()
                    categ.name = other
                    categ.save()

                if not cat == "Other":
                    category = Category.objects.filter(name=cat)
                else:
                    category = Category.objects.filter(name=other)


                if Products.objects.filter(name=name, company=company, seller=dbuser):
                    x=Products.objects.filter(name=name, company=company)[0]

                if Products.objects.filter(name=name, company=company, category=category, seller=dbuser[0]):
                    x=Products.objects.filter(name=name, company=company, category=category)[0]

                    x.price=price
                    x.availability=availability
                    x.save(update_fields=['price','availability'])
                else:
                    product = Products()
                    product.productID = "GBDP{0}{1}".format(id, Products.objects.count())
                    product.name = name
                    product.company = company
                    product.price = price
                    product.availability = availability
                    product.category = category[0]
                    product.seller = dbuser[0]
                    product.save()

                categories = Category.objects.all()
                products=Products.objects.filter(seller=dbuser[0])
                context = {
                    'dbuser': dbuser,
                    'products':products,
                    'categories': categories,
                }
                return render(request, 'seller/dashboard.html', context)

        else:
           dbuser = Sellers.objects.filter(id=id)
           mysearch=ProductSearchForm(request.GET)
           if mysearch.is_valid():
               search=mysearch.cleaned_data['searchfield']

               productlist=list(Products.objects.filter(name__icontains=search, seller=id))

               productlist=list(Products.objects.filter(name__icontains=search,seller=id))
               productlist.extend(list(Products.objects.filter(company__icontains=search,seller=id)))
               categories = Category.objects.all()


               context = {
                   'dbuser': dbuser,
                   'products': productlist,
                   'categories': categories,
               }
               return render(request, 'seller/dashboard.html', context)
           else:
               products = Products.objects.filter(seller=dbuser[0])
               categories = Category.objects.all()
               context = {
                   'dbuser': dbuser,
                   'products': products,
                   'categories': categories,
               }
               return render(request, 'seller/dashboard.html', context)




    else:
        return render(request, 'seller/index.html')
