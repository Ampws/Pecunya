from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import View
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

class CustomPasswordResetView(PasswordResetView):
    allowed_methods = ('POST')

    def post(self, request, *args, **kwargs):
        if 'email' not in request.data and 'username' not in request.data:
            return Response(
                {'detail': _('Must provide either email or username.')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if '@' in request.data.get('username', ''):
            return Response(
                {'detail': _('Username should not contain @')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if 'email' in request.data:
            return super().post(request, *args, **kwargs)
        if 'username' in request.data:
            username = request.data['username']
            user_model = get_user_model()
            try:
                user = user_model.objects.get(username=username)
            except user_model.DoesNotExist:
                return Response(
                    {'detail': _('User not found.')},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            email = user.email
            request.data['email'] = email
            return super().post(request, *args, **kwargs)
        
class CustomPasswordResetConfirmView(View):
    allowed_methods = ('GET')

    def get(self, request, *args, **kwargs):
        return redirect(request.path.replace('/api', ''))
    
class CustomRegisterView(RegisterView):
    allowed_methods = ('POST')

    def post(self, request, *args, **kwargs):
        if '@' in request.data.get('username', ''):
            return Response(
                {'detail': _('Username should not contain @')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().post(request, *args, **kwargs) 
    
class CustomVerifyEmailView(VerifyEmailView):
    allowed_methods = ('GET')

    def get(self, *args, **kwargs):
        request = self.request._request
        request.method = 'POST'
        request.data = kwargs
        response = self.post(request)
        if response.status_code == 200:
            return redirect('/login/')
        return response