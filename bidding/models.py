from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns


class Item(models.Model):
    """Model for merchandise items in the auction"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    bidder = models.ForeignKey('Bidder', on_delete=models.SET_NULL, null=True, blank=True)
    bid_amount = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        """String for representing the Item"""
        return self.name

class Bidder(models.Model):
    """Model for individuals placing bids in the auction"""
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(blank=True)
    mobile_checkout = models.BooleanField()
    payment_complete = models.BooleanField(default=False)
    payment_txn = models.CharField(max_length=50,blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        """String for representing the Bidder"""
        return self.first_name + ' ' + self.last_name
    
    def get_invoice_url(self):
        """Returns the url to access a particular invoice for the bidder."""
        return reverse('bidder-detail', args=[str(self.id)])
    
    def get_edit_url(self):
        """Returns the url to access as edit page for the bidder."""
        return reverse('bidder-update', args=[str(self.id)])
    
    def get_print_url(self):
        """Returns the url to access as invoice print for the bidder."""
        return reverse('print-invoice', args=[str(self.id)])
    
    def amount_owed(self):
        total_bid = 0
        for item in self.item_set.all():
            total_bid += item.bid_amount
        return total_bid

    
class BatchProcessing(models.Model):
    """Model for uploading and processing XLS documents with item & bidder details"""
    
    FILE_TYPES = (
        ('I', 'Items'),
        ('B', 'Bidders'),
    )
    
    name = models.CharField(max_length=50)
    file = models.FileField(help_text='Files must be in CSV format. \rItems files should have 2 columns: id, name \rBidders files should have 4 columns: first_name, last_name, email_address, mobile_checkout (for the last column, any value will be interpretted as True; leave the cell blank for False)')
    type = models.CharField(max_length=10, choices=FILE_TYPES)