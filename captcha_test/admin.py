from django.contrib import admin
from captcha_test.models import TextCaptcha, ImageCaptcha

# Register your models here.
admin.site.register(TextCaptcha)
admin.site.register(ImageCaptcha)
