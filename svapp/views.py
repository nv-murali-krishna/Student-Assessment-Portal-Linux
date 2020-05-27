from django.shortcuts import render,redirect
from .forms import User_commentsForm,Student_commentsForm
from .models import User,User_comments,Student_comments
from django.contrib.auth import get_user_model,logout
from django.views.generic import CreateView,FormView
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,get_user_model
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.utils.http import is_safe_url
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from .forms import StudentRegisterForm,TeacherRegisterForm,UserProfileForm,StudentUpdateForm,TeacherUpdateForm
from django.shortcuts import render
from .models import Question,Subject,Quiz,Answer,Student,TakenQuiz,StudentAnswer
from django.shortcuts import redirect, render
#<---------------------teacher-------------------------->
from django.views.generic import TemplateView
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from .forms import BaseAnswerInlineFormSet, QuestionForm,SubjectForm
from .models import Answer, Question, Quiz,Subject
#<---------------------student--------------------------->
from django.db import transaction
from django.db.models import Count, Sum
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from .forms import StudentInterestsForm, TakeQuizForm
from .models import Quiz, Student, TakenQuiz, Question,User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django import template
register = template.Library()
user_login_required = user_passes_test(lambda user: user.is_admin, login_url='/')

def admin_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

def index(request):
    return render(request, "svapp/index.html")

@login_required(login_url="/log")
@admin_user_required
def adm(request):
    return render(request, "svapp/adm.html")

@login_required(login_url="/tlog")
@staff_member_required(login_url="/")
def teacher(request):
    return render(request, "svapp/teacher.html")

@login_required(login_url="/slog")
def student(request):
    return render(request, "svapp/student.html")

def about(request):
    return render(request, "sapp/about.html")

@admin_user_required
def show(request):
    return render(request, "sapp/show.html")

@login_required(login_url="/slog")
def write(request):
    return render(request, "sapp/write.html")

@admin_user_required
def easy(request):
    questions_list=Question.objects.filter(difficulty__exact='Easy')
    return render(request,'sapp/easy.html',{'questions_list':questions_list})

@admin_user_required
def medium(request):
    questions_list=Question.objects.filter(difficulty__exact='Medium')
    return render(request,'sapp/medium.html',{'questions_list':questions_list})

@admin_user_required
def hard(request):
    questions_list=Question.objects.filter(difficulty__exact='Hard')
    return render(request,'sapp/hard.html',{'questions_list':questions_list})

@admin_user_required
def sdetails(request):
    students_list=User.objects.filter(staff__exact='False').order_by('rollnumber')
    students=User.objects.filter(staff__exact='False').count()
    return render(request, 'sapp/sdetails.html',{'students_list':students_list,'students':students})

@admin_user_required
def tdetails(request):
    teachers_list=User.objects.filter(staff__exact='True')
    teachers=User.objects.filter(staff__exact='True').count()
    return render(request, 'sapp/tdetails.html',{'teachers_list':teachers_list,'teachers':teachers})

@admin_user_required
def delete_s(request,id):
    student=User.objects.get(id=id)
    student.delete()
    return redirect('/sdetails')

@admin_user_required
def delete_t(request,id):
    teacher=User.objects.get(id=id)
    teacher.delete()
    return redirect('/tdetails')

@admin_user_required
def delete_c(request,id):
    comment=User_comments.objects.get(id=id)
    comment.delete()
    return redirect('/comments')

@admin_user_required
def delete_sc(request,id):
    comment=Student_comments.objects.get(id=id)
    comment.delete()
    return redirect('/comments')

def S_Update(request,id):
    User=get_user_model()
    user=get_object_or_404(User,id=id)
    form=StudentUpdateForm(instance=user)
    if request.method =='POST':
        form=StudentUpdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
        return redirect('/sdetails')
    return render(request,'sapp/update_student.html',{'form':form})

@admin_user_required
def T_Update(request,id):
    User=get_user_model()
    user=get_object_or_404(User,id=id)
    form=TeacherUpdateForm(instance=user)
    if request.method =='POST':
        form=TeacherUpdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('/tdetails')

    return render(request,'sapp/update_t.html',{'form':form})

def StudentUpdate(request,id):
    User=get_user_model()
    user=get_object_or_404(User,id=id)
    form=StudentUpdateForm(instance=user)
    if request.method =='POST':
        form=StudentUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('/taken')
    return render(request,'sapp/update_s.html',{'form':form})

@login_required(login_url="/tlog")
@staff_member_required(login_url="/")
def TeacherUpdate(request,id):
    User=get_user_model()
    user=get_object_or_404(User,id=id)
    form=TeacherUpdateForm(instance=user)
    if request.method =='POST':
        form=TeacherUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/addquestions')

    return render(request,'sapp/update_t.html',{'form':form})

def ProfileUpdate(request,id):
    User=get_user_model()
    user=get_object_or_404(User,id=id)
    file_data=request.FILES or None
    form = UserProfileForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,file_data,instance=request.user)
        if form.is_valid():
            profile=request.POST.get('profile')
            form.save()
            messages.success(request, 'Your Profile image Was updated successfully.')
            if user.is_staff == True:
                return redirect('/addquestions')
            else:
                return redirect('/taken')

    return render(request, 'sapp/profile_pic.html', {'form': form})

def Search_Student(request):
    if request.method=='POST':
        srch = request.POST ['srh']
        if srch:
            match = User.objects.filter(Q(username__icontains=srch)|Q(rollnumber__iendswith=srch)|Q(email__icontains=srch))
            if match:
                return render(request,'sapp/sdetails.html',{'sr':match})
            else:
                messages.error(request,'Sorry no results found')
        else:
            return HttpResponseRedirect('/sdetails')
    return render(request,'sapp/sdetails.html')

def Search_Teacher(request):
    if request.method=='POST':
        srch = request.POST ['srh']
        if srch:
            match = User.objects.filter(Q(username__icontains=srch)|Q(phone__iendswith=srch)|Q(email__icontains=srch))
            if match:
                return render(request,'sapp/tdetails.html',{'sr':match})
            else:
                messages.error(request,'Sorry no results found')
        else:
            return HttpResponseRedirect('/tdetails')
    return render(request,'sapp/tdetails.html',{'match':match})

def Search_Assessments(request):
    if request.method=='POST':
        srch = request.POST ['srh']
        if srch:
            match = Quiz.objects.filter(Q(name__icontains=srch))
            if match:
                return render(request,'teachers/add questions.html',{'sr':match})
            else:
                messages.error(request,'Sorry no results found')
        else:
            return HttpResponseRedirect('/addquestions')
    return render(request,'teachers/add questions.html')

def Search_Quiz(request):
    if request.method=='POST':
        srch = request.POST ['srh']
        if srch:
            match = Quiz.objects.filter(Q(name__icontains=srch))
            if match:
                return render(request,'students/quiz_list.html',{'sr':match})
            else:
                messages.error(request,'Sorry no results found')
        else:
            return HttpResponseRedirect('/quiz_list')
    return render(request,'students/quiz_list.html')

User = get_user_model()
def teacher_reg(request):
    form=TeacherRegisterForm()
    if request.method =='POST':
        form=TeacherRegisterForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            email=request.POST.get('email')
            branch=request.POST.get('branch')
            gender=request.POST.get('gender')
            phone=request.POST.get('phone')
            password=request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request,'!That username is already taken.')
                return redirect('teacher_reg.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'!That email is already taken.')
                return redirect('teacher_reg.html')
            elif User.objects.filter(phone=phone).exists():
                messages.error(request,'!That phone is already taken.')
                return redirect('teacher_reg.html')
            elif password < str(8):
                messages.error(request,' Should Use @#$%&*,123,abc Your password must contain at least 8 characters.')
                return redirect('teacher_reg.html')
            else:
                form.save()
                return render(request,'sapp/teacher_log.html')
        else:
            messages.error(request,'!Your credentials are invalid or or Both Passwords or notequal')
            return redirect('teacher_reg.html')

    else:
        return render(request,'sapp/teacher_reg.html',{'form':form})


def teacher_log(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        UserModel = get_user_model()
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_staff == True:
                auth.login(request,user)
                user_data = User.objects.get(email=email)
                return redirect('/teacher')

        else:
            messages.error(request,'! Invalid Uer Id/Password, plz try again.')
            return redirect('teacher_log.html')
    else:
        return render(request,'sapp/teacher_log.html')


User = get_user_model()
def student_reg(request):
    form=StudentRegisterForm()
    if request.method =='POST':
        form=StudentRegisterForm(request.POST)
        if form.is_valid() :
            username=request.POST.get('username')
            email=request.POST.get('email')
            rollnumber=request.POST.get('rollnumber')
            branch=request.POST.get('branch')
            year=request.POST.get('year')
            phone=request.POST.get('phone')
            section=request.POST.get('section')
            gender=request.POST.get('gender')
            password=request.POST.get('password')
            if User.objects.filter(rollnumber=rollnumber).exists():
                messages.error(request,'!That rollnumber is already taken.' )
                return redirect('student_reg.html')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'!That studentname is already taken.')
                return redirect('student_reg.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'!That email is already taken.')
                return redirect('student_reg.html')
            elif User.objects.filter(phone=phone).exists():
                messages.error(request,'!That phone is already taken.')
                return redirect('student_reg.html')
            elif password < str(8):
                messages.error(request,'Should Use @#$%&*,123,abc Your password must contain at least 8 characters.')
                return redirect('student_reg.html')
            else:
                form.save()
                return redirect('/slog')
        else:
            messages.error(request,'!Your credentials are invalid or Both Passwords or notequal')
            return redirect('student_reg.html')

    else:
        return render(request,'sapp/student_reg.html',{'form':form})


def student_log(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        User = get_user_model()
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_staff == False:
                auth.login(request,user)
                user_data = User.objects.get(email=email)
                return redirect("/student")

        else:
            messages.error(request,'! Invalid Uer Id/Password. plz try again')
            return redirect('student_log.html')
    else:
        return render(request,'sapp/student_log.html')

User = get_user_model()
def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        User = get_user_model()
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            if user.admin == True:
                auth.login(request,user)
                user_data = User.objects.get(email=email)
                return redirect("/adm")
            elif user is None:
                messages.error(request,'! Invalid User id/Password, plz try again.')
                return redirect('login.html')
        else:
            messages.error(request,'! Invalid User id/Password, plz try again.')
            return redirect('login.html')
    else:
        return render(request,'sapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


User=get_user_model()
def add_student(request):
    form=StudentRegisterForm()
    if request.method =='POST':
        form=StudentRegisterForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            email=request.POST.get('email')
            rollnumber=request.POST.get('rollnumber')
            branch=request.POST.get('branch')
            year=request.POST.get('year')
            phone=request.POST.get('phone')
            section=request.POST.get('section')
            gender=request.POST.get('gender')
            profile=request.POST.get('profile')
            password=request.POST.get('password')
            if User.objects.filter(rollnumber=rollnumber).exists():
                messages.error(request,'!That rollnumber is already taken.' )
                return redirect('adds.html')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'!That studentname is already taken.')
                return redirect('adds.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'!That email is already taken.')
                return redirect('adds.html')
            else:
                form.save()
                messages.success(request,"Student was added Successfully")
                return redirect('/sdetails')

        else:
            messages.error(request,'!Your credentials are invalid. Password should min 8 letters.')
            return redirect('adds.html')
    return render(request, 'sapp/adds.html',{'form':form})


User=get_user_model()
def add_teacher(request):
    form=TeacherRegisterForm()
    if request.method =='POST':
        form=TeacherRegisterForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            email=request.POST.get('email')
            branch=request.POST.get('branch')
            gender=request.POST.get('gender')
            phone=request.POST.get('phone')
            profile=request.POST.get('profile')
            password=request.POST.get('password')
            if User.objects.filter(email=email).exists():
                messages.error(request,'!That email is already taken.')
                return redirect('addt.html')
            elif User.objects.filter(phone=phone).exists():
                messages.error(request,'!That phone is already taken.')
                return redirect('addt.html')
            else:
                form.save()
                messages.success(request,"Student was added Successfully")
                return redirect('/tdetails')


        else:
            messages.error(request,'!Your credentials are invalid. Password should min 8 letters.')
            return redirect('addt.html')
    return render(request, 'sapp/addt.html',{'form':form})



@admin_user_required
def comments(request):
    student_list=Student_comments.objects.all()
    comment_list=User_comments.objects.all()
    return render(request,'sapp/comments.html',{'comment_list':comment_list, 'student_list':student_list})

@staff_member_required(login_url="/")
def User_comment_view(request):
    form=User_commentsForm()
    if request.method == 'POST':
        form=User_commentsForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            email=request.POST.get('email')
            subject=request.POST.get('subject')
            message=request.POST.get('message')
            User_comments.username=username
            User_comments.email=email
            User_comments.subject=subject
            User_comments.message=message
            form.save()
            messages.success(request,'Your resposnece was saved successfully')
        else:
            messages.error(request,'plz try again..there is a some problem')
    return render(request,'sapp/comment.html',{'form':form})

def Student_comment_view(request):
    form=Student_commentsForm()
    if request.method == 'POST':
        form=Student_commentsForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            rollnumber=request.POST.get('rollnumber')
            subject=request.POST.get('subject')
            message=request.POST.get('message')
            Student_comments.username=username
            Student_comments.rollnumber=rollnumber
            Student_comments.subject=subject
            Student_comments.message=message
            form.save()
            messages.success(request,'Your resposnece was saved successfully')
        else:
            messages.error(request,'plz try again..there is a some problem')
    return render(request,'sapp/Student_comments.html',{'form':form})

class QuizChangeListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'teachers/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset

class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'subject', )
    template_name = 'teachers/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The Assessment was created with success! Go ahead and add some questions now.')
        # return redirect('quiz_change', quiz.pk)
        return redirect('addquestions')

class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', )
    context_object_name = 'quiz'
    template_name = 'teachers/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('quiz_change', kwargs={'pk': self.object.pk})

class AddQuestionsView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'teachers/add questions.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset

class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'teachers/quiz_delete_confirm.html'
    success_url = reverse_lazy('addquestions')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


class QuizTeacherResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'teachers/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-percentage')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            # return redirect('question_change', quiz.pk, question.pk)
            return redirect('question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'teachers/question_add_form.html', {'quiz': quiz, 'form': form})

def subject_add(request):
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            name=request.POST.get('name')
            color=request.POST.get('color')
            form.save()
            messages.success(request, 'You may now add Assessments and questions.')
            # return redirect('question_change', quiz.pk, question.pk)
            return redirect('/quiz/add')
        else:
            messages.error(request, 'You must should add your subjets.')

    return render(request, 'teachers/add subjects.html', {'form': form})

def subject_details(request):
    subject_list=Subject.objects.all()
    return render(request, 'teachers/subject_details.html',{'subject_list':subject_list})

def subject_update(request, id):
    subject=Subject.objects.get(id=id)
    form = SubjectForm(instance=subject)
    if request.method =='POST':
        form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            name=request.POST.get('name')
            color=request.POST.get('color')
            form.save()
            return redirect('/addquestions')

    return render(request,'teachers/subject_update.html',{'form':form})

def subject_delete(request, id):
    subject=Subject.objects.get(id=id)
    subject.delete()
    return redirect('/subdetails')

def question_delete(request, idd):
    question=Question.objects.filter(id=idd)
    question.delete()
    return redirect('/show')

def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=5,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'teachers/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz_change', kwargs={'pk': question.quiz_id})


class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'students/interests_form.html'
    success_url = reverse_lazy('quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Subjects updated with success!')
        return super().form_valid(form)
        return HttpResponseRedirect('/quiz_list')


class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


class QuizResultsView(View):
    template_name = 'students/quiz_result.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(id = kwargs['pk'])
        taken_quiz = TakenQuiz.objects.filter(student = request.user.student, quiz = quiz)
        if not taken_quiz:
            """
            Don't show the result if the user didn't attempted the quiz
            """
            return render(request, '404.html')
        questions = Question.objects.filter(quiz =quiz)

        # questions = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'questions':questions,
            'quiz':quiz, 'percentage': taken_quiz[0].percentage})


class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    percentage = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=correct_answers, percentage= percentage)
                    student.score = TakenQuiz.objects.filter(student=student).aggregate(Sum('score'))['score__sum']
                    student.save()
                    if percentage < 35.0:
                        messages.warning(request, 'Better luck next time! Your score for the Assessment %s was %s.' % (quiz.name, percentage))
                    elif percentage > 60.0:
                        messages.success(request, 'Congratulations! You completed the Assessment %s with success! You scored %s points.' % (quiz.name, percentage))
                    else:
                        messages.info(request, 'You completed the Assessment %s with success! You scored %s points.' % (quiz.name, percentage))
                    return redirect('quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress,
        'answered_questions': total_questions - total_unanswered_questions,
        'total_questions': total_questions
    })
