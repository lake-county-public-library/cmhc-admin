from django.db import models

class Status(models.Model):
  date = models.DateTimeField('date')
  csv_staged = models.BooleanField(default=False)
  images_staged = models.BooleanField(default=False)
  derivatives_generated = models.BooleanField(default=False)
  pages_generated = models.BooleanField(default=False)
  indexes_rebuilt = models.BooleanField(default=False)
  deploy_aws = models.BooleanField(default=False)
  deploy_local = models.BooleanField(default=False)
  kill_local = models.BooleanField(default=False)

  def __str__(self):
    return "(%i): %s" %(self.id, self.date.strftime("%Y-%m-%d %H:%M:%S"))
