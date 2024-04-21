from urllib.parse import urlencode


def encoded_string(query):
    return urlencode(query, True).replace("%40", "@")


def cleanNoneValue(d) -> dict:
    out = {}
    for k in d.keys():
        if d[k] is not None:
            out[k] = d[k]
    return out


def check_required_parameter(value, name):
    if not value and value != 0:
        raise ParameterRequiredException([name])


def check_required_parameters(params):
    """Validate multiple parameters
    params = [
        ['btcusdt', 'symbol'],
        [10, 'price']
    ]

    """
    for p in params:
        check_required_parameter(p[0], p[1])


class ParameterRequiredException(Exception):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return "%s is mandatory, but received empty." % (", ".join(self.params))
