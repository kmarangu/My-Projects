# Generated by Django 2.0.5 on 2018-10-30 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('service_category', multiselectfield.db.fields.MultiSelectField(choices=[('Marquee', 'Marquee'), ('Pagodas', 'Pagodas'), ('Luxury Marquees', 'Luxury Marquees'), ('Capri Marquees', 'Capri Marquees'), ('Traditional Pole Marquees', 'Traditional Pole Marquees'), ('Tipi Hire', 'Tipi Hire'), ('Bell Tents', 'Bell Tents'), ('Clear span marquees', 'Clear span marquees'), ('Chair covers', 'Chair covers'), ('Yurts', 'Yurts'), ('Party Tents', 'Party Tents'), ('Furniture', 'Furniture'), ('Marquee furniture', 'Marquee furniture'), ('Big tops', 'Big tops'), ('Stretch marquee', 'Stretch marquee'), ('marquee floring', 'marquee floring'), ('wedding furniture', 'wedding furniture'), ('Ice Cream Rolls', 'Ice Cream Rolls'), ('Italian Catering', 'Italian Catering'), ('Indian Catering', 'Indian Catering'), ('Kosher Catering', 'Kosher Catering'), ('Goat Roast (Nyama Choma)', 'Goat Roast (Nyama Choma)'), ('Location Catering', 'Location Catering'), ('Bar', 'Bar'), ('Halal Catering', 'Halal Catering'), ('Children Caterers', 'Children Caterers'), ('Caribbean Mobile Catering', 'Caribbean Mobile Catering'), ('Churros', 'Churros'), ('French Catering', 'French Catering'), ('Fun Foods', 'Fun Foods'), ('Mediterranean Catering', 'Mediterranean Catering'), ('Mexican Mobile Catering', 'Mexican Mobile Catering'), ('Pie & Mash Catering', 'Pie & Mash Catering'), ('Vegetarian and vegan catering', 'Vegetarian and vegan catering'), ('Vintage crockery hire', 'Vintage crockery hire'), ('Waffles', 'Waffles'), ('Caribbean Catering', 'Caribbean Catering'), ('Mexican Catering', 'Mexican Catering'), ('Canapes', 'Canapes'), ('Asian Catering', 'Asian Catering'), ('Asian Mobile Catering', 'Asian Mobile Catering'), ('Berberque', 'Berberque'), ('Business Lunch Catering', 'Business Lunch Catering'), ('Afternoon Tea', 'Afternoon Tea'), ('African Catering', 'African Catering'), ('Cocktail Bars', 'Cocktail Bars'), ('Coffee Bars', 'Coffee Bars'), ('Food Vans', 'Food Vans'), ('Pizza Vans', 'Pizza Vans'), ('Crepes Vans', 'Crepes Vans'), ('Fish & Chips Vans', 'Fish & Chips Vans'), ('Paella Catering', 'Paella Catering'), ('Sweets & Candy Carts', 'Sweets & Candy Carts'), ('Jacket Potato Vans', 'Jacket Potato Vans'), ('Candy Floss', 'Candy Floss'), ('Tableware', 'Tableware'), ('Buffets', 'Buffets'), ('Cake Makers', 'Cake Makers'), ('Wedding Cakes', 'Wedding Cakes'), ('Corporate Event Catering', 'Corporate Event Catering'), ('Dinner Party Catering', 'Dinner Party Catering'), ('Private Chef', 'Private Chef'), ('Mobile Caterers', 'Mobile Caterers'), ('Popcorn', 'Popcorn'), ('Private Party Catering', 'Private Party Catering'), ('Refrigiration', 'Refrigiration'), ('Wedding Catering', 'Wedding Catering'), ('Burger Vans', 'Burger Vans'), ('Chocolate Fountain Hire', 'Chocolate Fountain Hire'), ('Cupcakes', 'Cupcakes'), ('Mobile Bars', 'Mobile Bars'), ('Hog Roast', 'Hog Roast'), ('Prosecco Vans', 'Prosecco Vans'), ('Mobile Gin Bars', 'Mobile Gin Bars'), ('Ice Cream Vans', 'Ice Cream Vans'), ('Ice Cream Carts', 'Ice Cream Carts'), ('Hot Dog Stand Hire', 'Hot Dog Stand Hire'), ('Catering Equipments', 'Catering Equipments')], max_length=1203)),
                ('event_type', models.CharField(blank=True, max_length=264)),
                ('private_public', models.CharField(blank=True, max_length=264)),
                ('confirmed_venue', models.CharField(blank=True, max_length=1000)),
                ('speculated_venue', models.CharField(blank=True, max_length=1000)),
                ('event_date', models.DateField(blank=True)),
                ('start_time', models.TimeField(blank=True)),
                ('duration_onsite', models.IntegerField(default=6)),
                ('duration_measure', models.CharField(blank=True, default='Hours', max_length=264)),
                ('description', models.TextField(blank=True, default='')),
                ('contact_mobile', models.CharField(blank=True, max_length=264)),
                ('author_role', models.CharField(blank=True, max_length=264)),
                ('current_stage', models.CharField(blank=True, max_length=264)),
                ('venue_type', models.CharField(blank=True, max_length=264)),
                ('guests_expected', models.CharField(blank=True, max_length=264)),
                ('children_count', models.IntegerField(blank=True)),
                ('payment_terms', models.CharField(blank=True, max_length=264)),
                ('service_level', models.CharField(blank=True, max_length=264)),
                ('terms_conditions', models.CharField(blank=True, max_length=264)),
                ('receive_info', models.CharField(blank=True, max_length=264)),
                ('catering_type', models.CharField(blank=True, max_length=264)),
                ('starters_deserts', models.CharField(blank=True, max_length=264)),
                ('dietary_requirements', models.CharField(blank=True, max_length=264)),
                ('mobile_caterer_type', models.CharField(blank=True, max_length=264)),
                ('power_water', models.CharField(blank=True, max_length=264)),
                ('bar_type', models.CharField(blank=True, max_length=264)),
                ('bar_options', models.CharField(blank=True, max_length=264)),
                ('drink_types', models.CharField(blank=True, max_length=264)),
                ('duration_bar', models.CharField(blank=True, max_length=264)),
                ('inside_outside', models.CharField(blank=True, max_length=264)),
                ('budget_perhead', models.CharField(blank=True, max_length=264)),
                ('funfood_types', models.CharField(blank=True, max_length=264)),
                ('crockery_tableware', models.CharField(blank=True, max_length=264)),
                ('roast_types', models.CharField(blank=True, max_length=264)),
                ('roast_sides', models.CharField(blank=True, max_length=264)),
                ('roast_service', models.CharField(blank=True, max_length=264)),
                ('business_lunchbuffet', models.CharField(blank=True, max_length=264)),
                ('buffet_types', models.CharField(blank=True, max_length=264)),
                ('staff', models.CharField(blank=True, max_length=264)),
                ('flexible_budget', models.BooleanField(default=False)),
                ('hire_crockery', models.BooleanField(default=False)),
                ('drinks_with_tea', models.CharField(blank=True, max_length=264)),
                ('coffee_bar', models.CharField(blank=True, max_length=264)),
                ('drinks_preference', models.CharField(blank=True, max_length=264)),
                ('snack_types', models.CharField(blank=True, max_length=264)),
                ('candyfloss_popcorn', models.CharField(blank=True, max_length=264)),
                ('cakemakers_cupcakes', models.CharField(blank=True, max_length=264)),
                ('catering_services', models.CharField(blank=True, max_length=264)),
                ('icecream_van_cart', models.CharField(blank=True, max_length=264)),
                ('Catering_equipment_types', models.CharField(blank=True, max_length=264)),
                ('tent_structure', models.CharField(blank=True, max_length=264)),
                ('seated_standing', models.CharField(blank=True, max_length=264)),
                ('surface_type', models.CharField(blank=True, max_length=264)),
                ('tent_use', models.CharField(blank=True, max_length=264)),
                ('tent_furnished', models.CharField(blank=True, max_length=264)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('description_html', models.TextField(blank=True, default='', editable=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='memberships', to='events_app.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='events_app.GroupMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together={('group', 'user')},
        ),
    ]
