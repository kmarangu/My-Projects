from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone

import misaka

from events_app.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts",null=True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    # function leaves publish date blank until it's published
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # Function for dealing with approved post
    def approved_comments(self):
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse(
            "vendor:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]

# Going to connect each comment to actual Post
class comments(models.Model):
    post = models.ForeignKey('vendor.Post',related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def def__str__(self):
        return self.text
