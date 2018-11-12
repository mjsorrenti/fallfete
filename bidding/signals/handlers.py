from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from bidding.models import Bidder

@receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    """Do things here upon a valid IPN message received"""
    if sender.payment_status == ST_PP_COMPLETED:
        if sender.receiver_email != 'mjsorrenti-facilitator@gmail.com':
            #not a valid message
            return
        
        bidder = Bidder.objects.get(id=sender.invoice)
        
        if sender.mc_gross != bidder.amount_owed:
            #not a valid payment - amounts do not match
            return
        
        if bidder.payment_complete == True:
            #may be a duplicate payment
            return
        
        bidder.payment_complete = True

@receiver(invalid_ipn_received)
def do_not_show_me_the_money(sender, **kwargs):
    """Do things here upon an invalid IPN message received"""
    pass