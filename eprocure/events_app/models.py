from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify

import misaka
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()

from multiselectfield import MultiSelectField

SERVICES=[
            ('Marquee','Marquee'),
            ('Pagodas','Pagodas'),
            ('Luxury Marquees','Luxury Marquees'),
            ('Capri Marquees','Capri Marquees'),
            ('Traditional Pole Marquees','Traditional Pole Marquees'),
            ('Tipi Hire','Tipi Hire'),
            ('Bell Tents','Bell Tents'),
            ('Clear span marquees','Clear span marquees'),
            ('Chair covers','Chair covers'),
            ('Yurts','Yurts'),
            ('Party Tents','Party Tents'),
            ('Furniture','Furniture'),
            ('Marquee furniture','Marquee furniture'),
            ('Big tops','Big tops'),
            ('Stretch marquee','Stretch marquee'),
            ('marquee floring','marquee floring'),
            ('wedding furniture','wedding furniture'),
            ('Ice Cream Rolls','Ice Cream Rolls'),
            ('Italian Catering','Italian Catering'),
            ('Indian Catering','Indian Catering'),
            ('Kosher Catering','Kosher Catering'),
            ('Goat Roast (Nyama Choma)','Goat Roast (Nyama Choma)'),
            ('Location Catering','Location Catering'),
            ('Bar','Bar'),
            ('Halal Catering','Halal Catering'),
            ('Children Caterers','Children Caterers'),
            ('Caribbean Mobile Catering','Caribbean Mobile Catering'),
            ('Churros','Churros'),
            ('French Catering','French Catering'),
            ('Fun Foods','Fun Foods'),
            ('Mediterranean Catering','Mediterranean Catering'),
            ('Mexican Mobile Catering','Mexican Mobile Catering'),
            ('Pie & Mash Catering','Pie & Mash Catering'),
            ('Vegetarian and vegan catering','Vegetarian and vegan catering'),
            ('Vintage crockery hire','Vintage crockery hire'),
            ('Waffles','Waffles'),
            ('Caribbean Catering','Caribbean Catering'),
            ('Mexican Catering','Mexican Catering'),
            ('Canapes','Canapes'),
            ('Asian Catering','Asian Catering'),
            ('Asian Mobile Catering','Asian Mobile Catering'),
            ('Berberque','Berberque'),
            ('Business Lunch Catering','Business Lunch Catering'),
            ('Afternoon Tea','Afternoon Tea'),
            ('African Catering','African Catering'),
            ('Cocktail Bars','Cocktail Bars'),
            ('Coffee Bars','Coffee Bars'),
            ('Food Vans','Food Vans'),
            ('Pizza Vans','Pizza Vans'),
            ('Crepes Vans','Crepes Vans'),
            ('Fish & Chips Vans','Fish & Chips Vans'),
            ('Paella Catering','Paella Catering'),
            ('Sweets & Candy Carts','Sweets & Candy Carts'),
            ('Jacket Potato Vans','Jacket Potato Vans'),
            ('Candy Floss','Candy Floss'),
            ('Tableware','Tableware'),
            ('Buffets','Buffets'),
            ('Cake Makers','Cake Makers'),
            ('Wedding Cakes','Wedding Cakes'),
            ('Corporate Event Catering','Corporate Event Catering'),
            ('Dinner Party Catering','Dinner Party Catering'),
            ('Private Chef','Private Chef'),
            ('Mobile Caterers','Mobile Caterers'),
            ('Popcorn','Popcorn'),
            ('Private Party Catering','Private Party Catering'),
            ('Refrigiration','Refrigiration'),
            ('Wedding Catering','Wedding Catering'),
            ('Burger Vans','Burger Vans'),
            ('Chocolate Fountain Hire','Chocolate Fountain Hire'),
            ('Cupcakes','Cupcakes'),
            ('Mobile Bars','Mobile Bars'),
            ('Hog Roast','Hog Roast'),
            ('Prosecco Vans','Prosecco Vans'),
            ('Mobile Gin Bars','Mobile Gin Bars'),
            ('Ice Cream Vans','Ice Cream Vans'),
            ('Ice Cream Carts','Ice Cream Carts'),
            ('Hot Dog Stand Hire','Hot Dog Stand Hire'),
            ('Catering Equipments','Catering Equipments'),
]

# Models for requesting quote
class Group(models.Model):
    name = models.CharField(max_length=500)
    # service_category = MultiSelectField(choices=SERVICES, max_choices=10)
    service_category = models.CharField(max_length=264,blank=True)
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=264,blank=True)
    private_public = models.CharField(max_length=264,blank=True)
    confirmed_venue = models.CharField(max_length=1000,blank=True)
    speculated_venue = models.CharField(max_length=1000,blank=True,default='Nairobi')
    guests_expected = models.CharField(max_length=264,blank=True)
    # event_date = models.DateField(blank=True)
    event_date = models.CharField(max_length=264,blank=True)
    start_time = models.TimeField(blank=True,default='10:00')
    duration_onsite = models.IntegerField(unique=False,default=6)
    duration_measure = models.CharField(max_length=264,blank=True, default='Hours')
    description = models.TextField(blank=True, default='')
    # Validator regex
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+254722999999' or '0722999999'. Up to 15 digits allowed.")
    contact_mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    author_role = models.CharField(max_length=264,blank=True)
    current_stage = models.CharField(max_length=264,blank=True)
    venue_type = models.CharField(max_length=264,blank=True)
    guests_expected = models.CharField(max_length=264,blank=True)
    children_count = models.IntegerField(unique=False,blank=True,default=0)
    payment_terms = models.CharField(max_length=264,blank=True)
    service_level = models.CharField(max_length=264,blank=True)
    terms_conditions = models.CharField(max_length=264,blank=True)
    receive_info = models.CharField(max_length=264,blank=True)

    # Catering
    catering_type = models.CharField(max_length=264,blank=True)
    starters_deserts = models.CharField(max_length=264,blank=True)
    dietary_requirements = models.CharField(max_length=264,blank=True)
    mobile_caterer_type = models.CharField(max_length=264,blank=True)
    power_water = models.CharField(max_length=264,blank=True)
    bar_type = models.CharField(max_length=264,blank=True)
    bar_options = models.CharField(max_length=264,blank=True)
    drink_types = models.CharField(max_length=264,blank=True)
    duration_bar = models.CharField(max_length=264,blank=True)
    inside_outside = models.CharField(max_length=264,blank=True)
    budget_perhead = models.CharField(max_length=264,blank=True)
    funfood_types = models.CharField(max_length=264,blank=True)
    crockery_tableware = models.CharField(max_length=264,blank=True)
    roast_types = models.CharField(max_length=264,blank=True)
    roast_sides = models.CharField(max_length=264,blank=True)
    roast_service = models.CharField(max_length=264,blank=True)
    business_lunchbuffet = models.CharField(max_length=264,blank=True)
    buffet_types = models.CharField(max_length=264,blank=True)
    staff = models.CharField(max_length=264,blank=True)
    flexible_budget = models.BooleanField(default=False,blank=True)
    hire_crockery = models.BooleanField(default=False,blank=True)
    drinks_with_tea = models.CharField(max_length=264,blank=True)
    coffee_bar = models.CharField(max_length=264,blank=True)
    drinks_preference = models.CharField(max_length=264,blank=True)
    snack_types = models.CharField(max_length=264,blank=True)
    candyfloss_popcorn = models.CharField(max_length=264,blank=True)
    cakemakers_cupcakes = models.CharField(max_length=264,blank=True)
    catering_services = models.CharField(max_length=264,blank=True)
    icecream_van_cart = models.CharField(max_length=264,blank=True)
    Catering_equipment_types = models.CharField(max_length=264,blank=True)

    # Tents
    tent_structure = models.CharField(max_length=264,blank=True)
    seated_standing = models.CharField(max_length=264,blank=True)
    surface_type = models.CharField(max_length=264,blank=True)
    tent_use = models.CharField(max_length=264,blank=True)
    tent_furnished = models.CharField(max_length=264,blank=True)

    created_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True,null=True)

    # slug default max_length is 50 characters
    slug = models.SlugField(max_length=264,allow_unicode=True, unique=True)
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through="GroupMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Saving name using existing fields in the model
        # e.g(wedding on 12/12/2018 requires party tents at karen)
        self.name = self.event_type + " on " + self.event_date + " requires " + self.service_category + " at " + self.confirmed_venue

        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        # super().save(*args, **kwargs)
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user")
