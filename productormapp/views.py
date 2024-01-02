from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import Product, Cart,Order
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
import razorpay
from .forms import ViewProduct


def about(req):
    return render(req,'about.html')

def contact(req):
    return render(req,'contact.html')

# Create your views here.
def index(req):
    username = req.user.username
    allproducts = Product.objects.all()
    context = {"allproducts": allproducts, "username": username}
    return render(req, "index.html", context)


def register(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "register.html", context)
        elif ucpass != upass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "register.html", context)
        else:
            try:
                u = User.objects.create(username=uname, password=upass)
                u.set_password(upass)
                u.save()
                return redirect("/userlogin")
            except Exception:
                context["errmsg"] = "User already exists"
                return render(req, "register.html", context)
    else:
        return render(req, "register.html")


def userlogin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" and upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "login.html", context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(req, u)
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "login.html", context)
    else:
        return render(req, "login.html")


def userlogout(req):
    logout(req)
    return redirect("/")


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    allproducts = get_object_or_404(Product, product_id=product_id)
    cart_item, created = Cart.objects.get_or_create(product_id=allproducts, userid=user)
    if not created:
        cart_item.qty += 1
    else:
        cart_item.qty = 1
    cart_item.save()

    return redirect("/cart")


def cart(req):
    if req.user.is_authenticated:
        username = req.user.username
        allcarts = Cart.objects.filter(userid=req.user.id)
        total_price = 0
        for x in allcarts:
            total_price += x.product_id.price * x.qty
        length = len(allcarts)
        context = {
            "cart_items": allcarts,
            "total": total_price,
            "items": length,
            "username": username,
        }
        return render(req, "cart.html", context)
    else:
        allcarts = Cart.objects.filter(userid=req.user.id)
        total_price = 0
        for x in allcarts:
            total_price += x.product_id.price * x.qty
        length = len(allcarts)
        context = {
            "cart_items": allcarts,
            "total": total_price,
            "items": length,
        }
        return render(req, "cart.html", context)

def placeorder(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        user=None
    # user=request.user.id
    allcarts = Cart.objects.filter(userid=user)
    # order_id=random.randrange(1000,9999)
    # for x in allcarts:
    #     o=Order.objects.create(order_id=order_id,product_id=x.product_id,userid=x.userid,qty=x.qty)
    #     o.save()
    #     x.delete()
    # orders=Order.objects.filter(userid=user)
    total_price = 0
    length = len(allcarts)
    for x in allcarts:
        total_price += x.product_id.price * x.qty
    context={}
    context['cart_items']=allcarts
    context['total']=total_price
    context['items']=length
    context['username']=user
    return render(request,'placeorder.html',context)

def showorders(req):
    if req.user.is_authenticated:
        user=req.user
        allorders = Order.objects.filter(userid=user)
        context = {"allorders": allorders, "username": user}
        return render(req, "orders.html", context)
    else:
        user=None
        return redirect('/userlogin')


def makepayment(request):
    if request.user.is_authenticated:
        user=request.user
        order_id=random.randrange(1000,9999)
        allcarts = Cart.objects.filter(userid=user)
        for x in allcarts:
            o=Order.objects.create(order_id=order_id,product_id=x.product_id,userid=x.userid,qty=x.qty)
            o.save()
            x.delete()
        orders=Order.objects.filter(userid=user)
        total_price = 0
        for x in orders:
            total_price += x.product_id.price * x.qty
            oid=x.order_id
        client = razorpay.Client(auth=("rzp_test_UlbO35bHqiCAbm", "nceh3T6nR5SEq6TfacTEM7gt"))
        data = { "amount": total_price*100, "currency": "INR", "receipt": str(oid) }
        payment = client.order.create(data=data)
        # print(payment)
        context={}
        context['data']=payment
        context['amount']=payment
        return render(request,'payment.html',context)
    else:
        user=None
        return redirect('/userlogin')
    

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    cart_item = Cart.objects.filter(product_id=product_id, userid=user)
    cart_item.delete()
    return redirect("/cart")

def remove_from_order(request, product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    orders=Order.objects.filter(userid=user,product_id=product_id)
    orders.delete()
    return redirect("/cart")

def range_view(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        r1 = request.POST.get("min")
        r2 = request.POST.get("max")
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts = Product.prod.get_price_range(r1, r2)
            context = {"allproducts": allproducts}
            return render(request, "index.html", context)
        else:
            allproducts = Product.objects.all()
            context = {"allproducts": allproducts}
            return render(request, "index.html", context)


def mobilelistview(request):
    if request.method == "GET":
        allproducts = Product.prod.mobile_list()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)


def clothslistview(request):
    if request.method == "GET":
        allproducts = Product.prod.cloths_list()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)


def shoeslistview(request):
    if request.method == "GET":
        allproducts = Product.prod.shoes_list()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)
    else:
        allproducts = Product.object.all()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)


def allsortedorderview(request):
    sort_option = request.GET.get("sort")
    if sort_option == "high_to_low":
        allproducts = Product.objects.order_by("-price")
    elif sort_option == "low_to_high":
        allproducts = Product.objects.order_by("price")
    else:
        allproducts = Product.objects.all()

    context = {"allproducts": allproducts}
    return render(request, "index.html", context)


def searchproduct(request):
    query = request.GET.get("q")
    if query:
        allproducts = Product.objects.filter(
            Q(product_name__icontains=query)
            | Q(category__icontains=query)
            | Q(price__icontains=query)
        )
    else:
        allproducts = Product.objects.all()
    context = {"allproducts": allproducts, "query": query}
    return render(request, "index.html", context)


def updateqty(request, qv, product_id):
    allcarts = Cart.objects.filter(product_id=product_id)
    if qv == "1":
        totol = allcarts[0].qty + 1
        allcarts.update(qty=totol)
    else:
        if allcarts[0].qty > 1:
            totol = allcarts[0].qty - 1
            allcarts.update(qty=totol)
        else:
            allcarts = Cart.objects.filter(product_id=product_id)
            allcarts.delete()

    return redirect("/cart")


def viewregisterproduct(request):
    if request.user.is_authenticated:
        user = request.user
        allproducts=Product.objects.filter()
        context={'allproducts':allproducts,'username':user}
        return render(request,"viewregisterproduct.html",context)
    else:
        user = None
        return redirect('/userlogin')

def deleteproducts(request, product_id):
    m = Product.objects.filter(bookID =  product_id);
    m.delete()
    return redirect('/viewregisterproduct')

def insertproducts(request):
    if request.user.is_authenticated:
        user=request.user
        if request.method == "GET":
            # Render the form for GET requests
            form = ViewProduct()
            return render(request, 'insertproducts.html', {'form': form,"username":user})
        else:
            # Process form data for POST requests
            form = ViewProduct(request.POST ,request.FILES or None)
            if form.is_valid():
                # Save the form data to the model if valid
                form.save()
                return redirect("/viewregisterproduct")  # Successful, redirect
            else:
                # Form data is not valid, handle errors or display them
                return render(request, 'insertproducts.html', {'form': form,"username":user})
    else:
        # Redirect to login if the user is not authenticated
        return redirect("/userlogin")
    
def updateproducts(request, product_id):
    if request.user.is_authenticated:
        user=request.user
        products = get_object_or_404(Product, product_id=product_id)

        if request.method == 'POST':
            form = ViewProduct(request.POST,request.FILES, instance=ViewProduct)
            if form.is_valid():
                form.save()
                return redirect('/viewregisterproduct')  
        else:
            form = ViewProduct(instance=ViewProduct)

        context = {
            'form': form,
            'data': [products],
            'username':user,
        }

        return render(request, "updateproducts.html", context)
    else:
        return redirect('/userlogin')