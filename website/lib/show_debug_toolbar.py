from django.conf import settings


def show(request):
    try:
        ip = get_client_ip(request)
    except:
        ip = None
    if ip and ip in settings.INTERNAL_IPS:
        return True
    else:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
