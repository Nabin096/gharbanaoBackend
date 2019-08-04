from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_control

from designers.models import Designers
from . models import VerifiedDesigners, Products, Category, Bills, Purchases, ShippingAddress
from . forms import StoreLoginForm, VerificationForm, SearchForm


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.session.has_key('designerID'):
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)
        categories = Category.objects.all()

        if dbuser:
            vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])
            if 'cart' in request.session:
                cart = request.session['cart']
            else:
                cart = {}
            count = len(cart)
            context = {
                'dbuser': dbuser[0],
                'categories': categories,
                'cartcount': count,
            }

            if vdes:
                if not vdes[0].verified:
                    return render(request, 'store/notverified.html', context)

                return render(request, 'store/dashboard.html', context)

            VerifiedDesigners.objects.create(designer=dbuser[0])
            return render(request, 'store/notverified.html', context)

    context = {}
    return render(request, 'store/index.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    designerID = ""
    password = ""

    if request.method == "POST":
        if request.session.has_key('designerID'):
            designerID = request.session['designerID']
            dbuser = Designers.objects.filter(designerID=designerID)
            categories = Category.objects.all()
            if dbuser:
                vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])
                if 'cart' in request.session:
                    cart = request.session['cart']
                else:
                    cart = {}
                count = len(cart)
                context = {
                    'dbuser': dbuser[0],
                    'categories': categories,
                    'cartcount': count,
                }

                if vdes:
                    if not vdes[0].verified:
                        return render(request, 'store/notverified.html', { 'dbuser': dbuser[0] })

                    return render(request, 'store/dashboard.html', context)

                VerifiedDesigners.objects.create(designer=dbuser)
                return render(request, 'store/notverified.html', { 'dbuser': dbuser[0] })
        
        LoginForm = StoreLoginForm(request.POST)
        form_errors = LoginForm.errors
        print(form_errors)

        if LoginForm.is_valid():
            designerID = LoginForm.cleaned_data['designerID']
            password = LoginForm.cleaned_data['password']
            print(designerID)
            dbuser = Designers.objects.filter(designerID=designerID)

            if dbuser and check_password(password, dbuser[0].password):
                vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])
                user = dbuser[0]
                request.session['designerID'] = designerID
                categories = Category.objects.all()
                if 'cart' in request.session:
                    cart = request.session['cart']
                else:
                    cart = {}
                count = len(cart)
                context = {
                    'dbuser': user,
                    'categories': categories,
                    'cartcount': count,
                }
                if vdes:
                    if not vdes[0].verified:
                        return render(request, 'store/notverified.html', { 'dbuser': user })
                    return render(request, 'store/dashboard.html', context)

                VerifiedDesigners.objects.create(designer=dbuser[0])
                return render(request, 'store/notverified.html', { 'dbuser': user })
            if not dbuser:
                print("Not user")
                context = {
                    'error': "DesignerID or Password incorrect!"
                }
                return render(request, 'store/index.html', context)
        else:
            print("Not valid")
            return render(request, 'store/index.html', {})

    else:
        LoginForm = StoreLoginForm(request.GET)
        if request.session.has_key('designerID'):
            designerID = request.session['designerID']
            dbuser = Designers.objects.filter(designerID=designerID)
            categories = Category.objects.all()
            if 'cart' in request.session:
                cart = request.session['cart']
            else:
                cart = {}
            count = len(cart)
            if dbuser:
                vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])
                context = {
                    'dbuser': dbuser[0],
                    'categories': categories,
                    'cartcount': count,
                }
                if vdes:
                    if not vdes[0].verified:
                        return render(request, 'store/notverified.html', { 'dbuser': dbuser[0] })
                    return render(request, 'store/dashboard.html', context)

                VerifiedDesigners.objects.create(designer=dbuser[0])
                return render(request, 'store/notverified.html', { 'dbuser': dbuser[0] })
        return render(request, 'store/index.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def getverified(request):
    return render(request, 'store/getverified.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def notverified(request):
    return render(request, 'store/notverified.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verification(request):
    if not request.session.has_key('designerID'):
        context = {
            'errors': "Please login to continue"
        }
        return render(request, 'store/index.html', context)

    verificationImage = None
    if request.method == "POST":
        verform = VerificationForm(request.POST)
        print(verform.errors)

        if verform.is_valid():
            verificationImage = request.FILES['verificationImage']
            if request.session.has_key('designerID'):
                designerID = request.session['designerID']
                designer = Designers.objects.filter(designerID=designerID)
                dbuser = VerifiedDesigners.objects.filter(designer=designer[0])
                user = VerifiedDesigners.objects.get(designer=designer[0])
                user.document = verificationImage

                user.save(update_fields=['document'])

                context = {
                    'dbuser': designer
                }
                return render(request, 'store/verification.html', context)
            else:
                context = {
                    'errors': "Please login to continue"
                }
                return render(request, 'store/index.html', context)
        else:
            print("invalid form")

    else:
        verform = VerificationForm(request.GET)
        return render(request, 'store/getverified.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    try:
        del request.session['designerID']
    except:
        pass
    context = {
        'error': "You have been successfully logged out."
    }
    return render(request, 'store/index.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def myprofile(request):
    if not request.session.has_key('designerID'):
        context = {
            'errors': "Please login to continue"
        }
        return render(request, 'store/index.html', context)

    designerID = request.session['designerID']
    designer = Designers.objects.filter(designerID=designerID)

    if designer:
        verdes = VerifiedDesigners.objects.filter(designer=designer[0])
        context = {
            'dbuser': designer[0],
        }

        if not verdes[0].verified:
            return render(request, 'store/notverified.html', context)

        context = {
            'dbuser': designer[0],
            'vdes': verdes[0],
        }
        return render(request, 'store/myprofile.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def searchres(request):
    selectpicker = ""
    search = ""
    product_list = []

    if request.session.has_key('designerID'):
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)

        if dbuser:
            vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])

        SearchF = SearchForm(request.GET)
        form_errors = SearchF.errors
        print(form_errors)

        if SearchF.is_valid():
            select = SearchF.cleaned_data['select']
            search = SearchF.cleaned_data['search']
            if not select == "All Categories":
                category = Category.objects.filter(name=select)
                product_list = Products.objects.filter(category=category[0], name__icontains=search).order_by('price')

            else:
                product_list = Products.objects.filter(name__icontains=search)

        return render(request, 'store/search.html', { 'filter': product_list })


def ajaxsearch(request):
    SearchF = SearchForm(request.GET)
    form_errors = SearchF.errors
    print(form_errors)
    product_list = []
    if SearchF.is_valid():
        select = SearchF.cleaned_data['select']
        search = SearchF.cleaned_data['search']

        if not select == "All Categories":
            category = Category.objects.filter(name=select)
            product_list = Products.objects.filter(category=category[0], name__icontains=search).order_by('price')

        else:
            product_list = Products.objects.filter(name__icontains=search)

    return render(request, 'store/ajax_search.html', context={ 'filter': product_list })


def products(request, product_name):
    if request.session.has_key('designerID'):
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)

        if dbuser:
            vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])

            if not vdes[0].verified:
                return render(request, 'store/notverified.html', context={ 'dbuser': dbuser[0] })

            prod = Products.objects.filter(name=product_name)
            cat = prod[0].category.name

            return render(request, 'store/products.html', { 'category': cat, 'product': prod[0] })


def add_to_cart(request):
    if request.method == "POST":
        if 'cart' in request.session:
            cart = request.session['cart']
        else:
            cart = {}
        id = request.POST.get("id")
        product = Products.objects.filter(productID=id)
        qty = request.POST.get("qty")
        if product[0].id in cart:
            cart[product[0].id] += qty
        else:
            cart[product[0].id] = qty
        request.session['cart'] = cart
        return HttpResponse("Added to cart")


def view_cart(request):
    if request.session.has_key('designerID'):
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)

        if dbuser:
            vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])

            if vdes:
                if not vdes[0].verified:
                    return render(request, 'store/notverified.html', { 'dbuser': dbuser[0] })

                if 'cart' in request.session:
                    cart = request.session['cart']
                else:
                    cart = {}

                products = {}
                if cart:
                    for id in cart:
                        product = Products.objects.get(productID=id)
                        products[cart[id]] = product

                context = {
                    'dbuser': dbuser[0],
                    'products': products,
                }
                return render(request, 'store/cart.html', context)


def del_item(request):
    if request.method == "POST":
        id = request.POST.get("id")

        if 'cart' in request.session:
            cart = request.session['cart']
        else:
            cart = {}

        if id in cart:
            del cart[id]

        request.session['cart'] = cart
        return HttpResponse("item deleted")


def update_item(request):
    if request.method == "POST":
        id = request.POST.get("id")
        qty = request.POST.get("qty")

        if 'cart' in request.session:
            cart = request.session['cart']
        else:
            cart = {}

        if id in cart:
            cart[id] = qty

        request.session['cart'] = cart
        return HttpResponse("item updated")


def checkout(request):
    if request.session.has_key('designerID'):
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)

        if dbuser:
            vdes = VerifiedDesigners.objects.filter(designer=dbuser[0])

            if vdes:
                if not vdes[0].verified:
                    return render(request, 'store/notverified.html', { 'dbuser': dbuser[0] })

                if 'cart' in request.session:
                    cart = request.session['cart']
                else:
                    cart = {}

                products = {}
                if cart:
                    for id in cart:
                        product = Products.objects.get(productID=id)
                        products[cart[id]] = product

                address = ShippingAddress.objects.filter(designer = dbuser[0])
                if not address:
                    return render(request, 'store/addaddress.html', { 'dbuser': dbuser[0] })

                context = {
                    'dbuser': dbuser[0],
                    'products': products,
                    'address': address[0],
                }
                return render(request, 'store/checkout.html', context)


def delcart(request):
    if 'cart' in request.session:
        request.session['cart'] = {}
        return HttpResponse("cart deleted")
