from django.urls import path, re_path

from apps.views import ProductListView, ProductDetailView, RegisterCreateView, LoginFormView, CustomLogoutView, \
    ActivateAccountView, ShoppingCartListView, OrderCreateView, OrderListView, ProfileTemplateView, \
    ProfileChangePasswordFormView, OrderItemListView, google_login, google_callback

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('products/carts', ShoppingCartListView.as_view(), name='shopping_cart_page'),
    path('products/checkout', OrderCreateView.as_view(), name='checkout_page'),
    path('products/orders', OrderListView.as_view(), name='order_page'),
    path('products/orders/<int:pk>', OrderItemListView.as_view(), name='order_detail_page'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
    path('auth/login', LoginFormView.as_view(), name='login_page'),
    path('auth/logout', CustomLogoutView.as_view(), name='logout_page'),
    re_path(r'^auth/user/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
            ActivateAccountView.as_view(), name='confirm_email_page'),
    path('auth/register', RegisterCreateView.as_view(), name='register_page'),
    path('profile', ProfileTemplateView.as_view(), name='profile_page'),
    path('profile/change/password', ProfileChangePasswordFormView.as_view(), name='profile_change_password_page'),

    path("auth/google-login", google_login, name='google_login'),
    path("auth/oauth2/callback", google_callback, name='google_callback'),

]
