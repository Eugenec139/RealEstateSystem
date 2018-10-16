from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class MyUserManager(BaseUserManager):
    def create_user(self, email,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # account_type=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # account_type=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    account_type = models.CharField(max_length=30,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Facilitie(models.Model):
    facility_name = models.CharField(max_length=50)

    def __str__(self):
        display_name = str(self.facility_name)
        return display_name


class Countrie(models.Model):
    country_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.country_name)


class Province(models.Model):
    province_name = models.CharField(max_length=50)
    country = models.ForeignKey(Countrie, on_delete=None)

    def __str__(self):
        return str(self.province_name)


class District(models.Model):
    district_name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=None)

    def __str__(self):
        return str(self.district_name)


class Surburb(models.Model):
    surburb_name = models.CharField(max_length=60)
    district = models.ForeignKey(District, on_delete=None)

    def __str__(self):
        return str(self.surburb_name)

class Agencie(models.Model):
    #district = models.ForeignKey(District, on_delete=None)
    agency_name = models.CharField(max_length=40)
    status = models.IntegerField(choices=(
        (1, ("Active")),
        (2, ("Inactive")),
        (3, ("Blocked")),
        (4, ("Suspended")),
        (5, ("Spam"))),
        default=1)
    package = models.IntegerField(choices=(
        (1, ("Free")),
        (2, ("Silver")),
        (3, ("Gold"))),
        default=1)
    address = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    image_logo = models.CharField(max_length=255)
    description = models.TextField(null=True)
    duser = models.IntegerField(null=False ,default= 0)
    phone = models.CharField(max_length=255)
    city = models.CharField(max_length=255,null=True)

    email = models.EmailField(max_length=60)
    website = models.CharField(max_length=255)
    gps_longitude = models.CharField(max_length=50, null=True)
    gps_latitude = models.CharField(max_length=50, null=True)
    twitter = models.TextField(null=True)
    facebook = models.TextField(null=True)
    pintrest = models.TextField(null=True)
    skype = models.TextField(null=True)
    #disclaimer = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.agency_name)

class Agency(models.Model):
    agency_name = models.CharField(max_length=40)
    status = models.IntegerField(choices=(
        (1, ("Active")),
        (2, ("Inactive")),
        (3, ("Blocked")),
        (4, ("Suspended")),
        (5, ("Spam"))),
        default=1)
    package = models.IntegerField(choices=(
        (1, ("Free")),
        (2, ("Silver")),
        (3, ("Gold"))),
        default=1)
    duser = models.IntegerField()
    address = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    image_logo = models.CharField(max_length=255)
    description = models.TextField(null=True)
    phone = models.CharField(max_length=255)
    mobile_number = models.TextField(null=True)
    prop_number = models.TextField(null=True)
    email = models.EmailField(max_length=60)
    website = models.CharField(max_length=255)
    gps_longitude = models.CharField(max_length=50, null=True)
    gps_latitude = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.agency_name)

class ordinaryuser(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    account_status = models.IntegerField(choices=(
        (1, ("Active")),
        (2, ("Inactive")),
        (3, ("Blocked")),
        (4, ("Suspended")),
        (5, ("Spam"))),
        default=2)
    phone_number = models.TextField(null=True)
    mobile_number = models.TextField(null=True)
    prop_number = models.TextField(null=True)
    email_address = models.EmailField(max_length=50, null=True)
    #agency = models.ForeignKey(Agencie, on_delete=None)
    street_address = models.CharField(max_length=50, null=False)
    duser = models.ForeignKey(MyUser, on_delete=None)
    profile_photo = models.TextField(null=True)
    twitter = models.TextField(null=True)
    facebook = models.TextField(null=True)
    pintrest = models.TextField(null=True)
    skype = models.TextField(null=True)
    #bio = models.TextField(null=True)

class Agent(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    account_status = models.IntegerField(choices=(
        (1, ("Active")),
        (2, ("Inactive")),
        (3, ("Blocked")),
        (4, ("Suspended")),
        (5, ("Spam"))),
        default=2)
    phone_number = models.TextField(null=True)
    mobile_number = models.TextField(null=True)
    prop_number = models.TextField(null=True)
    email_address = models.EmailField(max_length=50, null=True)
    agency = models.ForeignKey(Agencie, on_delete=None)
    street_address = models.CharField(max_length=50, null=False)
    duser = models.ForeignKey(MyUser, on_delete=None)
    profile_photo = models.TextField(null=True)
    twitter = models.TextField(null=True)
    facebook = models.TextField(null=True)
    pintrest = models.TextField(null=True)
    skype = models.TextField(null=True)
    bio = models.TextField(null=True)

class pricesincrease(models.Model):
    prop_id = models.IntegerField()
    user_id = models.IntegerField()
    #state = models.BooleanField(default=False)

class pricesdecrease(models.Model):
    prop_id = models.IntegerField()
    user_id = models.IntegerField()


class Bookmarks(models.Model):
    prop_id = models.IntegerField()
    user_id = models.IntegerField()
    state = models.BooleanField(default=False)

class Comments(models.Model):
    msg = models.TextField(null=False)
    name = models.TextField(null=True)
    email = models.TextField(null=True)
    subcomment = models.BooleanField(default=False)
    prop_id = models.IntegerField()
    user_id = models.IntegerField(null=True)
    comm_id = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Prop(models.Model):
    CHOICES = (
        ("House", "House"),
        ("Flat", "Flat"),
        ("Farm", "Farm"),
    )

    CURRENCIES = (
        ("K", "Kwacha"),
        ("$", "Dollars"),
    )
    STATUS = (
        ("For Rent", "For Rent"),
        ("For Sell", "For Sell")
    )
    agency = models.IntegerField(null=True, blank=True)
    agent = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, null=False)
    description = models.TextField(null=True)
    currency = models.CharField(choices=CURRENCIES, max_length=20,
                                default="K",)
    property_price = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    #number_of_rooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    number_of_garages = models.IntegerField()
    area_dimension = models.IntegerField()
    payment_options = models.CharField(max_length=50,
                                       choices=(
                                           ("Cash", "Cash"),
                                           ("Debit", "Debit")))
    property_type = models.CharField(max_length=15,
                                     choices=CHOICES,
                                     default="House", null=False)
    property_status = models.CharField(max_length=20, choices=STATUS, default="For Sell", null=False)
    listing_status = models.IntegerField(choices=(
        (1, ("Active")),
        (2, ("Inactive"))),
        default=1)
    requested_price = models.IntegerField(null=True)
    offered_price = models.IntegerField(null=True)
    #surburb = models.ForeignKey(Surburb, on_delete=None)
    #district = models.ForeignKey(District, on_delete=None)
    gps_longitude = models.CharField(max_length=50, null=True)
    gps_latitude = models.CharField(max_length=50, null=True)
    # usable_m2 = models.CharField(max_length=50, null=False)
    # primary_m2 = models.CharField(max_length=50, null=False)
    # footprint_m2 = models.CharField(max_length=50, null=False)
    year_of_construction = models.DateField(null=True)
    renovated_year = models.DateField(null=True)
    #facilities = models.ManyToManyField(Facilitie, related_name='real_estate_facilities_ref')
    #photos = models.FileField(upload_to='documents/')
  # TODO add uploads model, then use ManyToMany field.
    house_plan_file = models.CharField(max_length=255)
    video = models.CharField(max_length=255 , null=True)
    province = models.TextField(null=True)
    city = models.TextField(null=True)
    town = models.TextField(null=True)
    tags = models.TextField(null=True)
    ord_user = models.BooleanField(default=False)

    #views = models.IntegerField(null=True)


    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
