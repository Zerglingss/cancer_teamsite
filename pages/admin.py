from django.contrib import admin
from .models import ContactMessage

from django.core.mail import send_mail


@admin.action(description="Send welcome email")
def send_welcome_email(modeladmin, request, queryset):
    for customer in queryset:
        send_mail(
            subject="Welcome!",
            message="Don't piss off Admiral Jinx.",
            from_email="cancer.teamsite@example.com",
            recipient_list=["cancer.teamsite@gmail.com"],
            fail_silently=False,
        )

class CustomerAdmin(admin.ModelAdmin):
    actions = [send_welcome_email]

admin.site.register(ContactMessage, CustomerAdmin)