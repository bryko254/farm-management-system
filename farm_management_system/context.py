from django.conf import settings


def site(request):
    return {'allow_registration': settings.ALLOW_REGISTRATION}
