from django.db import models


class Material(models.Model):
  material= models.CharField(max_length=20)
  


  def __str__(self):
    return self.material