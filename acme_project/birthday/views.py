from django.shortcuts import render


def birthday(request):
    context = {}
    return render(request, 'birthday/birthday.html', context=context)