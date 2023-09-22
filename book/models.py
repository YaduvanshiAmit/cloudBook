

# Create your models here.
from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Book(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="UserBook", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # Define a field to store the author of the book
    # author = models.ForeignKey(
    #     User, related_name="authored_books", null=True, blank=True, on_delete=models.SET_NULL)
    
    # Define a ManyToManyField to store collaborators
    collaborators = models.ManyToManyField(User, related_name="collaborations", blank=True)

    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "Book"

    # def save(self, *args, **kwargs):
    #     if not self.author:
    #         self.author = self.user
    #     super().save(*args, **kwargs)

class Chapter(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="UserChapter", on_delete=models.CASCADE)
    EditUser = models.ForeignKey(
        User, related_name="EditUserChapter", on_delete=models.CASCADE, null=True, blank=True,)
    book = models.ForeignKey(Book, related_name='chapters', on_delete=models.CASCADE)
    parent_chapter = models.ForeignKey('self', null=True, blank=True, related_name='child_chapters', on_delete=models.CASCADE)
    section = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "Chapter"


