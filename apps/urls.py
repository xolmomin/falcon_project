from django.urls import path

from apps.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
]
