from django.shortcuts import render,  redirect
from django.core.mail import send_mail
from django.contrib import messages
from store.models import Product

# Create your views here.

from django.template import TemplateDoesNotExist  
from django.shortcuts import render  
import logging  

logger = logging.getLogger(__name__)  

def privacy_policy(request):  
    try:  
        return render(request, 'core/privacy_policy.html')  
    except TemplateDoesNotExist:  
        logger.error("Template does not exist: core/privacy_policy.html")  
        raise

def terms_of_service(request):
    return render(request, 'core/terms_of_service.html')


def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE, user__userprofile__isnull=False).order_by('-created_at')[:6]
    return render(request, 'core/frontpage.html', {
        'products': products
    })
def about(request):
    return render(request,'core/about.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email (configure email settings in settings.py first)
        send_mail(
            f'Contact Form: {subject}',
            f'From: {name} <{email}>\n\n{message}',
            email,
            ['ababahelen9@gmail.com'],  # Replace with your email
            fail_silently=False,
        )
        
        messages.success(request, 'Your message has been sent. We will get back to you soon!')
        return redirect('contact_us')
    
    return render(request, 'core/contactus.html')