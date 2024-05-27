from django.shortcuts import redirect
import requests
from django.contrib.auth import get_user_model, login
from profiles.models import Association, Profile
from django.contrib import messages
import convention.settings as settings
from urllib.parse import urlparse, parse_qs


def make_linkcs_request(username, access_token):

    url = 'https://api.linkcs.fr/v1/graphql/'
    headers = {'Authorization': "Bearer {}".format(access_token)}

    # La requête GraphQL
    query = f"""
        user(login:"{username}") {{
            firstName
            lastName
            promotion
            roles {{
                label
                sector {{
                    name
                    isBureau
                    composition {{
                        association {{
                            id
                            name
                            type
                        }}
                    }}
                }}
            }}
        }}
        """

    request = requests.get("{url}?query={{{query}}}".format(url=url, query=query), headers=headers).json()
    
    return request['data']
    


def registration(request):
    
    scope = "default linkcs-asso:read linkcs-user:read" # Les scopes nécessaires pour votre requête


    return redirect("https://auth.viarezo.fr/oauth/authorize/?" + "&" +
                    "redirect_uri=" + settings.BASE_URL + 'authentication/connexion/' + "&" +
                    "client_id=" + settings.OAUTH_CLIENT_ID + "&" +
                    "response_type=" + "code" + "&" +
                    "state=" + "MeLlamoLaplayaDeHoy" + "&" +
                    "grant_type=" + "authorization_code" + "&" +
                    "scope=" + scope)


def connexion(request):
    url = request.get_full_path()

    # Analysez l'URL pour obtenir les paramètres
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Vérifiez si le paramètre 'code' est présent dans les paramètres
    if 'code' in query_params:
        code = query_params['code'][0]
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "Erreur lors de la connexion ViaRezo",
        )
        return redirect(settings.LOGIN_REDIRECT_URL)

    server_response = requests.post("https://auth.viarezo.fr/oauth/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.BASE_URL + 'authentication/connexion/',
        "client_id": settings.OAUTH_CLIENT_ID,
        "client_secret": settings.OAUTH_CLIENT_SECRET
    }).json()

    access_token = server_response["access_token"]
    

    user_infos = requests.get("https://auth.viarezo.fr/api/user/show/me",
                              headers={"Authorization": "Bearer "
                                       + access_token}).json()
    
    username = user_infos['login']
    
    data = make_linkcs_request(username, access_token)
    
    promotion = data['user']['promotion']
    roles = data['user']['roles']
    
    asso_objects = []
    
    for role in roles:
        json_asso = role['sector']['composition']['association']
        association_id = json_asso['id']
        association_name = json_asso['name']

        if json_asso['type'] != "ASSOCIATION": continue
        
        asso_object, _ = Association.objects.get_or_create(id=association_id, name=association_name)
        asso_objects.append(asso_object)
        
        
    User = get_user_model()
    existing_user = User.objects.filter(username=username).first()

    if existing_user:
        login(request, existing_user, backend='allauth.account.auth_backends.AuthenticationBackend')
        # On vérifie le statut de la variable display_site_explanation du profile
        profile = Profile.objects.get(user=existing_user)
        
        # On met à jour la promotion de l'utilisateur
        profile.promotion = promotion
        profile.assos.set(asso_objects)
        
        profile.save()
        
        if profile.display_site_explanation:
            return redirect(settings.LOGIN_REDIRECT_URL + "?display_site_explanations=True")

        return redirect(settings.LOGIN_REDIRECT_URL)

    # Specify user data
    user_data = {
        'username': user_infos['login'],
        'email': user_infos['email'],
    }

    # Create the user
    user = User.objects.create_user(**user_data)

    # Create an email address entry for the user (required by allauth)
    # email = user_data['email']
    # EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)

    login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

    # On vérifie le statut de la variable display_site_explanation du profile
    profile = Profile.objects.get(user=user)
    profile.promotion = promotion
    profile.save()
    
    if profile.display_site_explanation:
        return redirect(settings.LOGIN_REDIRECT_URL + "?display_site_explanations=True")

    return redirect(settings.LOGIN_REDIRECT_URL)