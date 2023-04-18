from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models


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
        http_referer = self.request.META['HTTP_REFERER']
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                "Product doesn't exist"
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            # TODO: var exists in cart
            pass
        else:
            # TODO; var doesnt exist in cart
            pass
        return HttpResponse(f'{variation.product} {variation.name}')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class Finalize(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalize')
