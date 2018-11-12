from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

from .models import Bidder, Item

def email_standard_invoice(bidder, email):
    name = bidder.__str__()
    inv_total = bidder.amount_owed()
    
    item_lines = ''
    for item in Item.objects.all():
        if item.bidder == bidder:
            item_lines += '<tr><td>' + item.name + '</td><td>' + str(item.bid_amount) + '</td></tr>'
    
    mail = Mail()
    mail.from_email = Email('Brown Play School <claudine@brownplayschool.org>')
    mail.template_id = 'd-9b5b3fc5a5314921aae113351f712ca9'
    p = Personalization()
    p.add_to(Email(email))
    p.dynamic_template_data = {
        'name': name,
        'item_rows': item_lines,
        'inv_total': inv_total
    }
    mail.add_personalization(p)

    sg = SendGridAPIClient()
    response = sg.client.mail.send.post(request_body=mail.get())
    
    return response
    
    
def email_paypal_invoice(bidder):
    name = bidder.__str__()
    inv_total = bidder.amount_owed()
    
    notify_url = settings.DEFAULT_DOMAIN + reverse('paypal-ipn')
    item_lines = ''
    paypal_link = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_cart&upload=1&business=MKNJSUCCMFE8U&lc=US&no_note=1&no_shipping=1&'
    paypal_link += 'notify_url=' + notify_url + '&'
    paypal_link += 'invoice=' + bidder.id + '&'
    
    i = 1
    for item in Item.objects.all():
        if item.bidder == bidder:
            item_lines += '<tr><td>' + item.name + '</td><td>' + str(item.bid_amount) + '</td></tr>'
            paypal_link += 'item_name_' + str(i) + '=' + item.name + '&amount_' + str(i) + '=' + str(item.bid_amount) + '&'
            i += 1
    
    paypal_link += 'email=' + bidder.email_address + '&first_name=' + bidder.first_name + '&last_name=' + bidder.last_name
    
    mail = Mail()
    mail.from_email = Email('Brown Play School <claudine@brownplayschool.org>')
    mail.template_id = 'd-3ca0881d65c14a3e88812b1bf2be6694'
    p = Personalization()
    p.add_to(Email(bidder.email_address))
    p.dynamic_template_data = {
        'name': name,
        'item_rows': item_lines,
        'inv_total': inv_total,
        'paypal_link': paypal_link
    }
    mail.add_personalization(p)

    sg = SendGridAPIClient()
    response = sg.client.mail.send.post(request_body=mail.get())
    
    return response
