# myapp/middleware.py

from django.shortcuts import redirect
from rest_framework_simplejwt.backends import TokenBackend

# class JWTTokenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.token_backend = TokenBackend(algorithm='HS256')  # Use the appropriate algorithm

#     def __call__(self, request):
#         jwt_token = request.session.get('access_token')
#         if jwt_token:
#             request.META['HTTP_AUTHORIZATION'] = f'Bearer {jwt_token}'
#             try:
#                 self.token_backend.decode(jwt_token)
#                 # Token is valid, continue with the request
#             except Exception as e:
#                 # Token verification failed, redirect to login
#                 return redirect('login')  # Replace 'login' with your login URL

#         response = self.get_response(request)
#         return response

from rest_framework_simplejwt.tokens import RefreshToken

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(request.user)
            access_token = str(refresh.access_token)

            # Set access token as a cookie
            response.set_cookie('access_token', access_token, httponly=False)

            # Store access token in the session
            request.session['access_token'] = access_token

        return response
