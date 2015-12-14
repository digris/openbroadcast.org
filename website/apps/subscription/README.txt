# setup


## settings

    # AI Key
    MAILCHIMP_API_KEY = ''
    # default _local_ id
    SUBSCRIPTION_DEFAULT_LIST_ID = 1
    # webhook, to use in the form of: https://www.example.com/subscription/webhook/mailchimp/XZ-VR-BW/
    SUBSCRIPTION_WEBHOOK_TOKEN = 'XZ-VR-BW'

## url patterns

    url(r'^subscription/', include('subscription.urls')),


## template

    {% load subscription_tags %}

    {% subscription_form %}