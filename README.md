# PI Stored

## 1. Wstęp

Ta webowa aplikacja pozwala na przechowywanie do pięciu dowolnych 
plików na serwerze. Jest ona tworzona w sposób symulujący działanie
dwóch serwerów - aplikacyjnego i plikowego. 

Aplikacja powstała w ramach przedmiotu _Programowanie Aplikacji
Mobilnych i Webowych_ prowadzonego na Informatyce Stosowanej na
__Politechnice Warszawskiej__. 

## 2. Wymagania

- Nginx
- uWSGI
- Redis

## 3. Sposób uruchomienia

Jako, że aplikacja ma w założeniu symulować dwa serwery, to należy
uruchomić dwie aplikacje. 

- Z folderu `webapp` komenda:

```commandline
uwsgi --ini webapp.ini
```

- I analogicznie z poziomu `dl`:

```commandline
uwsgi --ini dl.ini
```

## 4. Wymagane importy

- Flask
- Flask-OAuthlib
- Jinja2
- PyJWT
- Werkzeug
- redis
- requests
- requests-oauthlib