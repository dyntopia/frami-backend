from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


def get_deleted_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Prescription(models.Model):
    medication = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        related_name='prescriptions',
        on_delete=models.CASCADE,
    )
    prescriber = models.ForeignKey(
        User,
        related_name='prescribed',
        on_delete=models.SET(get_deleted_user),
    )


class Question(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        related_name='questions',
        on_delete=models.CASCADE,
    )
