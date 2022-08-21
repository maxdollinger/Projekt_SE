from django.shortcuts import render

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if '/reports/' in request.path and not request.user.is_authenticated:
            ctx = {
                'type': 'danger',
                'code': '401',
                'message': 'Bitte melde dich an, um diese Seite zu sehen.', 
                'redirect': True,
                'redirect_url': '/'
            }
            return render(request, 'alert.html', ctx)	
        else:
            return None

class AddUserRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            request.role = get_user_role(request.user)

        response = self.get_response(request)
        return response

def get_user_role(user):
    groups = user.groups.all().values_list('name', flat=True)
    if 'Leiter QM' in groups:
        return 'Leiter QM'
    if 'Mitarbeiter QM' in groups:
        return 'Mitarbeiter QM'
    if 'Mitarbeiter IU' in groups:
        return 'Mitarbeiter IU'
    if 'Student' in groups:
        return 'Student'
