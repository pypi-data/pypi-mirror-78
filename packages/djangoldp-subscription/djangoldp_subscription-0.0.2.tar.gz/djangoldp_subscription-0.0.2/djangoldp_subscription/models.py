from django.db import models
from djangoldp.models import Model

class Typemember (Model):
    name = models.CharField(max_length=50, verbose_name="Type of member")

    def __str__(self):
        return self.name 

class Gendermember (Model):
    name = models.CharField(max_length=50, verbose_name="Member gender")

    def __str__(self):
        return self.name 

class Member (Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    firstname = models.CharField(max_length=50, blank=True, null=True, verbose_name="First name")
    typemember = models.ForeignKey(Typemember,max_length=50, verbose_name="Type of member")
    gender = models.ForeignKey(Gendermember, blank=True, null=True, max_length=50)
    email = models.CharField(max_length=50, verbose_name="Email") 
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    birthdate = models.CharField(max_length=20, blank=True, null=True, verbose_name="Birth date")
    birthcity = models.CharField(max_length=50, blank=True, null=True, verbose_name="Birth city")
    birthcountry = models.CharField(max_length=50, blank=True, null=True, verbose_name="Birth country")
    corponame = models.CharField(max_length=50, blank=True, null=True,verbose_name="Corporate Name")
    mandat = models.CharField(max_length=50, blank=True, null=True,verbose_name="Social mandate")
    siret = models.IntegerField(max_length=14, blank=True, null=True, verbose_name="Siret")
    numberaddress = models.CharField(max_length=10, verbose_name="Street number")
    streetaddress = models.CharField(max_length=50, verbose_name="Street name")
    zipcode = models.CharField(max_length=10, verbose_name="Zip code")
    cityaddress = models.CharField(max_length=50, verbose_name="City")
    countryaddress = models.CharField(max_length=50, verbose_name="Country")
    mailacceptance = models.BooleanField(verbose_name="acceptance of notification emails")
    changemail = models.BooleanField(verbose_name="Change email validation")
    informationvalidation = models.BooleanField(verbose_name="Risk validation")
    statutes = models.BooleanField(verbose_name="Knowledge of the statutes")
    cavalidation = models.BooleanField(verbose_name="Validation of the CA")
    beneficiciaireconfirmation  = models.BooleanField(verbose_name="Bénéficiaire subscription")
    partquantity = models.IntegerField(max_length=2, verbose_name="Part Quantity")
    iddocument = models.URLField(blank=True, null=True, verbose_name="ID")

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']

    def __str__(self):
        return self.name 
