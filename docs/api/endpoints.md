For api overview and usages, check out [this page](overview.md).

[TOC]

# Authentication

This application uses the following for authentication:

+ [django-allauth](https://github.com/pennersr/django-allauth) for web based views. This package
also provides social sign in capabilities, although they are not enabled in boilerplate generated
projects by default. It is also a dependency of django-rest-auth.

+ [django-rest-auth](https://github.com/Tivix/django-rest-auth) - for API endpoints, some of which
are documented here, but until further documentation is completed for our specific application,
[this page](https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html) may be used as a
secondary reference. 

+ [djangorestframework-jwt](https://github.com/GetBlimp/django-rest-framework-jwt) - for JWT support

Environment variable settings:

+ `JWT_EXPIRATION_MINS`: how long a token is valid for
+ `LOGIN_ATTEMPTS`: number of consecutive invalid login attempts before timeout activated 
+ `LOGIN_TIMEOUT_SECS`: length of timeout period when user exceeds login attempts
+ `JWT_REFRESH_DAYS`: how many days a token can be refreshed for before the user has to authenticate again

## Register [/api/auth/registration/]

+ Parameters
    + email (string)
    + password1 (string) - must have uppercase letter, lowercase letter, digit, and special
    character (these criteria are configurable by a backend developer)
    + password2 (string) - must match password1

### Register user [POST]

+ Response 201 (application/json)

        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmNqc2FkYXNkZmZoamRrZmFmZmZmc2hkZmprQGJ5amFrdC5jb20iLCJ1c2VyX2lkIjoiYjhhMjZiM2EtMGZlZC00OGY0LWFlMTktYTIyZDU5MGFiM2E1IiwidXNlcm5hbWUiOiJtYXJjanNhZGFzZGZmaGpka2ZhZmZmZnNoZGZqa0BieWpha3QuY29tIiwib3JpZ19pYXQiOjE0NjczNzcxMzcsImV4cCI6MTQ2NzM3NzE5N30.NbIu-w_R5kXfAsPTU1SMWW1WrqCzDYlFWHTWK7bTD3M",
            "user": {
                "email": "knuth@example.com",
                "first_name": "Donald",
                "last_name": "Knuth"
            }
        }

## Login [/api/auth/login/]

+ Parameters
    + email (string)
    + password (string)
    
### Login user [POST]

+ Response 200 (application/json)

        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmNqc2FkYXNkZmZoamRrZmFmZmZmc2hkZmprQGJ5amFrdC5jb20iLCJ1c2VyX2lkIjoiYjhhMjZiM2EtMGZlZC00OGY0LWFlMTktYTIyZDU5MGFiM2E1IiwidXNlcm5hbWUiOiJtYXJjanNhZGFzZGZmaGpka2ZhZmZmZnNoZGZqa0BieWpha3QuY29tIiwib3JpZ19pYXQiOjE0NjczNzcxMzcsImV4cCI6MTQ2NzM3NzE5N30.NbIu-w_R5kXfAsPTU1SMWW1WrqCzDYlFWHTWK7bTD3M",
            "user": {
                "email": "knuth@example.com",
                "first_name": "Donald",
                "last_name": "Knuth"
            }
        }

## Token Refresh [/api/auth/token-refresh/]

To keep an end-user session from expiring, an API client may hit this endpoint with a _currently
valid_ token in order to receive a new token that will have the same delta as the original. Tokens
may be refreshed continuously in this manner until `JWT_REFRESH_DAYS` is reached, at which point
the user will have to authenticate again. 

+ Parameters
    + token (string) - valid token
    
### Refresh token [POST]

+ Response 200 (application/json)

        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmNqc2FkYXNkZmZoamRrZmFmZmZmc2hkZmprQGJ5amFrdC5jb20iLCJ1c2VyX2lkIjoiYjhhMjZiM2EtMGZlZC00OGY0LWFlMTktYTIyZDU5MGFiM2E1IiwidXNlcm5hbWUiOiJtYXJjanNhZGFzZGZmaGpka2ZhZmZmZnNoZGZqa0BieWpha3QuY29tIiwib3JpZ19pYXQiOjE0NjczODk3MDUsImV4cCI6MTQ2NzM4OTc3M30.tJqP04iDHisFKo8uBodo61-kY0EA1JNnUSMfJd2dU8Q"
        }

## User [/api/auth/user/]

+ Headers
    + Authorization (string) - JWT token, prefixed with "jwt " (ie. `Authorization: jwt <token>`)

### Get user [GET]

+ Response 200 (application/json)

        {
            "email": "knuth@example.com",
            "first_name": "Donald",
            "last_name": "Knuth"
        }

### Update user [PATCH]

+ Response 200 (application/json)

        {
            "email": "alan@example.com",
            "first_name": "Alan",
            "last_name": "Turing"
        }


