from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('display/', views.book_display, name='book_display'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('buy/<int:book_id>/', views.buy_now, name='buy_now'),
    path('remove/<int:book_id>/', views.remove, name='remove'),
    path('buy-now/<int:book_id>/', views.buy_now, name='buy_now'),
    path('payment/', views.payment_page, name='payment_page'),
    path('order-confirmed/', views.order_confirmed, name='order_confirmed'),
]
