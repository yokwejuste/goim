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
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        context[['register_form']] = form

    else:
        form = UserRegistrationForm
        context['register_form'] = form

    return render(request, 'register.html', context)


# Login view for user
def login_go_user(request):
    context = {}
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
        context['login_form'] = form
    return render(request, 'login.html', context)


# Logout for user
def logout_go_user(request):
    logout(request)
    return redirect('login')


@login_required
def choices(request):
    context = {}
    if request.method == "POST":
        return render(request, "choices.html", context)
    else:
        redirect("login")
    return render(request, 'choices.html', context)


def search_result(request):
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
                      })
    else:
        return render(request,
                      "records_search.html", {
                      })


@login_required
def dashboard(request):
    xyz = GoCustomerRegistration.objects.filter(type__contains='student')
    xzy = GoCustomerRegistration.objects.filter(type__contains='tourist')
    yzx = GoCustomerRegistration.objects.filter(type__contains='worker')
    data = [xyz.count(), xzy.count(), yzx.count()]
    arr = []
    book = []
    book2 = []
    for i in range(1, 13):
        arr.append(i)
    for months in arr:
        hello = GoCustomerRegistration.objects.filter(
            time_of_submission__month=months,
            time_of_submission__year=2021
        ).count()
        book.append(hello)
    for months in arr:
        hi = GoCustomerRegistration.objects.filter(
            time_of_submission__month=months,
            time_of_submission__year=2022
        ).count()
        book2.append(hi)
    labels = ['students', 'tourist', 'worker']
    context = {
        'labels': labels,
        'data': data,
        'arr': book,
        'arr_next': book2,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'profile.html', context)


@login_required
def h404(request):
    return render(request, "404.html", {})


def handler404(request, *args):
    return redirect('h404')


@login_required
def preview(request):
    detail = GoCustomerRegistration.objects.all()
    next_event = Event.objects.last()
    context = {
        'detail': detail,
        'event': next_event,
    }
    return render(request, 'customers_preview.html', context)


@login_required
def send_files(request):
    context = {
        'username': username,
    }
    if request.POST:
        form = GoCustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            subject = 'Welcome to new user.'
            context = {
                'username': username,
                'name': name,
            }
            from_email = settings.EMAIL_HOST_USER
            html_message = render_to_string('message.html', context, request)
            recipient_list = [email]
            plain_message = strip_tags(html_message)
            hey = EmailMultiAlternatives(
                subject, plain_message,
                from_email, recipient_list,
                [email],
            )
            hey.attach_alternative(html_message, 'text/html')
            hey.send()
            form.save()
            return redirect('preview')
        else:
            HttpResponse(f'Invalid data from {request.user.username}')
        context[['document_form']] = form

    else:
        form = GoCustomerRegistrationForm
        context['document_form'] = form
    return render(request, 'files.html', context)


def home(request):
    context = {

    }
    return render(request, 'index.html', context)


def customer_detail(request, pk):
    customer = GoCustomerRegistration.objects.get(id=pk)
    context = {
        'customer': customer,
    }

    return render(request, 'customer_detail.html', context)


# def customer_status_submit(request, pk):
#     customer = GoCustomerRegistration.objects.get(id=pk)
#     form = GoCustomerStatusForm
#     if request.POST:
#         form = GoCustomerStatusForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.info(request, 'Customer updated successfully')
#             redirect('preview')
#     context = {
#         'customer': customer,
#         'form': form,
#     }
#
#     return render(request, 'customer_status.html', context)


def customer_status(request, pk):
    client = GoCustomerStatus.objects.get(name=pk)
    customer = GoCustomerRegistration.objects.get(id=pk)
    context = {
        'client': client,
        'customer': customer,
    }
    if request.POST:
        form = GoCustomerStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('preview')
    else:
        form = GoCustomerStatusForm
        context['status_form'] = form

    return render(request, 'customer_status.html', context)


# ////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////


def render_pdf_view(request):
    template_path = 'user_printer.html'
    detail = GoCustomerRegistration.objects.all()
    next_event = Event.objects.all()
    context = {
        'detail': detail,
        'event': next_event,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

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
    context = {
        'detail': detail,
        'event': next_event,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# ////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////AGENDA//////////////////////////////////////////////


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def index(request):
    return HttpResponse('hello')


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
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'event.html', {'form': form})
