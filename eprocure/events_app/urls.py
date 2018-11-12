from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

from events_app.forms import (
                                ServiceCategoryForm,
                                ServiceCategoryFS1Form,
                                ServiceCategoryFS2Form,
                                CateringTypesForm,
                                StartersDesertsForm,
                                DietaryRequirementsForm,
                                BuffetTypesForm,
                                VenueTypeForm,
                                GuestsExpectedForm,
                                ChildrenCountForm,
                                PaymentTermsForm,
                                ServiceLevelForm,
                                EventTypeForm,
                                EventVenueForm,
                                EventDateForm,
                                MessageToVendorForm,
                                ContactMobileForm,
                                AuthorsRoleForm,
                                TermsConditionsForm,
        )

app_name = 'events_app'

FORMS_ALL = [
        ('service_category', ServiceCategoryForm),
        ('service_category_FS1', ServiceCategoryFS1Form),
        ('service_category_FS2', ServiceCategoryFS2Form),
        ('catering_types', CateringTypesForm),
        ('starters_deserts', StartersDesertsForm),
        ('dietary_requirements', DietaryRequirementsForm),
        ('buffet_types', BuffetTypesForm),
        ('venue_type', VenueTypeForm),
        ('guests_expected', GuestsExpectedForm),
        ('children_count', ChildrenCountForm),
        ('payment_terms', PaymentTermsForm),
        ('service_level',ServiceLevelForm),
        ('event_type', EventTypeForm),
        ('event_venue', EventVenueForm),
        ('event_date', EventDateForm),
        ('message_to_vendor', MessageToVendorForm),
        ('contact_mobile', ContactMobileForm),
        ('authors_role', AuthorsRoleForm),
        ('terms_conditions', TermsConditionsForm),
    ]

FORMS_SET_1 = [
        ('service_category_FS1', ServiceCategoryFS1Form),
        ('starters_deserts', StartersDesertsForm),
        ('dietary_requirements', DietaryRequirementsForm),
        ('venue_type', VenueTypeForm),
        ('guests_expected', GuestsExpectedForm),
        ('children_count', ChildrenCountForm),
        ('payment_terms', PaymentTermsForm),
        ('service_level',ServiceLevelForm),
        ('event_type', EventTypeForm),
        ('event_venue', EventVenueForm),
        ('event_date', EventDateForm),
        ('message_to_vendor', MessageToVendorForm),
        ('contact_mobile', ContactMobileForm),
        ('authors_role', AuthorsRoleForm),
        ('terms_conditions', TermsConditionsForm),
    ]

FORMS_SET_2 = [
        ('service_category_FS2', ServiceCategoryFS2Form),
        ('buffet_types', BuffetTypesForm),
        ('starters_deserts', StartersDesertsForm),
        ('dietary_requirements', DietaryRequirementsForm),
        ('venue_type', VenueTypeForm),
        ('guests_expected', GuestsExpectedForm),
        ('children_count', ChildrenCountForm),
        ('payment_terms', PaymentTermsForm),
        ('service_level',ServiceLevelForm),
        ('event_type', EventTypeForm),
        ('event_venue', EventVenueForm),
        ('event_date', EventDateForm),
        ('message_to_vendor', MessageToVendorForm),
        ('contact_mobile', ContactMobileForm),
        ('authors_role', AuthorsRoleForm),
        ('terms_conditions', TermsConditionsForm),
    ]

urlpatterns = [
    url(r"^$", views.ListGroups.as_view(), name="all"),
    url(r"^new/$", views.CreateGroup.as_view(), name="create"),
    url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleGroup.as_view(),name="single"),
    url(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),
    url(r'^formset1/add/$',views.FORMS_SET_1_Wizard.as_view(FORMS_SET_1),name='formset1'),
    url(r'^formset2/add/$',views.FORMS_SET_2_Wizard.as_view(FORMS_SET_2),name='formset2'),

]
