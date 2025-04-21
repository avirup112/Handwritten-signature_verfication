from django.db import models
from django.contrib.auth.models import User

# Model to store original signatures independently
class OriginalSignature(models.Model):
    signature_image = models.ImageField(upload_to='original_signatures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Original Signature {self.id} uploaded at {self.uploaded_at}"

# Model to store user's original signature at registration (can be deprecated or repurposed)
class UserSignature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # original_signature field removed as per new design

    def __str__(self):
        return f"{self.user.username}'s Signature"

# Model to store uploaded signature for verification
class SignatureVerification(models.Model):
    uploaded_signature = models.ImageField(upload_to='uploaded_signatures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uploaded Signature at {self.uploaded_at}"

# Model to store results of verification attempts
class VerificationAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_signature = models.ImageField(upload_to='verification_attempts/')
    result = models.CharField(max_length=10, choices=[('Real', 'Real'), ('Fake', 'Fake')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.result} at {self.timestamp}"
