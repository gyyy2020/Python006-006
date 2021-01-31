from django.db import models

# Create your models here.
class Films(models.Model):
    stars = models.IntegerField(verbose_name='星级')
    comments = models.CharField(max_length=1000, verbose_name='评论内容')

