from django import forms
from .models import order


class OrderForm(forms.ModelForm):
    # give it a couple meta options telling django which model it'll
    # be associated with and which fields we want to render.we're not
    # rendering any fields in the form which will be automatically calculated.
    # because no one will ever be filling that information out.
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county')

    # call the default init method to set the form up as it would be by default
    def __init__(self, *args, **kwargs):
        # Add placeholders and classes, remove auto-generated
        # labels and set autofocus on first field

        super().__init__(*args, **kwargs)
        # a dictionary of placeholders which will show up in form fields rather
        # than having clunky looking labels and empty text boxes in template
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # setting the autofocus attribute on the full name field to true
        # so cursor will start in the full name field when user loads the page.
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # we iterate through the forms fields adding a * to the placeholder
        # if it's a required field on the model.
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # Setting placeholder attrib to their values in dictionary above
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adding a CSS class we'll use later.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # removing the form fields labels ince we won't need them given
            # the placeholders are now set.
            self.fields[field].label = False
