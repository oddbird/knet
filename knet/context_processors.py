from django.conf import settings as s

def settings(request):
    return {
        'GOOGLE_ANALYTICS_ID': s.GOOGLE_ANALYTICS_ID,
        'ENABLE_LOGIN': s.ENABLE_LOGIN,
        'BASE_URL': s.BASE_URL,
        }
