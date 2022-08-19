from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class MinMaxLengthValidator(object):
    def __init__(self, min_length=8, max_length=255):
        self.min_length = min_length
        self.max_length = max_length
        self.message = _('Dass Passwort muss mindestens {} und darf maximal {} Zeichen lang sein.'.format(min_length, max_length))
        self.code = 'password_length'
    
    def validate(self, password, user=None):
        if len(password) < self.min_length or len(password) > self.max_length:
            raise ValidationError(self.message, self.code)
    
    def get_help_text(self):
        return self.message