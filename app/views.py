from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def cart_items_count(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return total_items


def search(request):
    query = request.GET["query"]
    if len(query) > 78:
        allprods = Product.objects.none()
    else:
        allprodtitle = Product.objects.filter(title__icontains=query)
        allprodcat = Product.objects.filter(category__icontains=query)
        allprodbrand = Product.objects.filter(brand__icontains=query)
        allprods = allprodtitle.union(allprodcat, allprodbrand)
    if allprods.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {"allprods": allprods, "query": query}
    return render(request, "app/search.html", params)


class HomeView(View):
    def get(self, request):
        topwear = Product.objects.filter(category="TW")
        bottomwear = Product.objects.filter(category="BW")
        mobile = Product.objects.filter(category="M")
        laptop = Product.objects.filter(category="L")
        # if request.user.is_authenticated:
        #     total_items = len(Cart.objects.filter(user=request.user))

        return render(
            request,
            "app/home.html",
            {
                "topwear": topwear,
                "bottomwear": bottomwear,
                "mobile": mobile,
                "laptop": laptop,
                "total_items_count": cart_items_count(request),
            },
        )


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        already_in_cart = False
        if request.user.is_authenticated:
            already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)#type: ignore
            ).exists()
        return render(
            request,
            "app/productdetail.html",
            {
                "product": product,
                "already_in_cart": already_in_cart,
                "total_items_count": cart_items_count(request),
            },
        )


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif data == "Redmi" or data == "Samsung" or data == "Realme":
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == "Below10000":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__lt=10000
        )
    elif data == "10000-20000":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__range=(10000, 20000)
        )
    elif data == "Above10000":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__gt=20000
        )
    return render(request, "app/mobile.html", {"context": mobiles, "total_items_count": cart_items_count(request)})  # type: ignore


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category="L")
    elif (
        data == "Hp"
        or data == "Dell"
        or data == "Acer"
        or data == "Asus"
        or data == "Lenovo"
        or data == "Apple"
    ):
        laptops = Product.objects.filter(category="L").filter(brand=data)
    elif data == "Below40000":
        laptops = Product.objects.filter(category="L").filter(
            discounted_price__lt=40000
        )
    elif data == "40000-100000":
        laptops = Product.objects.filter(category="L").filter(
            discounted_price__range=(40000, 100000)
        )
    elif data == "Above100000":
        laptops = Product.objects.filter(category="L").filter(
            discounted_price__gt=100000
        )
    return render(request, "app/laptop.html", {"context": laptops, "total_items_count": cart_items_count(request)}) #type: ignore


def clothing(request, data=None):
    top = Product.objects.filter(category="TW")
    bottom = Product.objects.filter(category="BW")
    cloths = top | bottom.order_by("?")

    if data == None:
        cloths = cloths

    elif data == "Below 1000":
        cloths = cloths.filter(discounted_price__lt=1000)
    elif data == "500-1000":
        cloths = cloths.filter(discounted_price__range=(500, 1000))
    elif data == "Above1000":
        cloths = cloths.filter(discounted_price__gt=1000)
    # category = ("TW", "BW")
    # cloths = product_brands(request, category=category, data=data, price=500)
    return render(
        request,
        "app/clothing.html",
        {
            "clothing": cloths,
        },
    )  # type: ignore


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_prod = [p for p in cart]

        if cart_prod:
            for p in cart_prod:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
                total_amount = amount + shipping_amount
    return render(request, "app/cart.html", {"carts": cart, "amount": amount, "total_amount": total_amount, "total_items_count": cart_items_count(request)})  # type: ignore


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_prod = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_prod:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "total_amount": total_amount,  # type: ignore
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_prod = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_prod:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "total_amount": total_amount,  # type: ignore
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_prod = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_prod:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {"amount": amount, "total_amount": total_amount}  # type: ignore
        return JsonResponse(data)


def buy_now(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect("/checkout")


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_prod = [p for p in cart_items]
    for p in cart_prod:
        tempamount = p.quantity * p.product.discounted_price
        amount += tempamount
        total_amount = amount + shipping_amount
    return render(
        request,
        "app/checkout.html",
        {
            "add": add,
            "total_amount": total_amount,
            "cart_prods": cart_prod,
            "total_items_count": cart_items_count(request),
        },
    )


@login_required
def payment_done(request):
    user = request.user
    customer = Customer.objects.get(id=request.GET.get("custid"))
    cart = Cart.objects.filter(user=user)
    for item in cart:
        PlacedOrder(
            user=user, customer=customer, product=item.product, quantity=item.quantity
        ).save()
        item.delete()

    return redirect("orders")


@login_required
def address(request):
    adrs = Customer.objects.filter(user=request.user)
    return render(
        request,
        "app/address.html",
        {
            "adrs": adrs,
            "active": "btn-primary",
            "total_items_count": cart_items_count(request),
        },
    )


class CustomerRegistrationFormView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "User Registered Successfully!!")
            form.save()
        return render(request, "app/customerregistration.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request,
            "app/profile.html",
            {
                "form": form,
                "active": "btn-primary",
                "total_items_count": cart_items_count(request),
            },
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            pf_data = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            pf_data.save()
            messages.success(request, "Profile Updated successfully!!")
        return render(
            request,
            "app/profile.html",
            {
                "form": form,
                "active": "btn-primary",
                "total_items_count": cart_items_count(request),
            },
        )


@login_required
def orders(request):
    order = PlacedOrder.objects.filter(user=request.user)
    return render(
        request,
        "app/orders.html",
        {"orders": order, "total_items_count": cart_items_count(request)},
    )
