# Copyright 2018 by Embrapa.  All rights reserved.
#
# This code is part of the machado distribution and governed by its
# license. Please see the LICENSE.txt and README.md files that should
# have been included as part of this package for licensing information.

"""App settings file."""

from importlib import import_module

from django.conf import settings


def patch_middleware():
    """Include dependencies to MIDDLEWARE."""
    settings.MIDDLEWARE.append("django.contrib.sessions.middleware.SessionMiddleware")
    settings.MIDDLEWARE.append(
        "django.contrib.auth.middleware.AuthenticationMiddleware"
    )
    settings.MIDDLEWARE.append("django.contrib.messages.middleware.MessageMiddleware")


def patch_root_urlconf():
    """Include the machado urls."""
    if hasattr(settings, "ROOT_URLCONF"):
        urlconf_module = import_module(settings.ROOT_URLCONF)
        from machado.urls import urlpatterns

        urlconf_module.urlpatterns += urlpatterns
    else:
        settings.ROOT_URLCONF = "machado.urls"


def patch_swagger_settings():
    """Include swagger settings."""
    settings.SWAGGER_SETTINGS = {
        "USE_SESSION_AUTH": False,
        "DEFAULT_MODEL_DEPTH": 0,
        "SECURITY_DEFINITIONS": False,
    }


def patch_templates():
    """Include dependencies to TEMPLATE."""
    if len(settings.TEMPLATES) == 0:
        settings.TEMPLATES.append(
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ]
                },
            }
        )


def patch_proxy_headers():
    """Include encrypted proxy headers."""
    settings.USE_X_FORWARDED_HOST = True
    settings.SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


def patch_all():
    """Apply patches."""
    patch_root_urlconf()
    patch_middleware()
    patch_templates()
    patch_swagger_settings()
    patch_proxy_headers()

    settings.USE_THOUSAND_SEPARATOR = True
    settings.APPEND_SLASH = True
    settings.USE_TZ = False
