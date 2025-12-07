from django.urls import path
from . import views

urlpatterns = [
    # you can add your API routes later
    path('products/',views.products_list),
    path('products/create/',views.product_create),
    path('products/<int:product_id>',views.product_detail),
    path('products/<int:product_id>/update',views.product_update),
    path('products/<int:product_id>/delete',views.product_delete)



]
