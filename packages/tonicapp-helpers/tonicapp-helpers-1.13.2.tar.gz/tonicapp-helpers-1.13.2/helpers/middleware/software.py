from django.http import HttpResponseBadRequest


class SoftwareTypeMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        app_type = request.META.get('HTTP_SOFTWARE_TYPE')
        if not app_type:
            return HttpResponseBadRequest(
                'Add Software-Type to the header. Example: Software-Type: Web or Software-Type: Application'
            )
        if app_type not in ['Application', 'Web', 'Backoffice']:
            return HttpResponseBadRequest(
                'Incorrect Software-Type, the available options are: Application or Web or Backoffice.'
            )

        request.software_type = 'mobile'

        if 'Web' in app_type:
            request.software_type = 'web'
        elif 'Backoffice' in app_type:
            request.software_type = None
            
        response = self.get_response(request)

        return response
