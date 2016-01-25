from django.http import HttpResponseNotAllowed

def post_only(func):# pragma: no cover
    def decorated(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['GET'])
        return func(request, *args, **kwargs)
    return decorated

def get_only(func):# pragma: no cover
    def decorated(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['POST'])
        return func(request, *args, **kwargs)
    return decorated

def generate_registration_code():
    import random
    key = []
    # add 6 letters or numbers to key
    for i in range(6):
        # determine if I should add number or letter
        decider = random.random()

        # 1/2 of the time, add a number between 0 and 9, inclusive
        if decider < (1/float(2)):
            adder = str(random.randint(0, 9))

        # 1/2 of the time, add uppercase letter
        else:
            adder = chr(random.randint(65, 90))

        # append adder to key
        key.append(adder)

    return ("".join(key))
