from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field


class UserSignUpForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('name', 'username')

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, 
                        widget=forms.TextInput(attrs={'placeholder': 'Search your query here..'}))
    page = forms.IntegerField(initial=1)
    pagesize = forms.IntegerField(required=False, max_value=100)
    fromdate = forms.CharField(max_length=10, required=False)
    todate = forms.CharField(max_length=10, required=False)
    order = forms.ChoiceField(choices=(('Desc', 'Desc'), ('Asc', 'Asc')))
    min_date = forms.CharField(max_length=10, required=False)
    max_date = forms.CharField(max_length=10, required=False)
    sort = forms.ChoiceField(choices=(('relevance', 'relevance'),
                                      ('activity', 'activity'),
                                      ('votes', 'votes'),
                                      ('creation', 'creation')), required=False)
    
    accepted = forms.ChoiceField(choices=(('', ''), ('True', 'True'), ('False', 'False')), required=False)
    answers = forms.IntegerField(required=False)
    body = forms.CharField(max_length=10, required=False)
    closed = forms.ChoiceField(choices=(('', ''), ('True', 'True'), ('False', 'False')), required=False)
    migrated = forms.ChoiceField(choices=(('', ''), ('True', 'True'), ('False', 'False')), required=False)
    notice = forms.ChoiceField(choices=(('', ''), ('True', 'True'), ('False', 'False')), required=False)
    nottagged = forms.CharField(max_length=10, required=False)
    tagged = forms.CharField(max_length=10, required=False)
    title = forms.CharField(max_length=10, required=False)
    user = forms.CharField(max_length=10, required=False)
    url = forms.URLField(max_length=250, required=False)
    views = forms.IntegerField(required=False)
    wiki = forms.ChoiceField(choices=(('', ''), ('True', 'True'), ('False', 'False')), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = False
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(   
                Column('query', css_class='form-group col-10 mb-0'),
                Column('page', css_class='form-group col-1 mb-0'),
                Column('pagesize', css_class='form-group col-1 mb-0'),
            ),
            Row(
                Column('fromdate', css_class='form-group col-3 mb-0'),
                Column('todate', css_class='form-group col-3 mb-0'),
                Column('min_date', css_class='form-group col-3 mb-0'),
                Column('max_date', css_class='form-group col-3 mb-0'),
            ),
            Row(
                Column('order', css_class='form-group col-4 mb-0'),
                Column('sort', css_class='form-group col-4 mb-0'),
                Column('accepted', css_class='form-group col-4 mb-0'),
            ),
            Row(
                Column('answers', css_class='form-group col-6 mb-0'),
                Column('body', css_class='form-group col-6 mb-0'),
            ),
            Row(
                Column('closed', css_class='form-group col-4 mb-0'),
                Column('migrated', css_class='form-group col-4 mb-0'),
                Column('notice', css_class='form-group col-4 mb-0'),
            ),
            Row(
                Column('title', css_class='form-group col-4 mb-0'),
                Column('user', css_class='form-group col-4 mb-0'),
                Column('url', css_class='form-group col-4 mb-0'),
            ),
            Row(
                Column('nottagged', css_class='form-group col-3 mb-0'),
                Column('tagged', css_class='form-group col-3 mb-0'),
                Column('views', css_class='form-group col-3 mb-0'),
                Column('wiki', css_class='form-group col-3 mb-0'),
            ),
            Submit('search_query', 'Submit' , css_class="btn-success")
        )