# Django Async Views Cancellation Freeze asgi process when  with django-allauth

This project is the minimal condition required to freeze a django `asgi` worker if `django-allauth` is configured.

This was reproduced using django-allauth version `0.59.0` and django `5.0`.

## setup

```bash
python3 -m venv ./venv
pip install -r requirements.txt
source ./venv/bin/activate
```

# start uvicorn in a shell
```bash
python -m uvicorn mysite.asgi:application --host=localhost --reload
```

# Reproduce the bug in another shell
start the request then cancel it with ^C (Ctrl-C)

```bash
curl http://localhost:8000/async_view/
^C
```

If you run again

```bash
curl http://localhost:8000/async_view/
```

The request will never end.

You also cannot kill the process with ^C (Ctrl-C) anymore. You have to kill it with `kill -9 <pid>`.


# The cause

It appears that the bug is caused by the `AccountMiddleware` of `django-allauth`. 

Commenting the line in `settings.py` the problem is gone.

```python

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # this line cause the bug:
    'allauth.account.middleware.AccountMiddleware',
]
```
