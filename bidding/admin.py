from django.contrib import admin
from bidding.models import Bidder, Item

@admin.register(Bidder)
class BidderAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'email_address', 'amount_owed', 'payment_complete')
    list_display_links = ('id', '__str__', 'email_address')
    list_editable = ('payment_complete',)
    list_filter = ('payment_complete',)
    search_fields = ['id', 'first_name', 'last_name']
    #fields = ('first_name', 'last_name', 'mobile_checkout', 'email_address')
    
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bidder', 'bid_amount')
    list_display_links = ('id', 'name')
    list_editable = ('bidder', 'bid_amount')
    raw_id_fields = ('bidder',)
    search_fields = ['id', 'name', 'bidder']
    fields = ('id', 'name')
