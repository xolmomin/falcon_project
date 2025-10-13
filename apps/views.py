from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView

from apps.forms import LoginForm, RegisterModelForm
from apps.mixins import LoginNotRequiredMixin
from apps.models import Product


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


class RegisterTemplateView(LoginNotRequiredMixin, CreateView):
    template_name = 'apps/auth/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('product_list_page')
    form_class = RegisterModelForm

    def form_valid(self, form):
        # TODO send email verification one time link
        return super().form_valid(form)
