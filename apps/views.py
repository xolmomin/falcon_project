from django.views.generic import ListView, DetailView, TemplateView

from apps.models import Product


class ProductListView(ListView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/products/product-grid.html'
    context_object_name = 'products'
    paginate_by = 1


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-details.html'
    context_object_name = 'product'


class LoginTemplateView(TemplateView):
    template_name = 'apps/auth/login.html'


class RegisterTemplateView(TemplateView):
    template_name = 'apps/auth/register.html'
