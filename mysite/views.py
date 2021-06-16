from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from polls.forms import JobModelForm
from polls.models import Job, NewUser, AssignedJobs
from django.core.paginator import Paginator

from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import redis


redis = redis.Redis(host='localhost', port='6379')


def index_with_page(request, i):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/')
        return email_authentication(request)

    data = Job.objects.all()
    paginator = Paginator(data, 2)

    page_number = i
    request.session['page'] = i
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        return render(request, 'index_user.html',
                      {'page_obj': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1),
                       'user': request.user})
    else:
        return render(request, 'index.html',
                      {'page_obj': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1),
                       'user': request.user})


def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/')
        return email_authentication(request)

    data = Job.objects.all()
    paginator = Paginator(data, 2)
    try:
        page_obj = paginator.get_page(request.session.get('page'))
        if request.user.is_authenticated:
            return render(request, 'index_user.html',
                          {'page_obj': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1),
                           'user': request.user})
        else:
            return render(request, 'index.html',
                          {'page_obj': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1),
                           'user': request.user})
    except KeyError:
        pass
    page_number = request.GET.get('page')
    request.session['page'] = page_number
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        return render(request, 'index_user.html',
                      {'page_obj': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1),
                       'user': request.user})
    else:
        return render(request, 'index_user.html',
                      {'page_obj': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1),
                       'user': request.user})


def details(request, job_id):
    job = Job.objects.get(pk=job_id)
    if request.method == 'POST':
        job.assigned_user = request.user.username
        job.save()
        assigned_job = AssignedJobs(job=job.title, user=request.user)
        assigned_job.save()
    return render(request, 'details.html', {'job': job, 'user': request.user})


def send_mail(request, user):
    current_site = get_current_site(request)
    token = account_activation_token.make_token(user)
    print(token)
    redis.set(token, user.username, ex=3600)
    message = render_to_string('acc_active_email.html', {
        'user': user, 'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    mail_subject = 'Activate your workTo account.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def email_authentication(request):
    form = UserCreationForm(request.POST)
    try:
        user = User.objects.get(email=form.data['email'])
        send_mail(request, user)
        return HttpResponse('Please confirm your email address to complete the registration.')
    except User.DoesNotExist:
        email = form.data['email']
        return redirect('signup', email)


def signup(request, email):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if is_valid(form):
            if 'master' in form.data:
                user = NewUser.objects.create(
                    user=User.objects.create_user(form.data['username'], form.data['email'], form.data['password']),
                    contractor=True)
            else:
                user = NewUser.objects.create(
                    user=User.objects.create_user(form.data['username'], form.data['email'], form.data['password']),
                    contractor=False)
            user.user.is_active = True
            user.save()
            send_mail(request, user.user)
            return HttpResponse('Please confirm your email address to complete the registration.')
    return render(request, 'signup.html', {'email': email})


def new_task(request):
    if request.user.newuser.contractor:
        if request.method == 'POST':
            if 'add' in request.POST:
                form = UserCreationForm(request.POST)
                job = Job.objects.create(title=form.data['title'], value=form.data['value'],
                                         approx_time=form.data['approx_time'], employer=request.user.username,
                                         date=timezone.now(), description=form.data['description'])
                job.save()
            elif 'exit' in request.POST:
                logout(request)
                return redirect('/')
        form_class = JobModelForm
        return render(request, 'new_task.html', {'form': form_class, 'user': request.user})
    else:
        return HttpResponse('You are not allowed to access this page.')


def is_valid(form):
    if form.data['password'] == form.data['password_rpt']:
        return True
    else:
        return False


def activate(request, uidb64, token):
    print(token)
    try:
        username = redis.get(token)

        user = User.objects.get(username=username.decode("utf-8"))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')
