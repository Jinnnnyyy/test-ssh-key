from django.db import models

# Create your models here.
class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=10)
    jobname = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    welfare = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    salary = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    workyear = models.CharField(max_length=20)
    createtime = models.CharField(max_length=20)

    class Meta:
        db_table = 'job'
