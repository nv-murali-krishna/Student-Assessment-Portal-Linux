# Create your models here.
from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.html import escape, mark_safe
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email,rollnumber=None,phone=None,username=None,profile=None,branch=None,gender=None, year=None, section=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('User must have an Password')
        user = self.model(
            email=self.normalize_email(email),

        )
        user.username=username
        user.year=year
        user.section=section
        user.gender=gender
        user.branch=branch
        user.phone=phone
        user.profile=profile
        user.rollnumber=rollnumber
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,

        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_studentuser(self, email,password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,

        )
        user.is_student = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.is_student = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    username=models.CharField(
    max_length=30,
    null=True,blank=True
     )
    g_choices=(
    ('Male','Male'),
    ('Female','Female'),
    ('Others','Others'),
    )
    gender=models.CharField(max_length=10,null=True,blank=True,choices=g_choices)
    y_choices=(('1st','1st'),
    ('2nd','2nd'),
    ('3rd','3rd'),
    ('4th','4th'),)
    year=models.CharField(max_length=10,null=True,blank=True,choices=y_choices)
    s_choices=(
    ('Section A','Section A'),
    ('Section B','Section B'),
    ('Section C','Section C'),
    ('Section D','Section D'),)
    section=models.CharField(max_length=10,null=True,blank=True,choices=s_choices)
    b_choices=(
    ('M.C.A','M.C.A'),
    ('M.B.A','M.B.A'),
    ('E.C.E','E.C.E'),
    ('E.E.E','E.E.E'),
    ('C.S.E','C.S.E'),
    ('IT','IT'      ),
    ('CIVIL','CIVIL'),
    )
    branch=models.CharField(max_length=10,null=True,blank=True,choices=b_choices)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="Phone number must be entered in the define format")
    phone=models.CharField(validators=[phone_regex], max_length=10,unique=True,null=True,blank=True)
    rollnumber=models.CharField(max_length=10,null=True,blank=True,unique=True)
    profile = models.ImageField(upload_to='', max_length=255,null=True,blank=True)
    is_student=models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False)
    datejoined = models.DateTimeField(default=timezone.now)
     # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects=UserManager()


    def get_username(self):

        return self.email

    def get_rollnumber(self):

        return self.email

    def get_phone(self):

        return self.email

    def get_branch(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
            # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff


    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Subject(models.Model):
    name = models.CharField(max_length=50)
    c_choices=(
        ('#007bff','#007bff'),
        ('#EC407A','#EC407A'),
        ('#FF5733','#FF5733'),
        ('#2ECC71','#2ECC71'),
        ('#7D3C98','#7D3C98'),
        ('#1B4F72','#1B4F72'),
        ('#F7DC6','#F7DC6'),
    )
    color = models.CharField(max_length=100, choices=c_choices)

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    d_choices=(
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Hard','Hard'),
    )
    difficulty = models.CharField(max_length=10,blank=False,choices=d_choices,default='Easy')
    text = models.TextField('Question', max_length=3000)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    # User reputation score.
    score = models.IntegerField(default=0)

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField()
    percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')


class User_comments(models.Model):
    username=models.CharField(max_length=225)
    email=models.EmailField(max_length=225,unique=True)
    subject = models.CharField(max_length=3000)
    message=models.TextField(max_length=3000)
    date= models.DateTimeField(default=timezone.now)

class Student_comments(models.Model):
    username=models.CharField(max_length=225)
    rollnumber=models.CharField(max_length=10,unique=True)
    subject = models.CharField(max_length=3000)
    message=models.TextField(max_length=3000)
    date= models.DateTimeField(default=timezone.now)
