from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import *

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "product-detail/<int:pk>",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("search/", views.search, name="search"),

    path("mobile/", views.mobile, name="mobile"),
    path("mobile/<slug:data>", views.mobile, name="mobile_flt"),

    path("laptop/", views.laptop, name="laptop"),
    path("laptop/<slug:data>", views.laptop, name="laptop_flt"),

    path("tv/", views.tv, name="tv"),
    path("tv/<slug:data>", views.tv, name="tv_flt"),

    path("clothing/", views.clothing, name="clothing"),
    path("clothing/<slug:data>", views.clothing, name="clothing_flt"),

    path("shoes/", views.shoe, name="shoes"),
    path("shoes/<slug:data>", views.shoe, name="shoes_flt"),

    path("watch/", views.watches, name="watch"),
    path("watch/<slug:data>", views.watches, name="watch_flt"),

    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"), #type: ignore
    path("pluscart/", views.plus_cart), #type: ignore
    path("minuscart/", views.minus_cart), #type: ignore
    path("removecart/", views.remove_cart), #type: ignore
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("orders/", views.orders, name="orders"),
    path("checkout/", views.checkout, name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path("buynow/", views.buy_now, name="buynow"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="app/password_reset.html", form_class=PasswordResetForm
        ),
        name="passwordreset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="app/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="app/password_reset_confirm.html",
            form_class=PasswordResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="app/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "passwordchange/",
        auth_views.PasswordChangeView.as_view(
            template_name="app/passwordchange.html",
            form_class=PasswordChangeForm,
            success_url="/passwordchangedone/",
        ),
        name="passwordchange",
    ),
    path(
        "passwordchangedone/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="app/passwordchangedone.html"
        ),
        name="passwordchangedone",
    ),
    path(
        "registration/",
        views.CustomerRegistrationFormView.as_view(),
        name="customerregistration",
    ),
    path(
        "accounts/login",
        auth_views.LoginView.as_view(
            template_name="app/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
