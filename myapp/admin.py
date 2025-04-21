from django.contrib import admin
from .models import *

admin.site.register(OriginalSignature)
admin.site.register(UserSignature)
admin.site.register(SignatureVerification)
admin.site.register(VerificationAttempt)

