from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        requestUrl = request.META['PATH_INFO']
        if not request.session.get('customer_id'):
             return redirect(f'/login?return_url={requestUrl}')

        response = get_response(request)
        return response

    return middleware

def require_email(get_response):
    def middleware(request):
        requestUrl = request.META['PATH_INFO']
        if not request.session.get('email'):
             return redirect(f'/getemail?return_url={requestUrl}')

        response = get_response(request)
        return response

    return middleware   