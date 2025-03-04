from django.db import models
from django.contrib.auth.hashers import make_password
from django.shortcuts import render

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    security_question_1 = models.CharField(max_length=255, null=True, blank=True)
    security_question_2 = models.CharField(max_length=255, null=True, blank=True)
    security_question_3 = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk:  # Only hash the password if it's a new user or the password is being updated
            self.password = make_password(self.password)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None
def some_view(request):
    customer = request.user.customer 
    return render(request, 'template_name.html', {'Customer': customer})