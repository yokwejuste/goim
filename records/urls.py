from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from records.views import *

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


urlpatterns = [
                  re_path(r'^favicon\.ico$', favicon_view),
                  path('', home, name='home'),
                  path('register/', register, name='register'),
                  path('login/', login_go_user, name='login'),
                  path('email/', email, name='email'),
                  path('email-user/', email_user, name='email_user'),
                  path('logout/', logout_go_user, name='logout'),
                  path('choices/', choices, name='choices'),
                  path('search/', search_result, name='search'),
                  path('dashboard/', dashboard, name='dashboard'),
                  path('profile/', profile, name='profile'),
                  path('preview/', preview, name='preview'),
                  path('preview/detail', customer_detail, name="sup"),
                  path('query_life_is_good/', h404, name='h404'),
                  url(r'^$', h404, name='page_not_found'),
                  path('pdf', render_pdf_view, name='pdf_view'),
                  path('pdf_d', render_pdf_download, name='pdf_download'),
                  path('upload/', send_files, name='upload'),
                  path('detail/<int:pk>/', customer_detail, name='customer_detail'),
                  path('status/', customer_status_change, name='customer_status'),
                  url(r'^status/edit/(?P<customer_status_id>\d+)/$', customer_status, name='customer'),
                  url(r'^calendar/$', CalendarView.as_view(), name='calendar'),
                  url(r'^event/new/$', event, name='event_new'),
                  url(r'^event/edit/(?P<event_id>\d+)/$', event, name='event_edit'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handlers404 = 'records.views.handlers404'
handlers500 = 'records.views.handlers505'
