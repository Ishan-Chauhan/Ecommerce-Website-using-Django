from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "store" 

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('track/', views.track, name='track'),
    path('category/<str:category>', views.category, name='category'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]