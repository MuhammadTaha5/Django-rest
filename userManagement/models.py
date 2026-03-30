from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20)
    user_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    city = models.CharField()

    def __str__(self):
        return self.emp_name
