from .bag import Bag


def bag(request):
    return {'bag': Bag(request)}
