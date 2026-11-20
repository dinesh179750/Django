from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import CrackersForm, Giftsform, sweetsform
from .models import Crackers, Sweets, Gifts


def add_products(request):

    crackers_form = CrackersForm()
    sweets_form = sweetsform()
    gifts_form = Giftsform()

    if request.method == "POST":

        if 'add_crackers' in request.POST:
            crackers_form = CrackersForm(request.POST, request.FILES)

            if crackers_form.is_valid():
                crackers_form.save()
                return redirect('crack')

        elif 'add_sweets' in request.POST:
            sweets_form = sweetsform(request.POST, request.FILES)

            if sweets_form.is_valid():
                sweets_form.save()
                return redirect('crack')

        elif 'add_gifts' in request.POST:
            gifts_form = Giftsform(request.POST, request.FILES)

            if gifts_form.is_valid():
                gifts_form.save()
                return redirect('crack')

    context = {
        'crackers_form': crackers_form,
        'sweets_form': sweets_form,
        'gifts_form': gifts_form
    }

    return render(request, 'crack.html', context)


def home(request):

    crackers = Crackers.objects.all()
    sweets = Sweets.objects.all()
    gifts = Gifts.objects.all()

    context = {
        'data': crackers,
        'data2': sweets,
        'data3': gifts
    }

    return render(request, 'home.html', context)



from django.shortcuts import  redirect
from .models import Crackers, Sweets, Gifts

def add_to_cart(request, id):
    if request.method == "POST":

        product = None
        product_type = None

        if Crackers.objects.filter(id=id).exists():
            product = Crackers.objects.get(id=id)
            product_type = "cracker"

        elif Sweets.objects.filter(id=id).exists():
            product = Sweets.objects.get(id=id)
            product_type = "sweet"

        elif Gifts.objects.filter(id=id).exists():
            product = Gifts.objects.get(id=id)
            product_type = "gift"

        if product:
            cart = request.session.get('cart', {})

            key = f"{product_type}_{id}"

            if key in cart:
                cart[key]['quantity'] += 1
            else:
                cart[key] = {
                    'id': id,
                    'name': str(product),
                    'price': float(product.price),
                    'quantity': 1,
                    'type': product_type
                }

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('home')


def cart(request):

    cart = request.session.get('cart', {})

    cart_items = []
    grand_total = 0

    for key, item in cart.items():

        total = item['price'] * item['quantity']

        cart_items.append({
            'key': key,
            'name': item['name'],
            'type': item['type'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': total
        })

        grand_total += total

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })


@require_POST
def update_cart(request, key):

    cart = request.session.get('cart', {})

    if key in cart:

        if request.POST.get('action') == 'increase':
            cart[key]['quantity'] += 1

        elif request.POST.get('action') == 'decrease':
            cart[key]['quantity'] -= 1

            if cart[key]['quantity'] <= 0:
                del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


@require_POST
def remove_from_cart(request, key):

    cart = request.session.get('cart', {})

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')