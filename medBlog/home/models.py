from django.db import models
from django.contrib.auth.models import User
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'msg from =  {self.name}'

class Relationship(models.Model):
    who = models.ForeignKey(User, related_name="who", on_delete=models.CASCADE)
    whom = models.ForeignKey(User, related_name="whom", on_delete=models.CASCADE)

    def __str__(self):
        return '{} follows {}'.format(self.who, self.whom)
