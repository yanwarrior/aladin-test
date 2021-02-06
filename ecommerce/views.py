from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ecommerce.forms import CartUpdateForm, CheckoutForm, TrackOrderForm
from ecommerce.helpers import check_and_generate_session, calculate_total, reset_session
from ecommerce.models import Product, Cart, Order


def product_list(request):
    object_list = Product.objects.all()

    paginator = Paginator(object_list, 18)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'ecommerce/product/list.html',
                  {'products': products, 'page': page})





def cart_list(request):
    session_number = check_and_generate_session(request)
    object_list = Cart.objects.filter(session_number=session_number)

    paginator = Paginator(object_list, 18)
    page = request.GET.get('page')

    try:
        carts = paginator.page(page)
    except PageNotAnInteger:
        carts = paginator.page(1)
    except EmptyPage:
        carts = paginator.page(paginator.num_pages)

    return render(request,
                  'ecommerce/cart/list.html',
                  {'carts': carts,
                   'page': page,
                   'session_number': session_number})


@require_POST
def cart_create(request, product_id):
    session_number = check_and_generate_session(request)
    product = get_object_or_404(Product, pk=int(product_id))
    cart, is_created = Cart.objects.get_or_create(product=product,
                                                  session_number=session_number)

    if not is_created:
        cart.quantity = F('quantity') + 1
    else:
        cart.quantity = 1

    cart.total = cart.quantity * product.price
    cart.save()

    calculate_total(request, session_number)

    return redirect('ecommerce:cart_list')


def cart_edit(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    if request.method == 'POST':
        form = CartUpdateForm(request.POST, instance=cart)
        if form.is_valid():
            cart_form = form.save(commit=False)
            if cart_form.quantity == 0:
                cart.delete()
                calculate_total(request, cart.session_number)
                return redirect('ecommerce:cart_list')

            cart.quantity = cart_form.quantity
            cart.total = cart.quantity * cart.product.price
            cart.save()
            calculate_total(request, cart.session_number)
            return redirect('ecommerce:cart_list')
    else:
        form = CartUpdateForm(instance=cart)

    return render(request,
                  'ecommerce/cart/edit.html',
                  {'form': form,
                   'cart': cart})


def cart_delete(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    session_number = cart.session_number
    if request.method == 'POST':
        cart.delete()
        calculate_total(request, session_number)
        return redirect('ecommerce:cart_list')

    return render(request,
                  'ecommerce/cart/delete.html')


def cart_reset(request):
    if request.method == 'POST':
        session_number = check_and_generate_session(request)
        Cart.objects.filter(session_number=session_number).delete()
        reset_session(request)

        return redirect('ecommerce:product_list')

    return render(request, 'ecommerce/cart/reset.html')


def order_create(request):
    order = None
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_number = check_and_generate_session(request)
            order.total = request.session.get('total')['total__sum']
            order.save()
            Cart.objects.filter(session_number=order.order_number).delete()
            del request.session['session_number']
            del request.session['total']
    else:
        form = CheckoutForm()

    return render(request,
                  'ecommerce/order/create.html',
                  {'form': form, 'order': order})


def order_track(request):
    order = None
    if request.method == 'POST':
        form = TrackOrderForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data.get('order_number')
            order = get_object_or_404(Order, order_number=order_number)
    else:
        form = TrackOrderForm()

    return render(request,
                  'ecommerce/order/track.html',
                  {'form': form, 'order': order})
