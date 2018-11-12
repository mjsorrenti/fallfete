from django.apps import AppConfig


class BiddingConfig(AppConfig):
    name = 'bidding'
    
    def ready(self):
        import bidding.signals.handlers
