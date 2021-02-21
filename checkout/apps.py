from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

# to let django know that there's a new signals module with some listeners
# we need to Override the ready method and importing signals module
    def ready(self):
        import checkout.signals
