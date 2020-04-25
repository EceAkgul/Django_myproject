#from ckeditor_uploader.forms import SearchForm
from django.contrib.auth import logout, authenticate, login
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from haber.models import Haber, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Haber.objects.all()[:4]
    category = Category.objects.all()
    dayhabers = Haber.objects.all()[:4]
    lasthabers = Haber.objects.all().order_by('-id')[:4]
    randomhabers = Haber.objects.all().order_by('?')[:4]
    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayhabers': dayhabers,
               'lasthabers': lasthabers,
               'randomhabers': randomhabers}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'hakkimizda.html', context)


def referans(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'referanslar.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydeder
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    # form=ContactFormu()
    context = {'setting': setting,
               'category': category}
    return render(request, 'iletisim.html', context)


def category_habers(request, id):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    habers = Haber.objects.filter(category_id=id)
    context = {'habers': habers,
               'category': category,
               'categorydata': categorydata}
    return render(request, 'habers.html', context)


def haber_detail(request, id):
    category = Category.objects.all()
    haber = Haber.objects.get(pk=id)
    images = Images.objects.filter(haber_id=id)
    comments = Comment.objects.filter(haber_id=id, status= 'True')
    context = {'haber': haber,
               'category': category,
               'images': images,
               'comments':comments
               }
    return render(request, 'haber_detail.html', context)

def haber_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid==0:
                habers = Haber.objects.filter(title__icontains=query)
            else:
                habers=Haber.objects.filter(title__icontains=query, category_id=catid)

            habers = Haber.objects.filter(title__icontains=query)
            context = {
                'habers' :habers,
                'category' : category,


            }
            return render(request,'haber_search.html',context)



    return HttpResponseRedirect('/')

def haber_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        haber = Haber.objects.filter(title__icontains=q)
        results = []
        for rs in haber:
            haber_json = {}
            haber_json = rs.title
            results.append(haber_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    category = Category.objects.all()
    context = {

        'category': category,

    }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate( username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')



    form = SignUpForm()

    category = Category.objects.all()
    context = {

        'category': category,
        'form': form,

    }
    return render(request, 'signup.html', context)

