from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from core import views

from core.views import frontpage,about, privacy_policy, terms_of_service



urlpatterns = [
    path('about/',about, name='about'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('admin/', admin.site.urls),
    path("robots.txt",TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain")),
    path('privacy-policy/',privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('', include('userprofile.urls')),
    path('', include('store.urls')),
    path('',frontpage,name='frontpage'),
    
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)