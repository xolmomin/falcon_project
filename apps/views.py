from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView

from apps.forms import LoginForm, RegisterModelForm
from apps.mixins import LoginNotRequiredMixin
from apps.models import Product, User
from apps.tokens import account_activation_token
from apps.utils import send_registration_link


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Email tasdiqlandi, endi bemalol login qilsa bo'ladi")
        else:
            messages.error(request, "Bu linkda xatolik bor")

        return redirect('product_list_page')


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-grid.html'
    context_object_name = 'products'
    paginate_by = 1


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-details.html'
    context_object_name = 'product'


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('product_list_page')


class LoginFormView(LoginNotRequiredMixin, FormView):
    template_name = 'apps/auth/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('product_list_page')

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class RegisterCreateView(LoginNotRequiredMixin, CreateView):
    template_name = 'apps/auth/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('product_list_page')
    form_class = RegisterModelForm

    def form_valid(self, form):
        user = form.save(False)
        user.is_active = False
        user.save()

        send_registration_link(user, f"http://{self.request.get_host()}")
        messages.success(self.request, "Ro'yxatdan muvaffaqiyatli o'tdingiz! Pochtangizni tekshiring.")
        return redirect(self.success_url)
