def check_offset_and_limit(offset: str | int = None, limit: str | int = None) -> tuple[int, int]:
    """
    Проверка параметров "offset" и "limit" и изменение их типа на числовой в случае успеха.

    :param offset: смещение по списку историй
    :param limit: ограничение списка историй
    :return: tuple[int, int]
    """
    if not offset:
        offset = 0
    else:
        if not isinstance(offset, int):
            offset = int(offset)

        if offset < 0:
            raise TypeError('Параметр "offset" отрицательный.')

    if not limit:
        limit = offset + 5
    else:
        if not isinstance(limit, int):
            limit = int(limit)

        if limit < 0:
            raise TypeError('Параметр "limit" отрицательный.')
        if offset >= limit:
            raise TypeError('Параметр "offset" больше или равен параметру "limit".')
        if limit - offset > 30:
            raise TypeError('Превышен лимит. Необходимо увеличить параметр "offset" или уменьшить параметр "limit"')

    return offset, limit
