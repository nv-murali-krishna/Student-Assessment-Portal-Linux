from .models import User_comments,Student_comments
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Question,Subject,Quiz,Answer,Student,TakenQuiz,StudentAnswer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User,'student'.
    list_display = ('email','username','rollnumber','gender','phone','section','year','branch','admin',)
    list_filter = ('admin','staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('User info', {'fields': ('username','rollnumber','year','section','branch','gender','phone','profile','datejoined')}),
        ('Permissions', {'fields': ('admin','staff','active','is_student')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','rollnumber','phone','gender','year','branch','profile','section','datejoined','password','password1')}
        ),
    )
    search_fields = ('email','username','rollnumber','phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Subject,SubjectAdmin)

class QuizAdmin(admin.ModelAdmin):
    list_display=['owner','name','subject','date']
admin.site.register(Quiz,QuizAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display=['text','difficulty']
admin.site.register(Question,QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display=['question','text',]
admin.site.register(Answer,AnswerAdmin)

class StudentAnswerAdmin(admin.ModelAdmin):
    list_display=['student','answer',]
admin.site.register(StudentAnswer,StudentAnswerAdmin)

class User_commentsAdmin(admin.ModelAdmin):
    list_display=['username','email','subject','message','date']
admin.site.register(User_comments,User_commentsAdmin)

class Student_commentsAdmin(admin.ModelAdmin):
    list_display=['username','rollnumber','subject','message','date']
admin.site.register(Student_comments,Student_commentsAdmin)
