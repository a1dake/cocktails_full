from api.v1.user.serializers import *

tags = ['User']

user_id = dict(
    operation_description='## Получения ID юзера по токену.\nИспользуется другими сервисами для авторизации.',
    operation_summary='Получения ID юзера по токену',
    tags=tags,
)

profile_destroy = {
    'operation_description': '## Удаление аккаунта пользователя',
    'operation_summary': 'Удаление аккаунта пользователя',
    'tags': tags,
}
