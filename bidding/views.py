import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.views import generic
from bidding.models import Bidder, Item
from bidding.forms import EmailInvoiceForm

# Create your views here.

@login_required
def summary(request, sort):
    """View function for the invoicing summary page"""
    total_amt = 0
    
    if sort == 'by-name':
        bidders = Bidder.objects.all().order_by('last_name')
    else:
        bidders = Bidder.objects.all()
        
    for bidder in bidders:
        total_amt += bidder.amount_owed()
    
    return render(request, 'summary.html', context={'bidders':bidders, 'sort':sort, 'total':total_amt})

@login_required
def summary_byname(request):
    """View function for the invoicing summary page"""
    
    bidders = Bidder.objects.all().order_by('last_name')
    
    return render(request, 'summary_byname.html', context={'bidders':bidders,})

@login_required
def bidder_detail(request, pk):
    bidder = get_object_or_404(Bidder, pk=pk)
    
    if request.method == 'POST':
        email_invoice_form = EmailInvoiceForm(request.POST)
        email_sent = False
        
        if email_invoice_form.is_valid():
            email_sent = True
        
        return render(request, 'bidding/bidder_detail.html', context={'bidder':bidder, 'email_form':email_invoice_form, 'email_sent':email_sent})
    
    else:
        email_invoice_form = EmailInvoiceForm(initial={'email': bidder.email_address})
        
    return render(request, 'bidding/bidder_detail.html', context={'bidder':bidder, 'email_form':email_invoice_form})


def payment_received(request, pk):
    if request.method == 'POST':
        bidder = get_object_or_404(Bidder, pk=pk)
    
        bidder.payment_complete = True
        bidder.payment_txn = 'manual_' + str(request.user.get_username())
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
