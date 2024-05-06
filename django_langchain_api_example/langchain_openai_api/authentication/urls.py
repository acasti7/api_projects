from rest_framework.authtoken import views
from django.urls import path
from .views import auth

urlpatterns =[
    path('get-auth/', views.obtain_auth_token),
    path('register/', auth)
]

'''
1. User Authentication:
Initially, the user provides their credentials (username and password) to the server.
The server verifies these credentials against its database to authenticate the user.

2. Token Generation:
Upon successful authentication, the server generates a unique token.
This token is cryptographically signed by the server using a secret key.

3. Token Transmission:
The server sends this token back to the client (typically as part of the response to the authentication request).
The client (e.g., a web browser or mobile app) receives the token and stores it securely. Common storage mechanisms include browser cookies, local storage, or device storage.

4. Subsequent Requests:
For every subsequent request that requires authentication (e.g., accessing protected resources or endpoints), the client includes the token in the request.
This token is usually sent in the HTTP headers (commonly in the Authorization header) or as a parameter in the request URL or body.

5. Token Validation:
When the server receives a request with a token, it validates the token's authenticity and integrity.
It verifies the signature of the token using the secret key that was used to sign it during token generation.
If the signature is valid and the token is not expired, the server considers the request authenticated and processes it accordingly.

6. Expiration and Renewal:
Tokens typically have an expiration time to enhance security.
If a token expires, the client must request a new token by re-authenticating with the server using their credentials.

7. Revocation:
In some systems, there might be a mechanism for revoking tokens before their expiration time (e.g., if a user logs out or their account is compromised).
Revocation might involve maintaining a blacklist of revoked tokens on the server side.

'''