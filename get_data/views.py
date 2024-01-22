from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

from .tasks import test_func

    
def index(request):
    if request.method == 'GET':  
        s = 'Binance Data Handler\r\n\r\n\r\n'
        return HttpResponse(s, content_type='text/plain; charset=utf-8')
    else:
        return HttpResponse('Wrong method: 405')
    
def test(request):
    test_func.delay()
    return HttpResponse('http done')