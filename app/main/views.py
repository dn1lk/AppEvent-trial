from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse

from . import models, check_offset_and_limit


def posts(request: HttpRequest) -> HttpResponse:
    """Ответ на GET запрос /posts."""

    def get_response(order: str = None, offset: str = None, limit: str = None, **kwargs):
        """
        Проверка введённых параметров и вывод полученного списка из базы данных.

        :param order: сортировка по атрибуту, если с "-" - по убыванию
        :param offset: смещение по списку историй
        :param limit: ограничение списка историй
        :return: JsonResponse
        """

        if kwargs:
            raise TypeError(f"Получен неизвестный параметр: {list(kwargs)}")
        offset, limit = check_offset_and_limit(offset, limit)

        if order:
            fields = sum(([field.name, f'-{field.name}'] for field in models.Posts._meta.get_fields()), [])

            if order not in fields:
                raise TypeError('Неверный параметр order.\n'
                                f'Возможно одно из следующих значений: {fields}.')

            stories = models.Posts.objects.order_by(order)
        else:
            stories = models.Posts.objects.all()

        return JsonResponse(list(stories[offset:limit].values()), safe=False, json_dumps_params={'indent': 2})
    try:
        return get_response(**request.GET.dict())
    except TypeError as e:
        return HttpResponseBadRequest(e, content_type='application/json')
