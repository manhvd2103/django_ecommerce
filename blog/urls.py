from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("blogs/", views.blogs_view, name="blogs"),
    path("blog_detail/<str:slug>/", views.blog_detail_view, name="blog_detail"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("shopping_detail/", views.shopping_detail_view, name="shopping_detail"),
    path("shopping_grid/", views.shopping_grid_view, name="shopping_grid"),
    path("shopping_cart/", views.shopping_cart_view, name="shopping_cart"),
]

