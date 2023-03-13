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
    """Returns the total count of items in the user's cart.

    Args:
        request (HttpRequest): the request object containing the GET query parameter.

    Returns:
        int: The total number of items in the user's cart.
    """
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return total_items


def search(request):
    """
    Returns a search page with the products matching the given query, or a warning message if no products match.

    Args:
        request (HttpRequest): the request object containing the GET query parameter.

    Returns:
        HttpResponse: the search page with the matching products and query, or a warning message if no products match.

    """
    query = request.GET["query"]
    if len(query) > 70 or len(query) < 1:
        allprods = Product.objects.none()
    else:
        allprodtitle = Product.objects.filter(title__icontains=query)
        allprodcat = Product.objects.filter(category__icontains=query)
        allprodbrand = Product.objects.filter(brand__icontains=query)
        allprods = allprodtitle | allprodcat | allprodbrand.order_by("?")
    if allprods.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    print(allprods)
    return render(request, "app/search.html", {"context": allprods, "query": query})


class HomeView(View):
    def get(self, request):
        """
        Return the home page with the list of products for top wear, bottom wear, mobile and laptop.

        Args:
            request (HttpRequest): The HTTP request object representing the current request.

        Returns:
            HttpResponse: The HTTP response object with the rendered home.html template containing the list of products for top wear, bottom wear, mobile, and laptop, as well as the total number of items in the user's cart.
        """

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
        """
        Retrieves a Product object with the specified primary key (pk) and renders the
        app/productdetail.html template with the retrieved product, a boolean flag indicating
        if the product is already in the cart of the authenticated user, and the total number
        of items in the cart.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the product to retrieve.

        Returns:
            HttpResponse: A rendered HTML response that displays the details of the product with
            the specified primary key, including a boolean flag indicating if it's already in the
            cart of the authenticated user, and the total number of items in the cart.
        """

        product = Product.objects.get(pk=pk)
        already_in_cart = False
        if request.user.is_authenticated:
            already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)  # type: ignore
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
    """
    Fetches and displays mobile products based on the provided data parameter.

    Args:
        request (HttpRequest): The HTTP request object.
        data (str, optional): The filter criteria for the mobile products. Default is None.

    Returns:
        HttpResponse: An HTTP response that renders the mobile.html template, passing in a context dictionary
        containing the filtered mobile products and the total number of items in the user's cart.
    """
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
    """
    Returns a list of laptops based on the given filter criteria.

    If no filter criteria is provided (i.e., data is None).

    Args:
        request: The HTTP request object.
        data(str, optional): filters the laptops by the specified criteria, which can be one of the following:
            - "Hp", "Dell", "Acer", "Asus", "Lenovo", or "Apple": filters by brand.
            - "Below40000": filters by price, showing laptops with a discounted price below 40,000.
            - "40000-100000": filters by price, showing laptops with a discounted price between 40,000 and 100,000.
            - "Above100000": filters by price, showing laptops with a discounted price above 100,000.

    Returns:
        A rendered template of the "laptop.html" file, with the following context variables:
        - "context": a list of laptops that match the specified filter criteria.
        - "total_items_count": the total number of items in the user's cart.
    """
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
    return render(request, "app/laptop.html", {"context": laptops, "total_items_count": cart_items_count(request)})  # type: ignore


def tv(request, data=None):
    """
    Fetches and displays television products based on the provided data parameter.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.
        data (str, optional): The filter criteria for the television products. Default is None.

    Returns:
        HttpResponse: An HTTP response that renders the laptop.html template, passing in a context dictionary
        containing the filtered television products and the total number of items in the user's cart.
    """
    if data == None:
        tvs = Product.objects.filter(category="TV")
    elif data == "LG" or data == "Sony" or data == "Samsung":
        tvs = Product.objects.filter(category="TV").filter(brand=data)
    elif data == "Below50000":
        tvs = Product.objects.filter(category="TV").filter(discounted_price__lt=50000)
    elif data == "50000-100000":
        tvs = Product.objects.filter(category="TV").filter(
            discounted_price__range=(50000, 100000)
        )
    elif data == "Above100000":
        tvs = Product.objects.filter(category="TV").filter(discounted_price__gt=100000)
    return render(request, "app/tv.html", {"context": tvs, "total_items_count": cart_items_count(request)})  # type: ignore


def clothing(request, data=None):
    """
    View function for displaying clothing products.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.
        data(str, optional) string parameter used for filtering products. Valid values include:
            - "TW": Filter products by top-wear category.
            - "BW": Filter products by bottom-wear category.
            - "Below 1000": Filter products with discounted price less than 1000.
            - "500-1000": Filter products with discounted price between 500 and 1000 (inclusive).
            - "Above1000": Filter products with discounted price greater than 1000.

    Returns:
        HttpResponse object with rendered clothing.html template and a dictionary containing
        the filtered clothing products under the 'clothing' key.
    """
    top = Product.objects.filter(category="TW")
    bottom = Product.objects.filter(category="BW")
    cloths = top | bottom.order_by("?")

    if data == None:
        cloths = cloths

    elif data == "TW" or data == "BW":
        cloths = cloths.filter(category=data)

    elif data == "Below 1000":
        cloths = cloths.filter(discounted_price__lt=1000)
    elif data == "500-1000":
        cloths = cloths.filter(discounted_price__range=(500, 1000))
    elif data == "Above1000":
        cloths = cloths.filter(discounted_price__gt=1000)
    return render(
        request,
        "app/clothing.html",
        {
            "clothing": cloths,
        },
    )  # type: ignore


def watches(request, data=None):
    """
    Renders the 'app/watch.html' template with a list of watches based on the provided filters.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.
        data (str, optional): A string that determines the type of watch list to display. If not provided or None, all watches in the "WW" category are displayed. Otherwise, the following values are recognized:

            - "Casio": displays watches from the "Casio" brand.
            - "Diesel": displays watches from the "Diesel" brand.
            - "Fossil": displays watches from the "Fossil" brand.
            - "Titan": displays watches from the "Titan" brand.
            - "Below10000": displays watches with a discounted price less than 10000.
            - "10000-20000": displays watches with a discounted price between 10000 and 20000.
            - "Above20000": displays watches with a discounted price greater than 20000.

    Returns:
        A rendered HTTP response containing the 'app/watch.html' template with the following context:

        - 'context': a list of watch objects that match the provided filter (or all watches in the "WW" category if no filter is provided).
        - 'total_items_count': the total number of items in the user's shopping cart.
    """
    if data == None:
        watch = Product.objects.filter(category="WW")
    elif data == "Casio" or data == "Diesel" or data == "Fossil" or data == "Titan":
        watch = Product.objects.filter(category="WW").filter(brand=data)
    elif data == "Below10000":
        watch = Product.objects.filter(category="WW").filter(discounted_price__lt=10000)
    elif data == "10000-20000":
        watch = Product.objects.filter(category="WW").filter(
            discounted_price__range=(10000, 20000)
        )
    elif data == "Above20000":
        watch = Product.objects.filter(category="WW").filter(discounted_price__gt=20000)
    return render(request, "app/watch.html", {"context": watch, "total_items_count": cart_items_count(request)})  # type: ignore


def shoe(request, data=None):
    """
    Renders the shoes template based on the given filter. If no filter is provided,
    then all shoes under the category 'SH' are shown.

    Parameters:
    request (HttpRequest): The HTTP request object representing the current request.
    data (str, optional): The filter for the shoes. Default is None.

    Returns:
    HttpResponse: The rendered shoes template.

    """
    if data == None:
        shoes = Product.objects.filter(category="SH")
    elif data == "Nike" or data == "Reebok":
        shoes = Product.objects.filter(category="SH").filter(brand=data)
    elif data == "Below3000":
        shoes = Product.objects.filter(category="SH").filter(discounted_price__lt=3000)
    elif data == "3000-10000":
        shoes = Product.objects.filter(category="SH").filter(
            discounted_price__range=(3000, 10000)
        )
    elif data == "Above10000":
        shoes = Product.objects.filter(category="SH").filter(discounted_price__gt=10000)
    return render(request, "app/shoes.html", {"context": shoes, "total_items_count": cart_items_count(request)})  # type: ignore


@login_required
def add_to_cart(request):
    """
    Adds the specified product to the cart of the currently logged in user.

    Parameters:
        request (HttpRequest): The HTTP request object containing the user and product information.

    Returns:
        HttpResponseRedirect: A redirect response to the cart page.

    """
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    """
    Displays the user's shopping cart with the total amount and number of items.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.

    Returns:
        render: The rendered HTML template with the user's shopping cart.

    Raises:
        None

    Decorators:
        @login_required: Ensures that the user is authenticated before accessing the view.
    """
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
    """
    Increments the quantity of a product in the user's cart and returns JSON response with the updated quantity, cart subtotal amount, and total amount including shipping.

    Args:
    request (HttpRequest): The HTTP request object representing the current request.

    Returns:
    JsonResponse: A JSON response containing the following keys:
            - quantity (int): The updated quantity of the product in the cart.
            - amount (float): The subtotal amount of the cart (excluding shipping).
            - total_amount (float): The total amount of the cart (including shipping).

    """
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
    """
    Dencrements the quantity of a product in the user's cart and returns JSON response with the updated quantity, cart subtotal amount, and total amount including shipping.

    Args:
    request (HttpRequest): The HTTP request object representing the current request.

    Returns:
    JsonResponse: A JSON response containing the following keys:
            - quantity (int): The updated quantity of the product in the cart.
            - amount (float): The subtotal amount of the cart (excluding shipping).
            - total_amount (float): The total amount of the cart (including shipping).

    """
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
    """
    Removes the product in the user's cart and returns JSON response with the cart subtotal amount, and total amount including shipping.

    Args:
    request (HttpRequest): The HTTP request object representing the current request.

    Returns:
    JsonResponse: A JSON response containing the following keys:
            - amount (float): The subtotal amount of the cart (excluding shipping).
            - total_amount (float): The total amount of the cart (including shipping).

    """
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

@login_required
def buy_now(request):
    """
    Adds a product to the user's cart and redirects to the checkout page.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.

    Returns:
        HttpResponseRedirect: A redirect to the checkout page.

    """
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect("/checkout")


@login_required
def checkout(request):
    """
    Process checkout for authenticated user.

    Checks if the user is authenticated using @login_required decorator.
    Calculates the total amount for the items in the user's cart including shipping costs.
    Renders the checkout page with user's address, total amount, cart products and total items count.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.

    Returns:
        HttpResponse: The response object containing the rendered checkout page.

    """
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
    """
    Marks the cart items as ordered and redirects to the orders page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect response to the orders page.

    """
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
    """
    Renders the address page for a logged-in user.

    Args:
        request(HttpRequest): An HttpRequest object representing the current request.

    Returns:
        HttpResponse: An HttpResponse object that renders the address.html template with the following context variables:
                    - 'adrs': A QuerySet of Customer objects filtered by the current user.
                    - 'active': A string representing the CSS class for the active button.
                    - 'total_items_count': An integer representing the total number of items in the user's cart.

    """
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
    """
    A view for handling customer registration form submissions.

    This view provides GET and POST methods for rendering and processing
    the customer registration form. Upon successful form submission, a
    success message is displayed and the user is redirected to the home page.

    Methods:
        get: Renders the customer registration form.
        post: Processes the customer registration form and saves the data to the database.

    """

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
    """
    View class that displays and updates customer profile information.

    This view class requires users to be logged in before accessing it by using the login_required
    method decorator. It provides two methods, get() and post(), for rendering the profile form and
    updating the customer profile, respectively.

    Attributes:
    N/A

    Methods:
    get(request): Renders the customer profile form with a blank CustomerProfileForm instance.
    post(request): Updates the customer profile information based on the data provided by the user in the submitted
                CustomerProfileForm. If the form is valid, it saves the data to the database and displays a success message.

    """

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
    """
    Renders a page with a list of orders placed by the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        A rendered template (HttpResponse) that displays a list of orders
        placed by the logged-in user, along with the total number of items
        in their cart.

    """
    order = PlacedOrder.objects.filter(user=request.user)
    return render(
        request,
        "app/orders.html",
        {"orders": order, "total_items_count": cart_items_count(request)},
    )
