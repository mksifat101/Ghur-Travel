from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command
import contextlib


def error_404(request, exception):
    return render(request, '404.html')


def error_500(request):
    return render(request, '500.html')


def dbbackup(request):
    with contextlib.suppress(Exception):
        call_command('dbbackup')
        return HttpResponse('Databased Backup')
