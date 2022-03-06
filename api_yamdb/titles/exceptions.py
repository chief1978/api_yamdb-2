from rest_framework.exceptions import APIException


class SelfFollow(APIException):
    status_code = 400
    default_detail = 'Нельзя подписаться на самого себя'
    default_code = 'Нельзя_подписаться_на_самого_себя'
