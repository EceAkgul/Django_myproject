from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from haber.models import Category, Comment, Haber, HaberFormu
from home.models import UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(pk=current_user.id)

    context = { 'category': category,
                'profile' : profile}
    return render(request, 'user_profile.html',context )

def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category' : category,
            'user_form' : user_form,
            'profile_form' : profile_form
        }
        return render(request, 'user_update.html',context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            print("Başarılı")
            return HttpResponseRedirect('/user')
        else:
           return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',{
            'form' : form, 'category' : category
        })

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id = current_user.id)
    context = {
        'category': category,
        'comments': comments
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):

    current_user = request.user
    Comment.objects.filter(id = id, user_id=current_user.id).delete()

    return HttpResponseRedirect('/user/comments')



@login_required(login_url='/login')
def haber_ekle(request):
    if request.method == 'POST':
        form = HaberFormu(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Haber()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['category']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'Your Content Recorded Successfully ')
            return HttpResponseRedirect('/user/haber_show')
        else:
            messages.error(request, 'Announcement Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/haber_ekle')
    else:
        category = Category.objects.all()
        form = HaberFormu()
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user_addnews.html', context)


@login_required(login_url='/login')
def haber_edit(request, id):
    haber = Haber.objects.get(id=id)
    if request.method == 'POST':
        form = HaberFormu(request.POST, request.FILES, instance=haber)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Announcement Updated Successfully ')
            return HttpResponseRedirect('/user/haber_show')
        else:
            messages.error(request, 'Haber Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/haber_edit' + str(id))
    else:
        category = Category.objects.all()
        form = HaberFormu(instance=haber)
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user_addnews.html', context)


@login_required(login_url='/login')
def haber_show(request):
    category = Category.objects.all()
    current_user = request.user
    haber = Haber.objects.filter(user_id=current_user.id, status='True')
    context = {
        'category': category,
        'haber': haber,
    }
    return render(request, 'user_news.html', context)


@login_required(login_url='/login')
def haber_delete(request, id):
    current_user = request.user
    Haber.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content deleted..')
    return HttpResponseRedirect('/user/haber_show')


