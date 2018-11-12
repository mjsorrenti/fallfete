from django.urls import path
from . import views



urlpatterns = [
    path('', views.summary, {'sort': 'by-id'}, name='summary'),
    path('?byname', views.summary, {'sort': 'by-name'}, name='summary-byname'),
    #path('sortbyname', views.summary_byname, name='summary-byname'),
    path('invoice/<int:pk>', views.bidder_detail, name='bidder-detail'),
    path('bidder/create', views.BidderCreate.as_view(), name='bidder-create'),
    path('bidder/<int:pk>/update', views.BidderUpdate.as_view(), name='bidder-update'),
    path('invoice/<int:pk>/payment-received', views.payment_received, name='payment-received'),
    path('invoice/<int:pk>/print', views.print_invoice, name='print-invoice'),
    path('packing-list', views.packing_list, name='packing-list'),
    path('paypal-ipn-listener', views.packing_list, name='packing-list'),
]

# Add mapping for Paypal IPN handler URL
from django.conf.urls import url, include

urlpatterns += [
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
]
