from django.template.response import TemplateResponse


def demo(request):
    return TemplateResponse(request, 'demo.html')
