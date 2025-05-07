from django.shortcuts import render

def vacations(request):
    page = 'vacations'
    page_title = 'Vacations'

    profile = request.user.profile if request.user.is_authenticated else None

    context = {
        'page': page,
        'page_title': page_title,
        'profile': profile,
    }
    return render(request, 'vacations/vacations.html', context)