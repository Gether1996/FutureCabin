from django.shortcuts import render, redirect
from .models import Order
from datetime import datetime, timedelta
from django.contrib import messages
from .forms import OrderForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
import uuid
from django.utils.translation import activate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def checkout(request):
    language_code = request.session.get('django_language', 'sk')
    activate(language_code)
    current_date = datetime.now()
    dates = request.GET.get('dates')
    print(dates)

    if not dates:
        messages.error(request, 'Vyberte si termín.')
        return redirect('/#reservations')

    dates = dates.split(',')
    selected_dates_by_user = []
    reserved_dates = []

    print(dates)

    if len(dates) == 1:
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[0], '%Y-%m-%d')
    else:
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[-1], '%Y-%m-%d')
        if end_date < start_date:
            start_date = datetime.strptime(dates[1], '%Y-%m-%d')
            end_date = datetime.strptime(dates[0], '%Y-%m-%d')

    while start_date <= end_date:
        selected_dates_by_user.append(start_date.strftime('%Y-%m-%d'))
        start_date += timedelta(days=1)

    print(selected_dates_by_user)

    if len(selected_dates_by_user) <3:
        messages.error(request, 'Vyberte si minimálne 2 noci.')
        return redirect('/#reservations')

    # Retrieve all reservations from the database
    reservations = Order.objects.all()

    # Iterate through reservations to extract reserved dates
    # last day of reservation can be reserved again
    for reservation in reservations:
        start_date = reservation.date_from + timedelta(days=1)
        end_date = reservation.date_to - timedelta(days=1)

        # Generate a list of dates within the reservation range
        while start_date <= end_date:
            reserved_dates.append(start_date.strftime('%Y-%m-%d'))
            start_date += timedelta(days=1)

    for date in selected_dates_by_user:
        if date in reserved_dates:
            messages.error(request, 'Váš termín je už obsadený.')
            return redirect('/#reservations')

    nights_count = len(selected_dates_by_user) - 1
    if language_code == 'sk':
        night_text = 'noci' if nights_count < 5 else 'nocí'
    else:
        night_text = 'nights'

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                name_surname=form.cleaned_data['name_surname'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                date_from=datetime.strptime(selected_dates_by_user[0], '%Y-%m-%d'),
                date_to=datetime.strptime(selected_dates_by_user[-1], '%Y-%m-%d'),
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal=form.cleaned_data['postal'],
                price=nights_count * 99
            )
            order_id = order.id
            return redirect('order', order_id=order_id)
    else:
        form = OrderForm()

    context = {
        'first_date': datetime.strptime(selected_dates_by_user[0], '%Y-%m-%d').strftime('%d.%m.%Y'),
        'last_date': datetime.strptime(selected_dates_by_user[-1], '%Y-%m-%d').strftime('%d.%m.%Y'),
        'nights': nights_count,
        'night_text': night_text,
        'form': form
    }

    return render(request, 'checkout.html', context)


def order(request, order_id):
    language_code = request.session.get('django_language', 'sk')
    activate(language_code)
    order_details = Order.objects.get(id=order_id)

    request.session['order_id'] = order_details.id

    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": order_details.price,  # Use dollar_value here
        "item_name": 'Pobyt',
        "invoice": uuid.uuid4(),  # Unique invoice ID
        "currency_code": "EUR",
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('success')}",
        "cancel_return": f"http://{host}{reverse('fail')}",
    }

    payment_paypal = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'order': order_details,
        'paypal': payment_paypal
    }

    return render(request, 'order.html', context)


def success(request):
    language_code = request.session.get('django_language', 'sk')
    activate(language_code)
    order_id = request.session['order_id']
    print(order_id)
    order_to_pay = Order.objects.get(id=order_id)
    order_to_pay.paid = True
    order_to_pay.save()

    if language_code == 'sk':
        subject = f'Objednávka chaty č. {order_to_pay.id}'
        message = render_to_string('email_template.html', {'order': order_to_pay})
    else:
        subject = f'Order of cottage number {order_to_pay.id}'
        message = render_to_string('email_template_en.html', {'order': order_to_pay})
    plain_message = strip_tags(message)
    from_email = 'gether1996@gmail.com'
    send_mail(subject, plain_message, from_email, [order_to_pay.email, 'gether1996@gmail.com'], html_message=message)

    del request.session['order_id']
    return render(request, 'payment_ok.html')


def fail(request):
    language_code = request.session.get('django_language', 'sk')
    activate(language_code)
    del request.session['coins']
    return render(request, 'payment_fail.html')
