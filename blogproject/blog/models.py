from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from markdown import Markdown
from django.utils.html import strip_tags
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=64)
    body  = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    #摘要
    digest = models.CharField(max_length=256,blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)

    author = models.ForeignKey(User)
    #文章阅读量
    views = models.PositiveIntegerField(default=0)
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})


    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.digest:
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.digest = strip_tags(md.convert(self.body))[:64]
        super().save(*args,**kwargs)
    class Meta:
        ordering = ['-created_time']
