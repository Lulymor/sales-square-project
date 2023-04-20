from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

from pprint import pprint
from perfil.models import Perfil


class ProductList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_inventory = variation.inventory
        product = variation.product

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unity_price = variation.price
        unity_sale_price = variation.sale_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.inventory < 1:
            messages.error(
                self.request,
                'Item Out of Stock'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            quantity_cart = cart[variation_id]['quantity']
            quantity_cart += 1

            if variation_inventory < quantity_cart:
                messages.warning(
                    self.request,
                    f'Not enough items on stock {quantity_cart}x for '
                    f'product "{product_name}". {variation_inventory}x '
                    f'Added to cart.'
                )
                quantity_cart = variation_inventory

            cart[variation_id]['quantity'] = quantity_cart
            cart[variation_id]['quantity_price'] = unity_price * \
                quantity_cart
            cart[variation_id]['quantity_sale_price'] = unity_sale_price * \
                quantity_cart
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unity_price': unity_price,
                'unity_sale_price': unity_sale_price,
                'quantity_price': unity_price,
                'quantity_sale_price': unity_sale_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Product {product_name} {variation_name} added to your '
            f'cart {cart[variation_id]["quantity"]}x.'
        )

        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f'Item {cart["product_name"]} {cart["variation_name"]} '
            f'removed from cart.'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }

        return render(self.request, 'product/cart.html', context)


class OrderSummary(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('product:list')

        contexto = {
            'usuario': self.request.user,
            'cart': self.request.session['cart'],
        }

        return render(self.request, 'product/ordersummary.html', contexto)
