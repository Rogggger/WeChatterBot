# coding : utf-8


def deal(any):
    if isinstance(any, dict):
        return deal_dict(any)
    elif isinstance(any, list):
        return deal_list(any)
    else:
        return any


def deal_dict(dic):
    return ''.join('{}:{}'.format(deal(key), deal(val)) for key, val in dic.items())


def deal_list(lis):
    return ''.join('{}'.format(deal(one)) for one in lis)


def compose_error(errors, code):
    errors = deal(errors)
    return {
        'error': errors,
        'code': code
    }
