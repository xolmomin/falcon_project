from django.urls import path

from apps.views import ProductListView, ProductDetailView, RegisterTemplateView, LoginTemplateView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
    path('login', LoginTemplateView.as_view(), name='login_page'),
    path('register', RegisterTemplateView.as_view(), name='register_page'),
]
