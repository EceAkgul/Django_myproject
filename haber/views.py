from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from haber.models import CommentForm, Comment


def index(request):
    return HttpResponse("Haber Sayfası")

#@login_required(login_url = '/login')  #CHECKING
def addcomment(request,id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comment()
            data.user_id = current_user.id
            data.haber_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #message.success(request, "Yorumunuz kaydedilmiştir.")
            url = request.META.get('HTTP_REFERER') # get last url
            return HttpResponseRedirect(url)





