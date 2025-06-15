

# Register your models here.
from django.contrib import admin
from .models import Post,Comment

from .models import Category
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
from .models import SiteSettings

admin.site.register(SiteSettings)


from django.contrib import admin
from .models import SiteSettings  # Import the model


from django.contrib import admin
from .models import QuizCategory, QuizQuestion

admin.site.register(QuizCategory)
admin.site.register(QuizQuestion)

# blog/admin.py

from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    ist_display = ('question', 'correct_option')
    search_fields = ('question',)

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)


