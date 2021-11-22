from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField(max_length=7000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default='Deleted user')
    date_created = models.TimeField(auto_now_add=True, verbose_name='date created')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogpost_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Blog post'
        verbose_name_plural = 'Blog posts'


def pre_save_blogpost_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + instance.title)


pre_save.connect(pre_save_blogpost_receiver, sender=BlogPost)
