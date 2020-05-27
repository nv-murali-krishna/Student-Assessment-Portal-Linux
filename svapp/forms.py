from django import  forms
from .models import User_comments,Student_comments
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction
from django.contrib.auth import get_user_model
from django.forms.utils import ValidationError
from .models import (Answer, Question, Student, StudentAnswer, Subject)
from .models import User
class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username','phone','rollnumber','gender','year','branch','section',)

    def clean_password1(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
class  StudentRegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username','rollnumber','gender','phone','year','branch','section',)

    def clean_password1(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords don't match")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    @transaction.atomic
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(StudentRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.active=True
        user.is_student=True
        user.staff=False
        if commit:
            user.save()
            student = Student.objects.create(user=user)
        return user

class TeacherRegisterForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
       model = User
       fields = ('email','username','branch','gender','phone',)

    def clean_password1(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords don't match")
        return password

    def clean_email(self):
       email = self.cleaned_data.get('email')
       qs = User.objects.filter(email=email)
       if qs.exists():
           raise forms.ValidationError("email is taken")
       return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TeacherRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.active=True
        user.staff=True
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ('profile',)


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ('email','username','branch','gender','phone',)

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username','rollnumber','gender','phone','year','branch','section',)

class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model= Subject
        fields=('name','color',)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'difficulty')


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class User_commentsForm(forms.ModelForm):
    class Meta:
        model=User_comments
        fields=('username','email','subject','message',)

    def clean_User_comments(self, *args, **kwargs):
        #run the standard clean method first
        inputdata = self.cleaned_data.get('User_commnets')
        print('validating form')
        return inputdata

class Student_commentsForm(forms.ModelForm):
    class Meta:
        model=Student_comments
        fields=('username','rollnumber','subject','message',)

    def clean_Student_comments(self, *args, **kwargs):
        #run the standard clean method first
        inputdata = self.cleaned_data.get('Student_commnets')
        print('validating form')
        return inputdata
