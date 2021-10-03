import calendar
from datetime import datetime, date, timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# \\\\\\\\\\\\\\Pdf imports ////////////////
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.views import generic
from xhtml2pdf import pisa

from .forms import *
from .models import *
from .utils import Calendar

username = GoUser.username


# Registration View of the user

def register(request):
    co_1 = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        co_1['register_form'] = form

    else:
        form = UserRegistrationForm
        co_1['register_form'] = form

    return render(request, 'register.html', co_1)


# Login view for user
def login_go_user(request):
    con_a = {}
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST['username']
            password = request.POST['password']
            user = authenticate(
                request,
                username=user_name,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserLoginForm
        con_a['login_form'] = form
    return render(request, 'login.html', con_a)


# Logout for user
def logout_go_user(request):
    logout(request)
    return redirect('login')


@login_required
def choices(request):
    cont = {}
    if request.method == "POST":
        return render(request, "choices.html", cont)
    else:
        redirect("login")
    return render(request, 'choices.html', cont)


def search_result(request):
    go = GoCustomerRegistration.objects.all()
    if request.method == "POST":
        search = request.POST['search']
        results = \
            GoCustomerRegistration.objects.filter(
                name__contains=search
            )
        return render(request,
                      "records_search.html", {
                          'search': search,
                          'results': results,
                          'cost': go,
                      })
    else:
        return render(request,
                      "records_search.html", {
                          'cost': go,
                      })


@login_required
def dashboard(request):
    go = GoCustomerRegistration.objects.all()
    xyz = GoCustomerRegistration.objects.filter(type__contains='student')
    xzy = GoCustomerRegistration.objects.filter(type__contains='tourist')
    yzx = GoCustomerRegistration.objects.filter(type__contains='worker')
    data = [xyz.count(), xzy.count(), yzx.count()]
    arr = []
    book = []
    book2 = []
    today_date = date.today()
    for i in range(1, 13):
        arr.append(i)
    for months in arr:
        hello_p = GoCustomerRegistration.objects.filter(
            time_of_submission__month=months,
            time_of_submission__year=today_date.year
        ).count()
        book.append(hello_p)
    for months in arr:
        hi = GoCustomerRegistration.objects.filter(
            time_of_submission__month=months,
            time_of_submission__year=2022
        ).count()
        book2.append(hi)
    labels = ['students', 'tourist', 'worker']
    context_p = {
        'labels': labels,
        'data': data,
        'arr': book,
        'arr_next': book2,
        'cost': go,
    }
    return render(request, 'dashboard.html', context_p)


@login_required
def profile(request):
    go = GoCustomerRegistration.objects.all()
    con = {
        'cost': go,
    }
    return render(request, 'profile.html', con)


@login_required
def h404(request):
    return render(request, "404.html", {})


def handler404(request, *args):
    return redirect('h404')


global hell


@login_required
def preview(request):
    global half
    detail = GoCustomerRegistration.objects.all()
    go = GoCustomerRegistration.objects.all()
    arr = GoCustomerStatus.objects.all()
    next_event = Event.objects.all()
    hey_d = ['primary', 'secondary',
             'success', 'danger', 'warning', 'info', 'dark'
             ]
    hey_p = hey_d * 400
    listing = zip(detail, arr, next_event, hey_p)
    conf_o = {
        'list': listing,
        'detail': detail,
        'event': next_event,
        # 'hello': half,
        'cost': go,
    }
    return render(request, 'customers_preview.html', conf_o)


@login_required
def email(request):
    context1 = {
    }
    global context
    global messages
    add = GoCustomerRegistration.objects.all()
    arr = []
    for a in add:
        arr.append(a.email)
    print(arr)
    if request.POST:
        subject = request.POST['title']
        email_1 = request.POST['message']
        recipient_list = arr
        from_email = settings.EMAIL_HOST_USER
        plain_message = strip_tags(email_1)
        hey = EmailMultiAlternatives(
            subject, plain_message,
            from_email, recipient_list,
        )
        hey.attach_alternative(email_1, 'text/html')
        hey.send()
        h = hey.send()
        messages = 'Emails sent successfully'
        context = {
            'messages': messages,
            'h': h,
        }
        return render(request, 'email.html', context)
    return render(request, 'email.html', context1)


@login_required
def email_user(request):
    global contexter
    add = GoCustomerRegistration.objects.all()
    arr = []
    for a in add:
        arr.append(a.email)
    print(arr)
    contexter = {
        'add': add,
    }
    global messages
    if request.POST:
        subject = request.POST['title']
        email_1 = request.POST['message']
        email = request.POST['email']
        recipient_list = [email]
        from_email = settings.EMAIL_HOST_USER
        plain_message = strip_tags(email_1)
        hey = EmailMultiAlternatives(
            subject, plain_message,
            from_email, recipient_list,
        )
        hey.attach_alternative(email_1, 'text/html')
        hey.send()
        h = hey.send()
        messages = 'Emails sent successfully'
        context = {
            'messages': messages,
            'h': h,
        }
        return render(request, 'email_user.html', context)
    return render(request, 'email_user.html', contexter)


@login_required
def send_files(request):
    cong = {
        'username': username,
    }
    if request.POST:
        form = GoCustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            email_d = request.POST['email']
            subject = 'Welcome to new user.'
            cong = {
                'username': username,
                'name': name,
            }
            from_email = settings.EMAIL_HOST_USER
            html_message = render_to_string('message.html', cong, request)
            recipient_list = [email_d]
            plain_message = strip_tags(html_message)
            hey = EmailMultiAlternatives(
                subject, plain_message,
                from_email, recipient_list,
                [email_d],
            )
            hey.attach_alternative(html_message, 'text/html')
            hey.send()
            form.save()
            return redirect('customer_status')
        else:
            HttpResponse(f'Invalid data from {request.user.username}')
        cong['document_form'] = form

    else:
        form = GoCustomerRegistrationForm
        cong['document_form'] = form
    return render(request, 'files.html', cong)


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    context_c = {

    }
    return render(request, 'index.html', context_c)


def customer_detail(request, pk):
    customer = GoCustomerRegistration.objects.get(id=pk)
    custom = GoCustomerStatus.objects.get(name_id=pk)
    context_z = {
        'customer': customer,
        'custom': custom,
    }

    return render(request, 'customer_detail.html', context_z)


def customer_status_change(request, customer_status_id=None):
    if customer_status_id:
        instance = get_object_or_404(GoCustomerStatus, pk=customer_status_id)
    else:
        instance = GoCustomerStatus()

    form = GoCustomerStatusForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        its = request.POST['name']
        name_k = GoCustomerRegistration.objects.get(pk=its)
        email_d = GoCustomerRegistration.objects.get(pk=its)
        new_val = request.POST['value']
        subject_d = f'{name_k} has Changed Status.'
        cong = {
            'username': username,
            'name': name_k.name,
            'new_value': new_val,
        }
        from_email = settings.EMAIL_HOST_USER
        html_message = render_to_string('status_message.html', cong, request)
        recipient_list = [email_d.email]
        plain_message = strip_tags(html_message)
        hey = EmailMultiAlternatives(
            subject_d, plain_message,
            from_email, recipient_list,
            [email_d],
        )
        hey.attach_alternative(html_message, 'text/html')
        hey.send()
        form.save()
        return redirect('event_new')
    context_k = {
        'form': form,
    }
    return render(request, 'customer_status.html', context_k)


def customer_status(request, customer_status_id=None):
    customer = GoCustomerRegistration.objects.get(pk=customer_status_id)
    if customer_status_id:
        instance = get_object_or_404(GoCustomerStatus, pk=customer_status_id)
    else:
        instance = GoCustomerStatus()

    form = GoCustomerStatusForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        name_k = GoCustomerRegistration.objects.get(pk=customer_status_id)
        nose = GoCustomerStatus.objects.get(pk=customer_status_id)
        email_d = GoCustomerRegistration.objects.get(pk=customer_status_id)
        new_val = request.POST['value']
        subject_d = f'{name_k} has Changed Status.'
        cong = {
            'username': username,
            'name': name_k.name,
            'nose': nose.value,
            'new_value': new_val,
        }
        from_email = settings.EMAIL_HOST_USER
        html_message = render_to_string('status_message.html', cong, request)
        recipient_list = [email_d.email]
        plain_message = strip_tags(html_message)
        hey = EmailMultiAlternatives(
            subject_d, plain_message,
            from_email, recipient_list,
            [email_d],
        )
        hey.attach_alternative(html_message, 'text/html')
        hey.send()
        form.save()
        return redirect('preview')
    context_q = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'customer_status.html', context_q)


def render_pdf_view(request):
    template_path = 'user_printer.html'
    detail = GoCustomerRegistration.objects.all()
    next_event = Event.objects.all()
    contest = {
        'detail': detail,
        'event': next_event,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(contest)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_download(request):
    template_path = 'user_printer.html'
    detail = GoCustomerRegistration.objects.all()
    next_event = Event.objects.all()
    context_se = {
        'detail': detail,
        'event': next_event,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context_se)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# /////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////AGENDA//////////////////////////////////////////////


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context_di = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context_di['calendar'] = mark_safe(html_cal)
        context_di['prev_month'] = prev_month(d)
        context_di['next_month'] = next_month(d)
        return context_di


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    previous_month = first - timedelta(days=1)
    month = 'month=' + str(previous_month.year) + '-' + str(previous_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_months = last + timedelta(days=1)
    month = 'month=' + str(next_months.year) + '-' + str(next_months.month)
    return month


def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        subject = request.POST['title']
        email_1 = request.POST['customer']
        email_2 = request.POST['description']
        gr_o_to = GoCustomerRegistration.objects.get(pk=email_1).email
        recipient_list = [gr_o_to]
        from_email = settings.EMAIL_HOST_USER
        plain_message = strip_tags(email_2)
        hey = EmailMultiAlternatives(
            subject, plain_message,
            from_email, recipient_list,
        )
        hey.attach_alternative(email_2, 'text/html')
        hey.send()
        form.save()
        return HttpResponseRedirect(reverse('preview'))
    return render(request, 'event.html', {'form': form})


def handler500(request):
    return render(request, '500.html', status=500)
