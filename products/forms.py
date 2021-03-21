from django import forms
from .models import Product, Category


# new class, ProductForm which will extend the built in forms.model
# form and have an inner metaclass that defines the model and the
# fields we want to include.
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # override the init method to make a couple changes to the fields.
        # We'll want the categories to show up in the form using their
        # friendly name,get all the categories and create a list of tuples
        # of the friendly names associated with their category ids.
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # update the category field on the form to use those for choices
        # instead of using the id.The effect of this will be seen in the
        # select box that gets generated in the form instead of seeing the
        # category ID or the name field we'll see the friendly name.
        self.fields['category'].choices = friendly_names
        # iterate through the rest of these fields and set some classes on
        # them to make them match the theme of the rest of our store
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'