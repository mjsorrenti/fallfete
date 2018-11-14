import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
#from django.views import generic
from bidding.models import Bidder, Item
from bidding.forms import EmailInvoiceForm, BidderSearchForm
from bidding.emails import *

# Create your views here.

@login_required
def summary(request, sort):
    """View function for the invoicing summary page"""
    total_amt = 0
    for bidder in Bidder.objects.all():
        total_amt += bidder.amount_owed()
    search_active = False
        
    if request.method == 'POST':
        search_form = BidderSearchForm(request.POST)
        if search_form.is_valid():
            bidders = Bidder.objects.filter(Q(first_name__icontains=search_form.cleaned_data['name']) | Q(last_name__icontains=search_form.cleaned_data['name']))
        search_active = True
    
    else:
        search_form = BidderSearchForm()
        
        if sort == 'by-name':
            bidders = Bidder.objects.all().order_by('last_name')
        else:
            bidders = Bidder.objects.all()
        
    
    
    return render(request, 'summary.html', context={'bidders':bidders, 'sort':sort, 'total':total_amt, 'search_form':search_form, 'search_active':search_active})


@login_required
def bidder_detail(request, pk):
    bidder = get_object_or_404(Bidder, pk=pk)
    
    if request.method == 'POST':
        email_invoice_form = EmailInvoiceForm(request.POST)
        email_sent = False
        
        if email_invoice_form.is_valid():
            send = email_standard_invoice(bidder,email_invoice_form.cleaned_data['email'])
            if send.status_code == 202:
                email_sent = 'Success'
            else:
                email_sent = 'Fail'
        
        return render(request, 'bidding/bidder_detail.html', context={'bidder':bidder, 'email_form':email_invoice_form, 'email_sent':email_sent})
    
    else:
        email_invoice_form = EmailInvoiceForm(initial={'email': bidder.email_address})
        
    return render(request, 'bidding/bidder_detail.html', context={'bidder':bidder, 'email_form':email_invoice_form})


def payment_received(request, pk):
    if request.method == 'POST':
        bidder = get_object_or_404(Bidder, pk=pk)
    
        bidder.payment_complete = True
        bidder.payment_txn = str(request.user.get_username()) + ' - ' + str(datetime.datetime.now())
        bidder.save()
    
    return HttpResponseRedirect(bidder.get_invoice_url())


class BidderCreate(LoginRequiredMixin, CreateView):
    model = Bidder
    fields = ['first_name', 'last_name', 'mobile_checkout', 'email_address']
    success_url = reverse_lazy('summary')
    
class BidderUpdate(LoginRequiredMixin, UpdateView):
    model = Bidder
    fields = ['first_name', 'last_name', 'mobile_checkout', 'email_address']
    success_url = reverse_lazy('summary')
    
@login_required
def print_invoice(request, pk):
    """View function for the invoicing printing page"""
    
    bidder = get_object_or_404(Bidder, pk=pk)
    date = datetime.date.today()
    year = date.year
    
    return render(request, 'bidding/print.html', context={'bidder':bidder, 'date':date, 'year':year,})

@login_required
def packing_list(request):
    """View function for the packing list page"""
    
    bidders = Bidder.objects.all()
    
    return render(request, 'packing_list.html', context={'bidders':bidders,})
