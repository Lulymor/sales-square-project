from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from product.models import Variation
from .models import Order, ItemOrdered

from utils import utils


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

class SaveOrder(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'You need to login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Your cart is empty.'
            )
            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variation_ids = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product')
            .filter(id__in=cart_variation_ids)
        )

        for variation in bd_variations:
            vid = str(variation.id)

            inventory= variation.inventory
            qtd_carrinho = cart[vid]['quantity']
            preco_unt = cart[vid]['unity_price']
            preco_unt_promo = cart[vid]['unity_sale_price']

            error_msg_inventory = ''

            if inventory < qtd_carrinho:
                cart[vid]['quantity'] = inventory
                cart[vid]['quantity_price'] = inventory * preco_unt
                cart[vid]['quantity_sale_price'] = inventory * \
                    preco_unt_promo

                error_msg_inventory= 'Not enough items on stock '
                
            if error_msg_inventory:
                messages.error(
                    self.request,
                    error_msg_inventory
                )

                self.request.session.save()
                return redirect('product:cart')

        qtd_total_carrinho = utils.total_cart_qtd(cart)
        valor_total_carrinho = utils.cart_total(cart)

        order = Order(
            user=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        order.save()

        ItemOrdered.objects.bulk_create(
            [
                ItemOrdered(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantity_price'],
                    sale_price=v['quantity_sale_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'order:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )


class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'


class List(DispatchLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 10
    ordering = ['-id']

# Create your views here.
