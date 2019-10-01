from django import dispatch


class WebhookSignal(dispatch.Signal):
    pass


webhook_signal = WebhookSignal()
