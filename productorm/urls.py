"""
URL configuration for productorm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from productormapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("userlogin/", views.userlogin, name="userlogin"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("register/", views.register, name="register"),
    path("cart/", views.cart, name="cart"),
    path("range_view/", views.range_view, name="range_view"),
    path("clothsview/", views.clothslistview, name="clothslistview"),
    path("shoeslistview/", views.shoeslistview, name="shoeslistview"),
    path("mobilelistview/", views.mobilelistview, name="mobilelistview"),
    path("searchproduct/", views.searchproduct, name="searchproduct"),
    path("allsortedorderview/", views.allsortedorderview, name="allsortedorderview"),
    path(
        "remove_from_cart/<int:product_id>",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "remove_from_order/<int:product_id>",
        views.remove_from_order,
        name="remove_from_order",
    ),
    path("add_to_cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("updateqty/<qv>/<product_id>", views.updateqty, name="updateqty"),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('showorders/',views.showorders,name='showorders'),
    path('insertproducts/',views.insertproducts,name='insertproducts'),
    path('updateproducts/<int:product_id>',views.updateproducts,name='updateproducts'),
    path('viewregisterproduct/',views.viewregisterproduct,name='viewregisterproduct'),
    path('deleteproducts/<int:product_id>',views.deleteproducts,name='deleteproducts'),
    path('makepayment/',views.makepayment,name='makepayment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
