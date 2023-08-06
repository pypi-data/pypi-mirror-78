from django.utils.translation import ugettext_lazy as _

from .classes import CredentialBackend


class OAuthAccessToken(CredentialBackend):
    class_fields = ('access_token',)
    field_order = ('access_token',)
    fields = {
        'access_token': {
            'label': _('Access token'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'Generated access token used to make API calls '
                'without going through the OAuth authorization flow.'
            ), 'kwargs': {
                'max_length': 248
            }, 'required': True
        },
    }
    label = _('OAuth access token')
    widgets = {
        'access_token': {
            'class': 'django.forms.widgets.PasswordInput',
            'kwargs': {
                'render_value': True
            }
        }
    }


class UsernamePassword(CredentialBackend):
    class_fields = ('username', 'password',)
    field_order = ('username', 'password',)
    fields = {
        'username': {
            'label': _('Username'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'Pseudonym used to identify a user.'
            ), 'kwargs': {
                'max_length': 254
            }, 'required': False
        }, 'password': {
            'label': _('Password'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'Character string used to authenticate the user.'
            ), 'kwargs': {
                'max_length': 192
            }, 'required': False
        },
    }
    label = _('Username and password')
    widgets = {
        'password': {
            'class': 'django.forms.widgets.PasswordInput',
            'kwargs': {
                'render_value': True
            }
        }
    }
