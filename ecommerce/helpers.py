from random import randrange

from django.db.models import Sum

from ecommerce.models import Cart


def session_id_exists(request):
    if request.session.get('session_number'):
        return True

    return False


def set_session(request):
    random_number = randrange(100000000000)
    request.session['session_number'] = random_number
    return random_number


def check_and_generate_session(request):
    if session_id_exists(request):
        return request.session['session_number']
    else:
        return set_session(request)


def calculate_total(request, session_number):
    request.session['total'] = Cart.objects.filter(session_number=session_number)\
        .aggregate(Sum('total'))


def reset_session(request):
    del request.session['session_number']
    del request.session['total']
