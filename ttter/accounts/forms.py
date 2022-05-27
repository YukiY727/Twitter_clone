from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import MyUser


class SignUpFrom(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'username', 'nickname', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.render_value = True
        self.fields['password2'].widget.render_value = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
