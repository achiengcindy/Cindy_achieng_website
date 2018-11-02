from django.urls import pathfrom . import views
app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
]