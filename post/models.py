from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='posts', verbose_name='Author')
    title = models.CharField(max_length=120, verbose_name='Title')
    body = RichTextField(verbose_name='Body')
    created = models.DateTimeField(verbose_name='Created', auto_now_add=1)
    published = models.BooleanField(verbose_name='Published', default=0)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)

    def __str__(self):
        return self.title

    def edit(self):
        return 'Edit'
    
    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})
    
    def get_edit_url(self):
        return reverse("post:edit", kwargs={"id": self.id})
    
    def get_delete_url(self):
        return reverse("post:delete", kwargs={"id": self.id})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created', 'id']

class Comment(models.Model):

    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)

    name = models.CharField(max_length=200, verbose_name='Comment Owner')
    message = models.TextField(verbose_name='Message')
    created = models.DateTimeField(verbose_name='Created', auto_now_add=1)

    class Meta:
        ordering = ['created']