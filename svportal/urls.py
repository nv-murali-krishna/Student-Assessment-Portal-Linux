"""svportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth import logout
from django.urls import path,re_path
from svapp.views import (QuizListView,StudentInterestsView,TakenQuizListView,QuizResultsView,
                        QuizChangeListView,QuizCreateView,QuizUpdateView,QuizDeleteView,QuizTeacherResultsView,QuestionDeleteView,
                        AddQuestionsView)
from svapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^adm/$', views.adm),
    url(r'^student/$', views.student),
    url(r'^teacher/$', views.teacher),
    url(r'^about/',views.about),
    url(r'^treg/',views.teacher_reg),
    url(r'^tlog/',views.teacher_log),
    url(r'^sreg/',views.student_reg),
    url(r'^slog/', views.student_log),
    url(r'^log/', views.login),
    url(r'^logout/$',views.logout_view),
    url(r'^adds/',views.add_student),
    url(r'^addt/',views.add_teacher),
    url(r'^comment/',views.User_comment_view),
    url(r'^com/',views.Student_comment_view),
    url(r'^comments/',views.comments),
    url(r'^show/', views.show),
    url(r'^sdetails/',views.sdetails),
    url(r'^tdetails/',views.tdetails),
    url(r'^subdetails/', views.subject_details),
    url(r'^subdelete/(?P<id>\d+)/', views.subject_delete),
    url(r'^subupdate/(?P<id>\d+)/', views.subject_update),
    url(r'^dels/(?P<id>\d+)/', views.delete_s),
    url(r'^delt/(?P<id>\d+)/', views.delete_t),
    url(r'^delc/(?P<id>\d+)/', views.delete_c),
    url(r'^delsc/(?P<id>\d+)/', views.delete_sc),
    url(r'^ups/(?P<id>\d+)/',views.StudentUpdate),
    url(r'^update_s/(?P<id>\d+)/',views.S_Update),
    url(r'^update_t/(?P<id>\d+)/',views.T_Update),
    url(r'^upt/(?P<id>\d+)/',views.TeacherUpdate),
    url(r'^search_s/',views.Search_Student),
    url(r'^search_t/',views.Search_Teacher),
    url(r'^search_a/',views.Search_Assessments),
    url(r'^search_q/',views.Search_Quiz),
    url(r'^easy/',views.easy),
    url(r'^medium/',views.medium),
    url(r'^hard/',views.hard),
    url(r'^write/', views.write),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^addprofile/(?P<id>\d+)/',views.ProfileUpdate, name='addprofile'),
    url(r'^quiz_list/',QuizListView.as_view(), name='quiz_list'),
    url(r'^interests/',StudentInterestsView.as_view(), name='student_interests'),
    url(r'^taken/', TakenQuizListView.as_view(), name='taken_quiz_list'),
    url(r'^quiztake/(?P<pk>\d+)/$', views.take_quiz, name='take_quiz'),
    url(r'^quiz/(?P<pk>\d+)/studentresults/$', QuizResultsView.as_view(), name='student_quiz_results'),

    url(r'^quiz_change_list/', QuizChangeListView.as_view(), name='quiz_change_list'),
    url(r'^quiz/add/', QuizCreateView.as_view(), name='quiz_add'),
    url(r'^quiz/(?P<pk>\d+)/$', QuizUpdateView.as_view(), name='quiz_change'),
    url(r'^quiz/(?P<pk>\d+)/delete/$', QuizDeleteView.as_view(), name='quiz_delete'),
    url(r'^quiz/(?P<pk>\d+)/results/$', QuizTeacherResultsView.as_view(), name='quiz_results'),
    url(r'^quiz/(?P<pk>\d+)/question/add/$', views.question_add, name='question_add'),
    url(r'^quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/$', views.question_change, name='question_change'),
    url(r'^quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/delete/$', QuestionDeleteView.as_view(), name='question_delete'),

    url(r'^addquestions/', AddQuestionsView.as_view(), name='addquestions'),
    url(r'^addsubjects/',views.subject_add, name='addsubjects'),
    url(r'^qdelete/(?P<idd>.*)/',views.question_delete, name='q_delete'),

] +static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
