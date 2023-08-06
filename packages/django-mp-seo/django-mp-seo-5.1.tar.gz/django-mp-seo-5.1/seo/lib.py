
from django.db.models import Q
from django.urls import resolve, Resolver404

from seo.models import PageMeta


def _get_url_full_name(request):

    name = ''

    try:
        url = resolve(request.path_info)
    except Resolver404:
        return ''

    if url.url_name is None:
        return ''

    if url.namespaces:
        name = ':'.join(url.namespaces) + ':'

    name += url.url_name

    return name


def _get_current_url(request):

    path = request.path

    if path.startswith('/{}/'.format(request.LANGUAGE_CODE)):
        return path[3:]

    return path


def get_page_meta(request):

    try:
        return PageMeta.objects.get(
            Q(url=_get_current_url(request)) |
            Q(url=_get_url_full_name(request))
        )
    except PageMeta.DoesNotExist:
        return PageMeta()
