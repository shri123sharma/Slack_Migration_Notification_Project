from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Category(models.Model):
  name=models.CharField(max_length=255,null=False,blank=False)
  # category_last_update=models.DateField(auto_now=False)

  def __str__(self):
    return self.name
  
class Language(models.Model):
  language_name=models.CharField(max_length=255,null=False,blank=False)
  language_type=models.CharField(max_length=200,null=True,blank=True)
  language_last_date=models.DateField(auto_now=True,help_text='this field in date format will be updated')

  def __str__(self):
    return self.language_name
  
class Film(models.Model):
  title=models.CharField(max_length=255,null=False,blank=False)
  description=models.TextField()
  film_language=models.ForeignKey(Language,null=True,blank=True,related_name='language_film',on_delete=models.CASCADE)
  release_date=models.DateField(auto_now_add=True)
  rental_duration=models.SmallIntegerField(null=False,default=0.0)
  length=models.SmallIntegerField(default=0)
  rental_rate=models.DecimalField(max_digits=5, decimal_places=3,null=False,default=0.0)
  rating=models.IntegerField(default=0,null=False)
  film_last_update=models.DateField(auto_now=True)

  def __str__(self):
    return self.title
  
class FilmCategory(models.Model):
  category=models.OneToOneField(Category,null=True,blank=True,on_delete=models.CASCADE)
  film=models.OneToOneField(Film,null=True,blank=True,on_delete=models.CASCADE)
  film_category_last_update=models.DateField(auto_now=True)

  
class Actor(models.Model):
  first_name=models.CharField(max_length=255,null=False,blank=False,help_text='enter actor first_name')
  last_name=models.CharField(max_length=255,null=False,blank=False,help_text='enter actor last_name')
  actor_email=models.EmailField(max_length=255,null=False,blank=False)
  last_update=models.DateField(auto_now=True)

  def __str__(self):
    return "actor"+"  "+self.first_name+self.last_name
      
class FilmActor(models.Model):
  actor=models.OneToOneField(Actor,null=True,blank=True,on_delete=models.CASCADE,help_text='One to one relation field')
  film_actor=models.OneToOneField(Film,null=True,blank=True,on_delete=models.CASCADE)
  actor_last_update=models.DateField(auto_now=True)

  def __str__(self):
    return str(self.actor_film) + "_" +str(self.actor)


class Country_Model(models.Model):
  country_name=models.CharField(max_length=255,null=False,blank=False)
  last_update=models.DateField(auto_now=True)

  def __str__(self):
    return self.country_name
  
class City(models.Model):
  country=models.ForeignKey(Country_Model,null=True,blank=True,related_name='country_city',on_delete=models.CASCADE,help_text='foriegn key relation field')
  city_name=models.CharField(max_length=255,null=False,blank=False)
  last_update=models.DateField(auto_now=True)

  def __str__(self):
    return self.city_name

class Address(models.Model):
  city=models.ForeignKey(City,null=True,blank=True,related_name='city_address',on_delete=models.CASCADE)
  address_1=models.CharField(max_length=255,null=False,blank=False)
  address_2=models.CharField(max_length=255,null=True,blank=True)
  district=models.CharField(max_length=255,null=False,blank=False)
  postal_code=models.CharField(max_length=255,null=True,blank=True)
  phone=models.CharField(max_length=10,null=False,blank=False)
  last_update=models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.address_1


class Staff(models.Model):
  staff_address=models.ForeignKey(Address,null=True,blank=True,related_name='staff_address',on_delete=models.CASCADE)
  username=models.CharField(max_length=255,null=False,blank=False)
  password=models.CharField(max_length=255,null=False,blank=False)
  first_name=models.CharField(max_length=255,null=False,blank=False)
  last_name=models.CharField(max_length=255,null=False,blank=False)
  email=models.EmailField(max_length=255,unique=True,null=False,blank=False)
  active=models.BooleanField(default=False,null=False,blank=False)
  last_update=models.DateField(auto_now=True)

  def __str__(self):
    return '{} {}'.format(self.first_name, self.last_name)
  
class Customer(models.Model):
  first_name=models.CharField(max_length=255,null=False,blank=False,help_text='Please enter your first name')
  last_name=models.CharField(max_length=250,null=False,blank=True,help_text='Please enter your last name')
  email=models.EmailField(max_length=100,null=True,blank=True,unique=True,help_text='Please enter your email address')
  address_customer=models.ForeignKey(Address,null=True,blank=True,on_delete=models.CASCADE,related_name='customer_address')
  active_bool=models.BooleanField(default=0)
  create_date=models.DateField(auto_now_add=True)
  last_update=models.DateField(auto_now=True)
  active=models.BooleanField(default=False)

  def __str__(self):
    return self.first_name + " " + self.last_name

class Rental(models.Model):
  rental_film=models.ForeignKey(Film,null=True,blank=True,related_name='film_rental',on_delete=models.CASCADE)
  customer_rental=models.OneToOneField(Customer,null=True,blank=True,on_delete=models.CASCADE)
  rental_staff=models.ForeignKey(Staff,null=True,blank=True,related_name='rental_staff',on_delete=models.CASCADE)
  rental_date=models.DateField(auto_created=True)
  return_date=models.DateField()
  last_update=models.DateField(auto_now=True)

  def __str__(self):
    return '{} {} {}'.format(self.rental_film,self.customer_rental.first_name,self.last_update)
  
class Payment(models.Model):
  customer_payment=models.ForeignKey(Customer,null=True,blank=True,related_name='customer_payment',on_delete=models.CASCADE)
  rental=models.ForeignKey(Rental,null=True,blank=True,related_name='rental_payment',on_delete=models.CASCADE)
  staff_payment=models.ForeignKey(Staff,null=True,blank=True,related_name='staff_payment',on_delete=models.CASCADE)
  amount=models.BigIntegerField(null=False,blank=False,default=0)
  payment_date=models.DateField(auto_now=True)

  def __str__(self):
    return '{}{}{}{}'.format(self.customer_payment,' ',self.rental,' ',self.staff_payment,' ',self.amount)

