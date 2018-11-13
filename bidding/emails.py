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
    
    merchant_id_production = 'AAAAA'
    merchant_id_test = 'MKNJSUCCMFE8U' #Mike Sorrenti's sandbox account
    merchant_id = merchant_id_test
    
    #notify_url = settings.DEFAULT_DOMAIN + reverse('paypal-ipn')
    notify_url = 'https%3a%2f%2fbpsfallfete2018%2eherokuapp%2ecom%2fpaypal%2f'
    
    item_lines = ''
    
    paypal_link = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_cart&business='
    paypal_link += merchant_id
    paypal_link += '&lc=US&'
    
    i = 1
    for item in Item.objects.all():
        if item.bidder == bidder:
            item_lines += '<tr><td>' + item.name + '</td><td>' + str(item.bid_amount) + '</td></tr>'
            paypal_link += 'item_name_' + str(i) + '=' + item.name + '&amount_' + str(i) + '=' + str(item.bid_amount) + '&'
            i += 1
    
    paypal_link += 'currency_code=USD&no_note=1&no_shipping=1&tax_rate=0%2e000&shipping=0%2e00&upload=1&'
    paypal_link += 'notify_url=' + notify_url + '&'
    paypal_link += 'email=' + bidder.email_address + '&first_name=' + bidder.first_name + '&last_name=' + bidder.last_name + '&custom=' + str(bidder.id)
    
    
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

def payment_dupe_warning(bidder, txn_id):
    mail = Mail()
    mail.from_email = Email('Brown Play School <claudine@brownplayschool.org>')
    mail.template_id = 'd-fcae18f2c2f14356bb3a654701cc656e'
    p = Personalization()
    p.add_to(Email('mjsorrenti@gmail.com'))
    p.dynamic_template_data = {
        'bidder': bidder,
        'txn': txn_id,
    }
    mail.add_personalization(p)

    sg = SendGridAPIClient()
    response = sg.client.mail.send.post(request_body=mail.get())
    
    return response

def payment_proc_debug(bidder,message):
    mail = Mail()
    mail.from_email = Email('Brown Play School <claudine@brownplayschool.org>')
    mail.template_id = 'd-ad6d3b4eac8a4dffb4fb3fbb5e206355'
    p = Personalization()
    p.add_to(Email('mjsorrenti@gmail.com'))
    p.dynamic_template_data = {
        'bidder': bidder,
        'message': message,
    }
    mail.add_personalization(p)

    sg = SendGridAPIClient()
    response = sg.client.mail.send.post(request_body=mail.get())
    
    return response