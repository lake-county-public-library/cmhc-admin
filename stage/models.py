from django.db import models

class Status(models.Model):
  date = models.DateTimeField('date')

  def __str__(self):
    return "(%i): %s" %(self.id, self.date.strftime("%Y-%m-%d %H:%M:%S"))
