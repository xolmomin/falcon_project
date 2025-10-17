from django.urls import path, re_path

from apps.views import ProductListView, ProductDetailView, RegisterCreateView, LoginFormView, CustomLogoutView, \
    ActivateAccountView, ShoppingCartTemplateView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
    path('products/carts', ShoppingCartTemplateView.as_view(), name='shopping_cart_page'),
    path('auth/login', LoginFormView.as_view(), name='login_page'),
    path('auth/logout', CustomLogoutView.as_view(), name='logout_page'),
    re_path(r'^auth/user/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
            ActivateAccountView.as_view(), name='confirm_email_page'),
    path('auth/register', RegisterCreateView.as_view(), name='register_page'),

]
