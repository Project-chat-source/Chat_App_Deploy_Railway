import uuid
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.email} - {self.otp_code}"
    



class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True )
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)




class ContactList(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user')
    contacts = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f"Contact List for {self.user.username}"



class Message(models.Model):
    room_name = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} in {self.room_name} at {self.timestamp}"