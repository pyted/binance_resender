import traceback
import requests.api
import urllib.parse as up
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import appSite.globalvar as gv
from appSite.models import SenderLogModel


def index_handler(request):
    return render(request, 'index.html', {})


def resender(request, path, api_url):
    # 需要保留的header key
    header_keys = ['Content-Type', 'User-Agent', 'X-MBX-APIKEY']
    # request中得到的header key转小写
    request_header_lower_map = {}
    for k, v in request.headers.items():
        request_header_lower_map[k.lower()] = v
    # 构造headers
    headers = {}
    for key in header_keys:
        if key.lower() in request_header_lower_map.keys():
            headers[key] = request_header_lower_map[key.lower()]

    method = request.method.lower()
    params = {}
    if method == 'get':
        for key in request.GET.keys():
            value = request.GET[key]
            params[key] = value
    else:
        for key in request.POST.keys():
            value = request.GET[key]
            params[key] = value
    params.pop('url', None)
    params_encode = up.urlencode(params, True).replace("%40", "@")
    url = up.urljoin(api_url, path)
    response = requests.api.request(
        method=method,
        url=url,
        params=params_encode,
        headers=headers
    )
    text = response.text
    return text


def base_api_handler(request, path, api_url):
    # ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not ip in gv.get('allowed_ips'):
        error_msg = 'Forbidden IP:' + ip
        status = 403
        if gv.get('use_log'):
            if not ip:
                ip = 'UnKnow'
            SenderLogModel(
                ip=ip,
                status=0,
                error_msg='Forbidden IP ' + ip
            ).save()
        error_data = {'code': '-1', 'data': {}, 'msg': error_msg}
        return JsonResponse(error_data, status=status)
    # resender
    try:
        text = resender(request, path, api_url)
        status = 200
        if gv.get('use_log'):
            SenderLogModel(
                ip=ip,
                status=1,
                error_msg='',
            ).save()
        return HttpResponse(str(text), status=status)
    except:
        error_msg = 'Error Binance Resender ' + traceback.format_exc()
        error_data = {'code': '-2', 'data': {}, 'msg': error_msg}
        status = 500
        if gv.get('use_log'):
            SenderLogModel(
                ip=ip,
                status=0,
                error_msg=error_msg,
            ).save()
        return JsonResponse(error_data, status=status)


@csrf_exempt
def api_handler(request, path):
    return base_api_handler(request, path, 'https://api.binance.com')


@csrf_exempt
def dapi_handler(request, path):
    return base_api_handler(request, path, 'https://dapi.binance.com')


@csrf_exempt
def eapi_handler(request, path):
    return base_api_handler(request, path, 'https://eapi.binance.com')


@csrf_exempt
def fapi_handler(request, path):
    return base_api_handler(request, path, 'https://fapi.binance.com')


@csrf_exempt
def papi_handler(request, path):
    return base_api_handler(request, path, 'https://papi.binance.com')
