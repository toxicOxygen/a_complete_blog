from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.
STATUS_CHOICES = (
    ('draft','Draft'),
    ('published','Published')
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',args=[str(self.slug),])
    
    def get_post_share_url(self):
        return reverse('post-share',args=[str(self.slug),])


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Comment by {} on {}".format(self.name,self.post)
