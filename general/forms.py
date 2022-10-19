from django import forms
from general.models import Employee,MsgSent,Letters,Resources
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



#overiding form date input from a textfield
class DateInput(forms.DateInput):
    input_type = 'date'



class MsgSentForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(MsgSentForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = MsgSent
        fields = ['subject','message', 'sent_to']
        help_texts = {
            'sent_to': "Select Recipient or leave blank to send to all"
        }




class empID(forms.Form):
    staffid = forms.CharField(max_length=15, label='Description')




class EmployeeForm(forms.ModelForm):#changename later
    # staff = forms.CharField(max_length=10, label='Username')
    def __int__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['staff'].label = 'Username'


    class Meta:
        model = Employee
        fields = '__all__'
        widgets = { 
            'dob': DateInput(),
            'date_employed': DateInput(),

        }
        def clean(self):
            cleaned_data = super(EmployeeForm, self).clean()
            return cleaned_data




class EmployeeUpdateForm(forms.ModelForm):#changename later
    # staff = forms.CharField(max_length=10, label='Username')
    def __int__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['staff'].label = 'Username'


    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ('username',)
        widgets = { 
            'dob': DateInput(),
            'date_employed': DateInput(),

        }

        def clean(self):
            cleaned_data = super(EmployeeUpdateForm, self).clean()
            return cleaned_data        








class LettersForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(LettersForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Letters
        fields = '__all__'
        exclude = ('date',)
        help_texts = {
            'start_from': "Leave blank if action is not time bound",
            'end': "Leave blank if action is not time bound"}

        widgets = { 
            'start_from': DateInput(),
            'end': DateInput()
        }




class RscForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(RscForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Resources
        fields = '__all__'
        help_texts = {
            'staff': "If Appraisal or Accreditation, choose staff",
            'end': "Leave blank if action is not time bound"}