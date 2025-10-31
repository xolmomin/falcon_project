from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField
from django.forms.utils import ErrorList
from django.utils.timezone import now

from apps.models import User, Order


class LoginForm(Form):
    username = UsernameField(required=True)
    password = CharField(max_length=128, required=True)

    def clean(self):
        cleaned_data = super().clean()

        user = authenticate(**cleaned_data)
        if user is None:
            raise ValidationError("Incorrect username or password")

        self.user = user
        return cleaned_data


class RegisterModelForm(ModelForm):
    confirm_password = CharField(max_length=255, required=True)
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = 'first_name', 'username', 'email', 'password'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")

        if cleaned_data['password'] != cleaned_data.pop('confirm_password'):
            raise ValidationError("Passwords don't match")

        cleaned_data['password'] = make_password(cleaned_data['password'])
        cleaned_data['username'] = cleaned_data['username'].lower()
        return cleaned_data


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['payment_type', 'card_number', 'exp_date', 'cvv']

    def clean(self):
        _data = super().clean()
        if _data['payment_type'] != Order.PaymentType.ONLINE:
            _data.pop('card_number')
            _data.pop('exp_date')
            _data.pop('cvv')
        else:
            if _data['card_number'] is None:
                raise ValidationError("Card number is required")

            if _data['exp_date'] is None:
                raise ValidationError("Expiration date is required")
            _month, _year = _data['exp_date'][:2], _data['exp_date'][2:]

            current_month = str(now().date().month)
            current_year = str(now().date().year)[2:]

            if not (current_year < _year or current_year == _year and current_month < _month):
                raise ValidationError("Expiration date is expired")

            if _data['cvv'] is None:
                raise ValidationError("CVV is required")

            if len(_data['card_number']) != 16 or len(_data['exp_date']) != 4 or len(str(_data['cvv'])) != 3:
                raise ValidationError("Information invalid")

        return _data


class ProfileChangePasswordModelForm(ModelForm):
    old_password = CharField(max_length=128, required=True)
    confirm_password = CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None,
                 request=None):
        self.request = request
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)

    def clean(self):
        _data = super().clean()
        user = self.request.user

        old_password = _data.pop('old_password')
        password = _data.get('password')
        confirm_password = _data.pop('confirm_password')

        if password != confirm_password or not user.check_password(old_password):
            raise ValidationError("Passwords don't match")

        user.set_password(password)
        user.save(update_fields=['password'])
        update_session_auth_hash(self.request, user)
        return _data
