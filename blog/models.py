from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Postdt(models.Model):
    title = models .CharField(max_length = 100)
    content = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User , on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})




#one user can have many posts bu one post has only one user
#user and post model are related as one to many rekation
#for this we use foreign key  Line 9
# to see sql code while u run the migrations 
# we can use python manage.py sqlmigrate BLOG 0001
# by python m