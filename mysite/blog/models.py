from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    # function leaves publish date blank until it's published
    def publish(self):
        self.published_date = timezone.now()
        self.save()

        # Function for dealing with approved post
    def approved_comments(self):
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

# Going to connect each comment to actual post
class comments(models.Model):
    post = models.ForeignKey('blog.post',related_name='comments', on_delete=models.CASCADE)
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
