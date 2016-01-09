from reddit.models import Subjeffit


def fetch_subjeffits(request):
    subjeffits = Subjeffit.objects.all()
    return {'subjeffits': subjeffits}
