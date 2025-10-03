from django.views.generic import ListView, DetailView, TemplateView

from apps.models import Product


# def index_page(request):
#     context = {
#         'products': Product.objects.all(),
#     }
#     return render(request, 'apps/products/product-grid.html', context)
#
# def product_detail_page(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     # product = Product.objects.filter(pk=pk).first()
#     # if product is None:
#     #     return
#
#     context = {
#         'product': product
#     }
#
#     return render(request, 'apps/products/product-details.html', context)


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-grid.html'
    context_object_name = 'products'
    paginate_by = 5


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-details.html'
    context_object_name = 'product'

class LoginView(TemplateView):
    template_name = 'apps/login.html'