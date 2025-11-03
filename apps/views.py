from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, F, Prefetch, PositiveIntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, TemplateView, UpdateView

from apps.forms import LoginForm, RegisterModelForm, OrderCreateForm, ProfileChangePasswordModelForm
from apps.mixins import LoginNotRequiredMixin
from apps.models import Product, User, CartItem, ProductImage, Order, OrderItem
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
    queryset = Product.objects.select_related('category').prefetch_related('images')  # join
    template_name = 'apps/products/product-grid.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description__icontains=search)
            )
        return qs


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-details.html'
    context_object_name = 'product'


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'apps/products/orders.html'
    context_object_name = 'orders'


class OrderItemListView(LoginRequiredMixin, ListView):
    queryset = OrderItem.objects.all()
    template_name = 'apps/products/order-details.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        qs = super().get_queryset()
        order_id = self.kwargs.get('pk')
        self.order = get_object_or_404(Order, id=order_id)
        return qs.filter(order=self.order).annotate(
            amount=F('quantity') * (
                        F('product__price') - F('product__discount_percentage') * F('product__price') / 100)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['shipping_cost'] = qs.aggregate(Sum('product__shipping_cost'))['product__shipping_cost__sum']
        context['subtotal'] = qs.aggregate(total_sum=Sum(F('amount')))['total_sum']
        context['order'] = self.order
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    queryset = Order.objects.all()
    template_name = 'apps/products/checkout.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('product_list_page')

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(False)
        self.object.user = user
        self.object.save()
        _total_price = 0
        order_items = []
        for cart_item in user.cart.cart_items.all():
            _price = cart_item.product.price
            _total_price += _price
            order_items.append(OrderItem(
                order=self.object,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=_price
            ))
        OrderItem.objects.bulk_create(order_items)
        user.cart.delete()
        self.object.total_price = self.object.total_price
        self.object.save(update_fields=['total_price'])
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = CartItem.objects.filter(cart__user=self.request.user)
        context['shipping_cost'] = qs.aggregate(Sum('product__shipping_cost'))['product__shipping_cost__sum']
        context['cart_items'] = qs
        context['subtotal_cost'] = qs.aggregate(
            total_sum=Sum(
                F('quantity') * (F('product__price') - F('product__discount_percentage') * F('product__price') / 100)
            )
        )['total_sum']
        return context


class ShoppingCartListView(LoginRequiredMixin, ListView):
    queryset = CartItem.objects.select_related('product').prefetch_related(
        Prefetch('product__images', queryset=ProductImage.objects.all()))
    template_name = 'apps/products/shopping-cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        qs = self.get_queryset()
        context['total_price'] = qs.aggregate(
            total_sum=Sum(
                F('quantity') * (F('product__price') - F('product__discount_percentage') * F('product__price') / 100)
            )
        )['total_sum']
        return context


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


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/auth/profile.html'


class ProfileChangePasswordFormView(LoginRequiredMixin, FormView):
    template_name = 'apps/auth/profile.html'
    form_class = ProfileChangePasswordModelForm
    success_url = reverse_lazy('profile_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Successfully updated your password!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating your password!")
        return super().form_invalid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'apps/auth/profile.html'
