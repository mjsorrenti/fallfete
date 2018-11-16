from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from bidding.models import Bidder
from bidding.emails import *

@receiver(valid_ipn_received)
def update_payment_status(sender, **kwargs):
    """Do things here upon a valid IPN message received"""
    
    #payment_proc_debug('none yet','The receiver is active. payment_status:' + sender.payment_status)
    
    if sender.payment_status == ST_PP_COMPLETED:
        
        #payment_proc_debug('none yet', 'Payment status checks out as complete.')
        
        # acct_email = 'mjsorrenti-facilitator@gmail.com' # Mike Sorrenti's sandbox account
        acct_email = 'cftaylor7@yahoo.com' # Brown Play School account
        
        if sender.receiver_email != acct_email:
            #not a valid message
            payment_proc_debug('none','Receiver emails didn\'t match:' + sender.receiver_email)
            return
        
        bidder = Bidder.objects.get(id=sender.custom)
        #payment_proc_debug('check invoice number', str(bidder.amount_owed()) + ' ? ' + str(sender.mc_gross))
        
        if sender.mc_gross != bidder.amount_owed():
            #not a valid payment - amounts do not match
            payment_proc_debug(bidder.last_name, 'Amount received (' + str(sender.mc_gross) + ') didn\'t match amount owed (' + str(bidder.amount_owed()) + ')')
            return
        
        if bidder.payment_complete == True:
            #may be a duplicate payment
            payment_dupe_warning(bidder.first_name + ' ' + bidder.last_name, str(sender.txn_id))
            return
        
        bidder.payment_complete = True
        bidder.payment_txn = 'PayPal-' + sender.txn_id
        bidder.save()

@receiver(invalid_ipn_received)
def do_not_show_me_the_money(sender, **kwargs):
    """Do things here upon an invalid IPN message received"""
    pass