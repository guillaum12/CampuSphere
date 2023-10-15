from django.shortcuts import render, redirect
import requests
from django.contrib.auth import get_user_model, login
from allauth.account.models import EmailAddress

import convention.settings as settings
from urllib.parse import urlparse, parse_qs

def registration(request):

    return redirect("https://auth.viarezo.fr/oauth/authorize/?" + "&" +
                "redirect_uri="+ settings.BASE_URL + 'authentication/connexion/' + "&" +
                "client_id=" + settings.OAUTH_CLIENT_ID + "&" +
                "response_type=" + "code" + "&" +
                "state=" + "MeLlamoLaplayaDeHoy" + "&" +
                "grant_type=" + "authorization_code" + "&" +
                "scope=" + "default")


def connexion(request):

    url = request.get_full_path()

    # Analysez l'URL pour obtenir les paramètres
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Vérifiez si le paramètre 'code' est présent dans les paramètres
    if 'code' in query_params:
        code = query_params['code'][0]


    server_response = requests.post("https://auth.viarezo.fr/oauth/token", data={
                "grant_type":"authorization_code",
                "code":code,
                "redirect_uri": settings.BASE_URL + 'authentication/connexion/',
                "client_id":settings.OAUTH_CLIENT_ID,
                "client_secret":settings.OAUTH_CLIENT_SECRET
    }).json()


    access_token = server_response["access_token"]

    user_infos = requests.get("https://auth.viarezo.fr/api/user/show/me", 
                                    headers={"Authorization":"Bearer "
                                             +access_token}).json()


    username = user_infos['login']

    User = get_user_model()
    existing_user = User.objects.filter(username=username).first()

    if existing_user:
        login(request, existing_user, backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect(settings.LOGIN_REDIRECT_URL)

    
    # Specify user data
    user_data = {
        'username': user_infos['login'],
        'email': user_infos['email'],
        'password': 'example_password',
    }
    
    # Create the user
    user = User.objects.create_user(**user_data)
    
    # Create an email address entry for the user (required by allauth)
    #email = user_data['email']
    #EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
    
    login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

    return redirect(settings.LOGIN_REDIRECT_URL)
