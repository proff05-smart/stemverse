from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Post, Comment, Category, SiteSettings
from .forms import CommentForm, ContactForm, PostForm


def home(request):
    posts = Post.objects.all().order_by('-created')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    site_settings = SiteSettings.objects.first() 
    categories = Category.objects.all()

    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'site_settings': site_settings, 

    })


def post_detail(request, post_id, post_slug):
    post = get_object_or_404(Post, pk=post_id, slug=post_slug)
    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, "Your comment was posted successfully.")
                comments = post.comments.all()  # Refresh comment list
        else:
            messages.warning(request, "You need to be logged in to comment.")
            return render(request, 'blog/post_detail.html', {'post': post})
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'new_comment': new_comment,
    })


from django.shortcuts import render, get_object_or_404
from .models import Category, Post  # make sure you import both

from django.shortcuts import render, get_object_or_404
from .models import Category, Post

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category)
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
    })




@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(post.get_absolute_url())


def contact_view(request):
    form = ContactForm(request.POST or None)
    settings = SiteSettings.objects.first()

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'blog/contact.html', {
        'form': form,
        'settings': settings,
    })


def user_list(request):
    users = User.objects.all()
    return render(request, 'blog/user_list.html', {'users': users})


def search_posts(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results,
    })


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user
            updated_post.save()
            return redirect(reverse('post-detail', kwargs={
                'post_id': updated_post.pk,
                'post_slug': updated_post.slug,
            }))
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {
        'form': form,
        'post': post,
    })


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

from django.shortcuts import render
from .models import Post

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(title__icontains=query) if query else Post.objects.none()
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query) if query else []
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})



from django.shortcuts import render

def calendar_view(request):
    return render(request, 'blog/calendar.html')

def support_view(request):
    return render(request, 'blog/support.html')


from django.shortcuts import render
from .models import QuizCategory, QuizQuestion
import random

from django.shortcuts import get_object_or_404, render
import random
def quiz_home(request):
    categories = QuizCategory.objects.all()
    return render(request, 'blog/quiz_home.html', {'categories': categories})

def random_quiz(request, category_id=None):
    if category_id:
        questions = QuizQuestion.objects.filter(category_id=category_id)
    else:
        questions = QuizQuestion.objects.all()
    
    questions = list(questions)
    random.shuffle(questions)
    return render(request, 'blog/quiz.html', {'questions': questions[:5]})  # 5 questions per quiz

# blog/views.py

from django.shortcuts import render, get_object_or_404
from .models import Quiz

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                answer = question.answers.get(pk=selected)
                if answer.is_correct:
                    score += 1
        return render(request, 'blog/quiz_result.html', {'quiz': quiz, 'score': score, 'total': total})

    return render(request, 'blog/take_quiz.html', {'quiz': quiz, 'questions': questions})

# blog/views.py

import random
from django.shortcuts import render
from .models import QuizQuestion

def quiz_view(request):
    questions = list(QuizQuestion.objects.all())
    random.shuffle(questions)
    selected_questions = questions[:5]  # Change number as needed

    if request.method == 'POST':
        score = 0
        total = len(selected_questions)
        for q in selected_questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_option:
                score += 1
        return render(request, 'blog/quiz_result.html', {
            'score': score,
            'total': total,
        })

    return render(request, 'blog/quiz.html', {'questions': selected_questions})

from django.shortcuts import render
from .models import QuizQuestion
import random

import random
from django.shortcuts import render
from .models import QuizQuestion

from django.shortcuts import render
from .models import QuizQuestion
import random
from django.shortcuts import render
import random
from .models import QuizQuestion
import random
from django.shortcuts import render
from .models import QuizQuestion, QuizCategory  # If you're using categories

def quiz_home(request):
    if request.method == 'POST':
        question_ids = request.POST.getlist('question_ids')
        questions = QuizQuestion.objects.filter(id__in=question_ids)

        score = 0
        total = len(questions)
        results = []

        for question in questions:
            user_answer = request.POST.get(str(question.id), "").strip()

            options = {
                'A': question.option_a.strip(),
                'B': question.option_b.strip(),
                'C': question.option_c.strip(),
                'D': question.option_d.strip()
            }

            selected_label = None
            for label, option in options.items():
                if user_answer == option:
                    selected_label = label
                    break

            is_correct = selected_label == question.correct_option
            if is_correct:
                score += 1

            results.append({
                'question': question.question,
                'user_answer': user_answer,
                'correct_answer': options[question.correct_option],
                'is_correct': is_correct
            })

        percentage = int((score / total) * 100) if total > 0 else 0
        passed = score >= (total / 2)

        return render(request, 'quiz/quiz_result.html', {
            'score': score,
            'total': total,
            'percentage': percentage,
            'passed': passed,
            'results': results
        })

    else:
        questions = list(QuizQuestion.objects.all())
        random.shuffle(questions)
        questions = questions[:5]

        return render(request, 'quiz/quiz_home.html', {'questions': questions})
