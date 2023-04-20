def formatting_price(val):
    return f'${val:.2f}'.replace('.', ',')


def total_cart_qtd(cart):
    return sum([item['quantity'] for item in cart.values()])


def cart_total(cart):
    return sum(
        [
            item.get('quantity_sale_price')
            if item.get('quantity_sale_price')
            else item.get('quantity_price')
            for item
            in cart.values()
        ]
    )
