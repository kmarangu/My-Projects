from django import forms
from django import template
from django.contrib.auth.models import User
from events_app.models import Group,GroupMember

from events_app.models import SERVICES

CATERING_FS1=[
            ('Italian Catering','Italian Catering'),
            ('Indian Catering','Indian Catering'),
            ('Kosher Catering','Kosher Catering'),
            ('Halal Catering','Halal Catering'),
            ('French Catering','French Catering'),
            ('Fun Foods','Fun Foods'),
            ('Mediterranean Catering','Mediterranean Catering'),
            ('Vegetarian and vegan catering','Vegetarian and vegan catering'),
            ('Caribbean Catering','Caribbean Catering'),
            ('Mexican Catering','Mexican Catering'),
            ('Asian Catering','Asian Catering'),
            ('African Catering','African Catering'),
            ('Private Party Catering','Private Party Catering'),
            ('Children Caterers','Children Caterers'),
            ('Wedding Catering','Wedding Catering'),
]

CATERING_FS2=[
            ('Business Lunch Catering','Business Lunch Catering'),
            ('Corporate Event Catering','Corporate Event Catering'),
            ('Dinner Party Catering','Dinner Party Catering'),
            ('Buffets','Buffets'),
            ('Private Chef','Private Chef'),
]

EVENT_TYPES=[('ANNIVERSARY','Anniversary Event'),
             ('BIRTHDAY PARTY','Birthday Party'),
             ('CHARITY EVENT','Charity Event'),
             ('CHILDRENS PARTY','Childrens Party'),
             ('CHRISTENING','Christening'),
             ('CORPORATE EVENT','Corporate Event'),
             ('FESTIVAL','Festival'),
             ('HEN PARTY','Hen Party'),
             ('POLITICAL EVENT','Political Event'),
             ('GRADUATION PARTY','Graduation Party'),
             ('FAMILY REUNION','Family Reunion'),
             ('TRADITIONAL WEDDING','Traditional Wedding'),
             ('STAG PARTY','Stag Party'),
             ('BABY SHOWER','Baby Shower'),
             ('WEDDING','Wedding Ceremony'),
             ('RELIGIOUS EVENT','Religious Event'),
             ('SCHOOL EVENT','School Event'),
             ('FUNERAL','Funeral'),
             ('UNSPECIFIED EVENT','Unspecified Event'),
            ]

PRIVATE_PUBLIC=[('PRIVATE EVENT','Private Event'),
                ('PUBLIC EVENT','Public Event'),
            ]

DURATION_MEASURE=[('MINUTES','Minutes'),
                  ('HOURS','Hours'),
                  ('DAYS','Days'),
            ]

AUTHORS_ROLE=[  ('PARTY HOST','Party Host'),
                ('PROFESSIONAL EVENT PLANNER','Professional Event Planner'),
                ('BRIDE OR GROOM','Bride or Groom'),
                ('OFFICE ADMINISTRATOR','Office Administrator'),
                ('VENUE MANAGER','Venue Manager'),
                ('OTHER','Other'),
            ]

CURRENT_STAGE=[ ('BOOKING STAGE','Booking Stage'),
                ('SOURCING FOR QUOTATIONS','Sourcing For Quotations'),
                ('CHECKING ON PRICES','Checking On Prices'),
                ('JUST TRYING THIS OUT','Just Trying This Out'),
            ]

TERMS_CONDITIONS=[  ('AGREE','I Agree'),
                    ('DISAGREE','I do not Agree'),
            ]

RECEIVE_INFO=[  ('AGREE','I Agree'),
                ('DISAGREE','I do not Agree'),
            ]

CATERING_TYPES=[ ('FORMAL SIT DOWN MEAL','Formal Sit Down Meal'),
                 ('INFORMAL SIT DOWN','Informal Sit Down Meal'),
                 ('SERVED BUFFET','Served Buffet'),
                 ('SELF SERVICE BUFFET','Self Service Buffet'),
                 ('BERBERQUE','Berberque'),
                 ('SPIT ROAST','Spit Roast(Goat,Pig,Chicken e.t.c)'),
                 ('AFTERNOON TEA','Afternoon Tea'),
                 ('CANAPES','Canapés'),
                 ('OPEN TO SUGGESTION','Open to Suggestion'),
            ]

STARTERS_DESERTS=[  ('STARTERS','I want Starters'),
                    ('DESERTS','I want Deserts'),
                    ('BOTH','I want Both'),
                    ('NONE','I do not want neither'),
            ]

DIETARY_REQUIREMENTS=[  ('DAILY INTOLERANT','Daily Intolerant'),
                        ('GLUTEN FREE','Gluten Free'),
                        ('HALAL','Halal'),
                        ('KOSHER','Kosher'),
                        ('NUT ALLERGY','Nut Allergy'),
                        ('VEGAN','Vegan'),
                        ('VEGETARIAN','Vegetarian'),
                        ('OTHER','Other(Kindly Specify)'),
                    ]

VENUE_TYPE=[    ('OUTDOORS WITH NO KITCHEN','Venue is Outdoors with No Kitchen Available'),
                ('OUTDOORS WITH DOMESTIC KITCHEN','Venue is Outdoors with Domestic Kitchen Available'),
                ('OUTDOORS WITH COMMERCIAL KITCHEN','Venue is Outdoors with Commercial Kitchen Available'),
                ('INDOORS WITH DOMESTIC KITCHEN','Venue is Indoors with Domestic Kitchen Available'),
                ('INDOORS WITH COMMERCIAL KITCHEN','Venue is Indoor with Commercial Kitchen Available'),
                ('INDOORS WITH NO KITCHEN','Venue is Indoor with No Kitchen Available'),
            ]

GUESTS_EXPECTED=[   ('10 or less','10 or less'),
                    ('11 - 20','11 - 20'),
                    ('21 - 30','21 - 30'),
                    ('31 - 40','31 - 40'),
                    ('41 - 50','41 - 50'),
                    ('51 - 60','51 - 60'),
                    ('61 - 70','61 - 70'),
                    ('71 - 80','71 - 80'),
                    ('81 - 90','81 - 90'),
                    ('91 - 100','91 - 100'),
                    ('101 - 125','101 - 125'),
                    ('126 - 150','126 - 150'),
                    ('151 - 200','151 - 200'),
                    ('201 - 250','201 - 250'),
                    ('251 - 300','251 - 300'),
                    ('301 - 350','301 - 350'),
                    ('351 - 400','351 - 400'),
                    ('401 - 450','401 - 450'),
                    ('451 - 500','451 - 500'),
                    ('MORE THAN 500','More than 500'),
                ]

PAYMENT_TERMS=[ ('WE WILL PAY UPFRONT','We will make payment upfront'),
                ('GUESTS WILL PAY','Guests will pay themselves'),
            ]

SERVICE_LEVEL=[ ('BASIC','Basic Service $'),
                ('STANDARD','Standard Service $$'),
                ('PREMIUM','Premium Service $$$'),
                ('HIGH END','Hold Nothing Back $$$$'),
            ]

MOBILE_CATERER_TYPE=[   ('GAZEBO','Gazebo'),
                        ('MODERN VAN OR TRAILER','Modern Van or Trailer'),
                        ('VINTAGE VAN OR TRAILER','Vintage Van or Trailer'),
            ]

POWER_WATER=[   ('YES BOTH AVAILABLE','Yes both are available'),
                ('POWER ONLY','Only power is available'),
                ('WATER ONLY','Only water is available'),
                ('NEITHER IS AVAILABLE','Neither is available'),
                ('NOT SURE','I am not sure'),
            ]

BAR_TYPE=[  ('POP UP BAR COUNTER','Pop Up Bar Counter'),
            ('CONVERTED CAR','A Car Converted to Bar Counter'),
        ]
# Checkbox
BAR_OPTIONS=[   ('DRY HIRE','DRY Hire(Just the bar structure, the organizer supplies stocks)'),
                ('CASH BAR','Cash Bar(Guests pay for themselves)'),
                ('PREPAID BAR','Pre-paid Bar(Money is deposited or vouchers given and once they run out, the cash bar starts)'),
                ('OPEN BAR','Open bar(All drinks are pre-paid by the organizer)'),
                ('NOT SURE','I am not sure'),
            ]
# Checkbox
DRINK_TYPES=[   ('BEER OR CIDER','Beer or Cider'),
                ('WINE','Wine'),
                ('CHAMPAGNE','Champagne'),
                ('SPIRITS OR COCKTAILS','Spirits or Cocktails'),
                ('SOFT DRINKS','Soft Drinks'),
            ]

DURATION_BAR=[  ('LESS THAN 4 HOURS','Less than 4 hours'),
                ('4 - 6 hours','4 - 6 hours'),
                ('6 - 8 hours','6 - 8 hours'),
                ('8 - 10 hours','8 - 10 hours'),
                ('10 + hours','10 + hours'),
                ('MORE THAN A DAY','MORE THAN A DAY'),
            ]

INSIDE_OUTSIDE=[    ('INSIDE','Inside'),
                    ('OUTSIDE','Outside'),
                    ('NOT DECIDED','I am not decided yet'),
            ]

BUDGET_PERHEAD=[    ('BELOW 1000','BELOW KSHS. 1000/-'),
                    ('KSHS.1000 - KSHS.2000','KSHS.1000 - KSHS.2000'),
                    ('KSHS.2000 - KSHS.3000','KSHS.2000 - KSHS.3000'),
                    ('KSHS.3000 - KSHS.4000','KSHS.3000 - KSHS.4000'),
                    ('MORE THANK 4000','More than KSHS.4000'),
                    ('KSHS.1000 - KSHS.2000','MORE THAN A DAY'),
            ]

FUNFOOD_TYPES=[     ('POP CORNS','Pop Corns'),
                    ('CANDY FLOSS','Candy Floss'),
                    ('FUN FOODS','Fun Foods'),
            ]

CROCKERY_TABLEWARE=[('TABLEWARE','Tableware (e.g.Plates, Spoons & Cups)'),
                    ('VINTAGE CROCKERY HIRE','Vintage Crockery Hire'),
            ]

# Checkbox
ROAST_TYPES=[   ('DIY','DIY (Vendor will provide everything you need e.g. machine(Jiko) and Goat. Then leaves you to cook.)'),
                ('FULL SERVICE','Full Service(Vendor stays to cook. Full plated meal, including goat and sides such as potatoes or salads.)'),
                ('ACCESORIES HIRE','Vendor will provide the roast equipment you need e.g. machine(Jiko). Then you provide the goat and you cook'),
            ]

ROAST_SIDES=[   ('0','0 Side Dishes'),
                ('1','1 Side Dishes'),
                ('2','2 Side Dishes'),
                ('3','3 Side Dishes'),
                ('4','4 Side Dishes'),
                ('5 OR MORE','MORE THAN A DAY'),
            ]

ROAST_SERVICES=[('HOG ROAST','Hog Roast'),
                ('GOAT ROAST','Goat Roast'),
            ]

BUSINESS_LUNCHBUFFET=[('BUSINESS LUNCH BUFFET','Business Lunch Buffet'),
                    ('BUFFET','Buffet'),
            ]

BUFFET_TYPES=[  ('COLD FOLK','Cold fork buffet'),
                ('FINGER','Finger buffet'),
                ('HOT','Hot buffet'),
                ('MIXED','Mixed buffet'),
                ('OPEN TO SUGGESTION','Open to suggestions'),
            ]

STAFF=[ ('YES','Yes, I need Staff'),
        ('NO','No, Just drop off the food'),
        ('NOT SURE','I am not sure yet'),
    ]

# Checkboxes
COFFEE_BAR=[('BAR COUNTER','Bar Counter'),
            ('LARGE VEHICLE','Large Vehicle'),
            ('SMALL VEHICLE','Small Vehicle'),
    ]

# Checkboxes
DRINK_PREFERENCE=[  ('INSTANT COFFEE','Instant coffee'),
                    ('BARISTA COFFEE','Barista coffee'),
                    ('TEA','Tea'),
                    ('FRUIT AND HERBAL TEA','Fruit and herbal tea'),
                    ('HOT CHOCOLATE','Hot Chocolate'),
                    ('COLD DRINKS','Cold drinks'),
            ]

# Checkboxes
SNACK_TYPES=[   ('BISCUITS','Biscuits'),
                ('BROWNIES','Brownies'),
                ('CAKES','Cakes'),
                ('NO SNACKS NEEDED','No Snacks Needed'),
                ('PASTRIES','Pastries'),
                ('OTHER','Other(please specify)'),
            ]

# Checkboxes
CAKEMAKERS_CUPCAKES=[   ('CAKE MAKERS','Cake Makers'),
                        ('CUP CAKES','Cup Cakes'),
                        ('WEDDING CAKES','Wedding Cakes'),
                    ]

# Checkboxes
CATERING_SERVICES=[ ('CORPORATE EVENT CATERING','Corporate Event Catering'),
                    ('BUSINSS LUNCH CATERING','Business Lunch Catering'),
                ]

# TENTS
TENT_STRUCTURE=[('BIG TOP','Big Top'),
                ('ANY STYLE MARQUEE','Any Style Marquee'),
                ('STRETCHED MARQUEE','Stretched Marquee'),
                ('PAGODA','Pagoda'),
                ('PARTY TENTS','Party Tents'),
                ('TIPI','Tipis'),
                ('YURT','Yurts'),
                ('CAMPING TENTS','Camping Tents'),
                ('OTHER','Other(please specify)'),
            ]

SEATED_STANDING=[   ('SEATED IN ROWS','Seated in Rows'),
                    ('SEATED IN TABLES','Seated in Tables'),
                    ('SEATED BUFFET','Seated Buffet'),
                    ('STANDING','Standing'),
                    ('STANDING WITH FEW CHAIRS','Standing With Few Chairs'),
                    ('N/A','N/A'),
                    ('OTHER','Other(please specify)'),
            ]

SEATED_STANDING=[   ('GRASS','Grass'),
                    ('HARD GROUND','Hard Ground(e.g. Concrete)'),
            ]

TENT_USE=[  ('SLEEPING','Sleeping'),
            ('CHILL OUT AREA','Chilling Out Area'),
            ('KIDS AREA','Kids Area'),
            ('OTHER','Other(please specify)'),
        ]

TENT_FURNISHED=[('YES BASIC FURNISHINGS','Yes With Basic Furnishings'),
                ('YES PREMIUM FURNISHINGS','Yes With Premium Furnishings'),
                ('NO FURNISHINGS NEEDED','No Furnishings Needed'),
                ('I DO NOT KNOW','Not Made Up My Mind Yet'),
            ]

class ServiceCategoryForm(forms.ModelForm):

    service_category = forms.ChoiceField(required=True,choices=SERVICES,widget=forms.RadioSelect(), label='What do you need?')

    class Meta():
        model = Group
        fields = ('service_category',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class ServiceCategoryFS1Form(forms.ModelForm):

    service_category = forms.ChoiceField(required=True,choices=CATERING_FS1,widget=forms.RadioSelect(attrs={'class':'form-check-input','id':'exampleRadios1'}))

    class Meta():
        model = Group
        fields = ('service_category',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['service_category'].label = 'What do you need?'

class ServiceCategoryFS2Form(forms.ModelForm):

    service_category = forms.ChoiceField(required=True,choices=CATERING_FS2,widget=forms.RadioSelect(attrs={'class':'form-check-input','id':'exampleRadios1'}), label='What do you need?')

    class Meta():
        model = Group
        fields = ('service_category',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class EventTypeForm(forms.ModelForm):

    event_type = forms.ChoiceField(choices=EVENT_TYPES, widget=forms.RadioSelect(), label='What type of event is it?')
    private_public = forms.ChoiceField(choices=PRIVATE_PUBLIC, widget=forms.RadioSelect(), label='Is the event private or public')

    class Meta():
        model = Group
        fields = ('event_type','private_public')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class EventVenueForm(forms.ModelForm):

    confirmed_venue = forms.CharField(widget=forms.TextInput(), label='I have a confirmed venue')
    speculated_venue = forms.CharField(widget=forms.TextInput(), label='Still looking for a venue')

    class Meta():
        model = Group
        fields = ('confirmed_venue','speculated_venue')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class EventDateForm(forms.ModelForm):

    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','placeholder':'e.g. 31/12/2019'}), label='What date is the event?')
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='What time does the event start?')
    duration_onsite = forms.IntegerField(widget=forms.NumberInput(), label='Estimated time required onsite?')
    duration_measure = forms.ChoiceField(choices=DURATION_MEASURE, widget=forms.Select())

    class Meta():
        model = Group
        fields = ('event_date','start_time','duration_onsite','duration_measure')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class MessageToVendorForm(forms.ModelForm):

    description = forms.CharField(required=True,widget=forms.Textarea(),label='Please write this as you would an email. Include key details and sign off with your name.')

    class Meta():
        model = Group
        fields = ('description',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class GuestsExpectedForm(forms.ModelForm):

    guests_expected= forms.ChoiceField(required=True,choices=GUESTS_EXPECTED,widget=forms.RadioSelect(), label='What is the estimated number of guests you expect')

    class Meta():
        model = Group
        fields = ('guests_expected',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class AuthorsRoleForm(forms.ModelForm):

    author_role = forms.ChoiceField(required=True,choices=AUTHORS_ROLE,widget=forms.RadioSelect(), label='What is the authors role')
    current_stage = forms.ChoiceField(required=True,choices=CURRENT_STAGE,widget=forms.RadioSelect(), label='What stage of planning are you at')

    class Meta():
        model = Group
        fields = ('author_role','current_stage')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class ContactMobileForm(forms.ModelForm):

    contact_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'e.g. +254722999999 or 0722999999'}), label='Please provide your phone number so we can notify you instantly when interested suppliers send you a quote.')

    class Meta():
        model = Group
        fields = ('contact_mobile',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class VenueTypeForm(forms.ModelForm):

    venue_type = forms.ChoiceField(required=True,choices=VENUE_TYPE,widget=forms.RadioSelect(), label='What type of Venue do you have')

    class Meta():
        model = Group
        fields = ('venue_type',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class ChildrenCountForm(forms.ModelForm):

    children_count = forms.IntegerField(widget=forms.NumberInput(), label='What is the estimated number of children expected?')

    class Meta():
        model = Group
        fields = ('children_count',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class PaymentTermsForm(forms.ModelForm):

    payment_terms = forms.ChoiceField(required=True,choices=PAYMENT_TERMS,widget=forms.RadioSelect(), label='How will you pay?')

    class Meta():
        model = Group
        fields = ('payment_terms',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class ServiceLevelForm(forms.ModelForm):

    service_level = forms.ChoiceField(required=True,choices=SERVICE_LEVEL,widget=forms.RadioSelect(), label='What level of service do you expect?')

    class Meta():
        model = Group
        fields = ('service_level',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class TermsConditionsForm(forms.ModelForm):

    terms_conditions = forms.MultipleChoiceField(required=True,choices=TERMS_CONDITIONS, widget=forms.CheckboxSelectMultiple(), label='Accept Terms & Conditions')
    receive_info = forms.MultipleChoiceField(required=True,choices=RECEIVE_INFO, widget=forms.CheckboxSelectMultiple(), label='I want to receive Promotions & Information')

    class Meta():
        model = Group
        fields = ('terms_conditions','receive_info')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class StartersDesertsForm(forms.ModelForm):

    starters_deserts = forms.ChoiceField(required=True,choices=STARTERS_DESERTS,widget=forms.RadioSelect(), label='Please choose the catering type you prefer')

    class Meta():
        model = Group
        fields = ('starters_deserts',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class CateringTypesForm(forms.ModelForm):

    catering_type = forms.ChoiceField(required=True,choices=CATERING_TYPES,widget=forms.RadioSelect(), label='Please choose the catering type you prefer')

    class Meta():
        model = Group
        fields = ('catering_type',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class DietaryRequirementsForm(forms.ModelForm):

    dietary_requirements = forms.MultipleChoiceField(required=True,choices=DIETARY_REQUIREMENTS,widget=forms.CheckboxSelectMultiple(), label='Do you have any dietary requirements?')

    class Meta():
        model = Group
        fields = ('dietary_requirements',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class BuffetTypesForm(forms.ModelForm):

    buffet_types = forms.MultipleChoiceField(required=True,choices=BUFFET_TYPES,widget=forms.CheckboxSelectMultiple(), label='What type of Buffet do you prefer?')

    class Meta():
        model = Group
        fields = ('buffet_types',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
