from rest_framework import serializers
from django.utils.crypto import get_random_string
from apps.user.models import User, TempCode
from base.backends import UsernameBackend
from base.tasks import send_mail
from rest_framework.authtoken.models import Token


__all__ = [
    'WebSignInRequestSerializer',
    'WebSignInResponseSerializer',
    'ResetPasswordSerializer',
    'ConfirmResetCodeSerializer',
    'ConfirmPasswordSerializer',
    'UserRegistrationSerializer',
    'EmailVerificationRequestSerializer',
    'CodeVerificationSerializer',
]


def get_verification_code():
    verification_code = get_random_string(length=4, allowed_chars='0123456789')
    return verification_code


class WebSignInRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    class Meta:
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs: dict):
        self.authenticate(login=attrs['username'], password=attrs['password'])

        if self.user is None:
            raise serializers.ValidationError(dict(errors=['Invalid login or password']))

        if not self.user.is_active:
            raise serializers.ValidationError(dict(errors=['Доступ к этому аккаунту был заблокирован администратором']))

        return attrs

    def authenticate(self, **kwargs):
        back = UsernameBackend()
        self.user: User = back.authenticate(**kwargs)


class WebSignInResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('token', 'roles')

    def get_token(self, obj: User) -> str:
        return self.context.get('token') or obj.auth_token.key  # noqa

    @staticmethod
    def get_roles(obj: User) -> list:
        return obj.roles  # noqa


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        verification_code = get_verification_code()
        temp_reset, created = TempCode.objects.get_or_create(email=self.validated_data['email'])
        temp_reset.verification_code = verification_code
        temp_reset.save()
        self.send_verification_email(temp_reset)

    def send_verification_email(self, temp_reset):
        send_mail(
            subject="Verification Code",
            template_name="mail/password.html",
            context={"code": temp_reset.verification_code},
            to_email=[temp_reset.email]
        )


class ConfirmResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs: dict):
        try:
            temp_reset = TempCode.objects.get(email=attrs['email'], verification_code=attrs['code'])
        except TempCode.DoesNotExist:
            raise serializers.ValidationError(dict(code=['Неверный код']))

        return attrs


class ConfirmPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    repeat_password = serializers.CharField(min_length=8, write_only=True)
    code = serializers.CharField(max_length=4, write_only=True)

    def validate(self, attrs: dict):
        if attrs['new_password'] != attrs['repeat_password']:
            raise serializers.ValidationError(dict(errors=['Пароли не совпадают']))

        try:
            temp_reset = TempCode.objects.get(email=attrs['email'], verification_code=attrs['code'])
        except TempCode.DoesNotExist:
            raise serializers.ValidationError(dict(code=['Неверный код']))

        self.user = User.objects.get(email=attrs['email'])
        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        TempCode.objects.filter(email=self.validated_data['email']).delete()


class EmailVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Этот email уже используется.')
        return value

    def create(self, validated_data):
        email = validated_data['email']
        verification_code = get_verification_code()

        temporary_user, created = TempCode.objects.get_or_create(email=email)
        temporary_user.verification_code = verification_code
        temporary_user.save()

        self.send_verification_email(email, verification_code)
        return temporary_user

    def send_verification_email(self, email, verification_code):
        send_mail(
            subject="Verification Code",
            template_name="mail/password.html",
            context={"code": verification_code},
            to_email=[email]
        )


class CodeVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        try:
            temporary_user = TempCode.objects.get(email=attrs['email'], verification_code=attrs['code'])
        except TempCode.DoesNotExist:
            raise serializers.ValidationError('Неверный код или email.')
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'gender', 'date_of_birth', 'password', 'email']

    def create(self, validated_data):
        # email = self.context['email']
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            email=email,
            username=email,
            password=password,
            **validated_data
        )

        token, _ = Token.objects.get_or_create(user=user)
        return user, token

    def to_representation(self, instance):
        user, token = instance
        data = super().to_representation(user)
        data['token'] = token.key
        return data
