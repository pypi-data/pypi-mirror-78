# -*- coding: utf-8 -*-
"""CAS login/logout replacement views"""
import uuid
import traceback
import logging
import requests
from django.core.files.storage import default_storage, FileSystemStorage
from django.contrib import auth
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
)
from django.conf import settings
from django.urls import reverse
from django.utils import translation
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.request import Request
from rest_framework.response import Response

from .utils import _oauthLogoutUrl
logger = logging.getLogger("default")


def is_secure(request):
    return getattr(settings, "IS_SECURE", request.is_secure())


def oauthLogout(request: Request):
    """登出"""
    auth.logout(request)
    logoutUrl = _oauthLogoutUrl(request)
    return HttpResponseRedirect(logoutUrl)


@api_view(["PUT"])
def language(request: Request):
    """language 设置语言
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    pk = request.user.hacId
    url = f"{request.domain.hac.url}/api/admin/users/{pk}/language"
    response = requests.put(
        url,
        json={"data": {"language": request.data.get("language", "zh_CN")}},
        headers={"identify": request.domain.hac.identify},
        timeout=10,
    )
    if response.status_code == 200 and response.json().get("code", None) == "200000":
        return Response(
            {"message": "操作成功"}, content_type="application/json;charset = utf-8"
        )
    return Response(
        {"message": "操作失败"},
        content_type="application/json;charset = utf-8",
        status=400,
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def enviroment(request: Request) -> Response:
    """enviroment 获取title，logo等配置
    """
    data = request.domain.config
    data['profileUrl'] = f'{request.domain.hac.url}/account/profile'
    data['hacUrl'] = f'{request.domain.hac.url}'
    data['loginUrl'] = f'{request.domain.url}' + reverse('cas:login')
    data['logoutUrl'] = f'{request.domain.url}' + reverse('cas:logout')
    return Response(data)


@api_view(['GET'])
def profile(request: Request) -> Response:
    try:
        data = dict(name=request.user.username, email=request.user.email)
        data.update(
            avatar=None,
            avatarThumb=None,
            theme=None,
            apps=None
        )
    except AttributeError:
        response = dict(message="未登录或 session 过期", url=f'{request.domain.url}' + reverse('cas:login'))
        return Response(status=401, data=response)

    url = f'{request.domain.hac.url}/api/admin/users/{request.user.hacId}/profile'
    try:
        hacResponse = requests.get(url, timeout=10, headers=request.domain.hac.identify or {'identify': 'URBahpGT5tYCFd0rjy2EHe1oVYX7O3hb'}).json()
    except Exception:
        logger.error(url)
        logger.error(traceback.format_exc())
        hacResponse = {}

    userInfo = hacResponse.get('result', {}) or {'language': settings.LANGUAGE_CODE}
    if userInfo:
        data.update(userInfo)
    request.session[translation.LANGUAGE_SESSION_KEY] = data['language']

    return Response(data)


@api_view(['GET'])
def userSettings(request: Request):
    """重定向到hac的settings"""
    redirectUrl = f'{request.domain.hac.url}/settings'
    return HttpResponseRedirect(redirectUrl)


@api_view(['POST'])
def upload(request):
    path = uuid.uuid4().hex
    myfile = request.FILES.get("file")
    storage = request.GET.get("storage", "")
    ext = ""
    storage_class = default_storage
    if not myfile:
        return Response({"file": 'required'}, status_code=401)
    if "." in myfile.name:
        ext = myfile.name.split(".")[-1]
    path = f"{path}.{ext}"
    if storage:
        storage_class = FileSystemStorage()
        path = myfile.name
    file = storage_class.open(path, "wb")
    file.write(myfile.read())
    file.close()
    url = storage_class.url(path)
    return Response({"file_path": path, "url": url})