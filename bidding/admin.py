from django.contrib import admin
from bidding.models import Bidder, Item
from bidding.emails import *

@admin.register(Bidder)
class BidderAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'email_address', 'amount_owed', 'payment_complete')
    list_display_links = ('id', '__str__', 'email_address')
    list_editable = ('payment_complete',)
    list_filter = ('payment_complete',)
    search_fields = ['id', 'first_name', 'last_name']
    #fields = ('first_name', 'last_name', 'mobile_checkout', 'email_address')
    
    actions = ['email_paypal_invoices',]
    
    def email_paypal_invoices(self, request, queryset):
        recipients = queryset.filter(mobile_checkout=True).filter(payment_complete=False)
        successful_emails = 0
        failed_emails = 0
        
        for recipient in recipients:
            if recipient.amount_owed() > 0:
                send = email_paypal_invoice(recipient)
                
                if send.status_code==202:
                    successful_emails += 1
                else:
                    failed_emails += 1
    
        self.message_user(request, '%s emails sent successfully' % successful_emails)
        if failed_emails > 0:
            self.message_user(request, '%s emails failed to send' % failed_emails, messages.WARNING)
    
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bidder', 'bid_amount')
    list_display_links = ('id', 'name')
    list_editable = ('bidder', 'bid_amount')
    raw_id_fields = ('bidder',)
    search_fields = ['id', 'name', 'bidder']
    fields = ('id', 'name')
