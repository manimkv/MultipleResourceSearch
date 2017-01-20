from django.http import HttpResponseRedirect


def redirect_to_api(request):
    host = request.META['HTTP_HOST']
    api = 'http://{host}/api/gg/search/?q=greedy+game'.format(host=host)
    return HttpResponseRedirect(api)
