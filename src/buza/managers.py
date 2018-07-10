from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


def validate_phone(phone):
    if phone.startswith("+27"):
        phone_pattern = re.compile(r'[+]27(\d{9})$')
        return phone_pattern.match(phone)
    else:
        phone_pattern = re.compile(r'0(\d{9})$')
        return phone_pattern.match(phone)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_name, login, password, **kwargs):
        """
        Creates and saves a User with the given email or phone and password.
        """
        if not login:
            raise ValueError('The please set a correct email or phone number')
        if not user_name:
            raise ValueError('The please set a user name')
        if validate_phone(login):
            email = ""
            phone = login
        else:
            # create account via email
            try:
                validate_email(login)
                email = self.normalize_email(login)
                phone = ""
            except ValidationError:
                raise ValidationError("please enter a valid email address")

        user = self.model(email=email, phone=phone, user_name=user_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_email_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_phone_user(self, phone, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(phone, password, **kwargs)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
