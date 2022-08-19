from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control form-control-lg',
                'placeholder': 'Benutzername',
                'required': 'true',
                'autofocus': 'true',
                'type': 'email',
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control form-control-lg',
                'placeholder': 'Passwort',
                'required': 'true',
                'minlength': 8,
                'maxlength': 255,
                'type': 'password',
            }
        )
