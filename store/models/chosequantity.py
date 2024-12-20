from django.db import models

class Chosequantity(models.Model):
  Chosequantity= models.CharField(max_length=20)
  
  def __str__(self):
    return self.Chosequantity
