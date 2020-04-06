from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from haber.models import Haber
from home.models import Setting, ContactFormMessage, ContactFormu


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Haber.objects.all()[:4]
    context = {'setting' : setting,
               'page':'home',
               'sliderdata' : sliderdata}
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting' : setting}
    return render(request, 'hakkimizda.html', context)

def referans(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting' : setting}
    return render(request, 'referanslar.html', context)

def iletisim(request):
    if request.method == 'POST' :
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() #veritabanına kaydeder
            return HttpResponseRedirect('/iletisim')


    setting = Setting.objects.get(pk=1)
    #form=ContactFormu()
    context = {'setting' : setting}
    return render(request, 'iletisim.html', context)