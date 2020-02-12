from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=70)
    slug = models.CharField(max_length=80)
    content = RichTextUploadingField()

    def __str__(self):
        return self.title
