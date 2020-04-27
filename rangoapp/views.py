from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rangoapp.models import Category, Page, UserProfile
from django.contrib.auth.models import User
from rangoapp.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rangoapp.helpers import visitor_session_handler, get_category_list, get_google_results
from rango import settings


def index(request):
    """
    Index page view
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - index page html
    """

    # set visitor cookie
    visitor_session_handler(request)

    return render(request, 'rangoapp/index.html', {
        'categories': Category.objects.order_by('-likes')[:5],
        'pages': Page.objects.order_by('-views')[:5],
        'visits': request.session['visits']
    })


def about(request):
    """
    About page view
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - about page html
    """
    return render(request, 'rangoapp/about.html', {'my_name': 'Anna Lysak'})


def category_view(request, category_name_slug):
    """
    Category page view
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - category page html
    """
    category = get_object_or_404(Category, slug=category_name_slug)
    category.views += 1
    category.save()

    pages = Page.objects.filter(category=category).order_by('-views')

    # Google search results for searching pages
    result_list = []
    query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        # Run Google search function to get the results list
        result_list = get_google_results(query)

    return render(request, 'rangoapp/category.html', {'category': category,
                                                      'pages': pages,
                                                      'result_list': result_list,
                                                      'query': query})


def suggest_category(request):
    """
    Suggest category view
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - categories list according to search query
    """
    cat_list = []
    if request.method == 'GET':
        search_str = request.GET.get('search_str', '').strip()
        cat_list = get_category_list(search_str)
    return render(request, 'rangoapp/templatetags/cats.html', {'cats': cat_list})


@login_required
def search_more_pages(request):
    """
    Search pages view
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - pages list according to search
    """
    result_list = []
    cat_id = 0
    if request.method == 'POST':
        query = request.POST['query'].strip()
        start = int(request.POST['start'])
        cat_id = int(request.POST['catid'])
        # Google returns up to 100 records for the query
        if query and start < 100:
            # Run Google search function to get the results list
            result_list = get_google_results(query, start=start)
    return render(request, 'rangoapp/parts/search_results.html', {'result_list': result_list,
                                                                  'category': {'id': cat_id}})


@login_required
def auto_add_page(request):
    """
    Add page to category and return newly updated category pages list
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - pages list of certain category
    """
    pages = []
    page = None
    if request.method == 'POST':
        cat_id = request.POST['category_id']
        url = request.POST['url']
        title = request.POST['title']
        category = Category.objects.get(id=int(cat_id))
        if category:
            page = Page.objects.get_or_create(category=category, title=title, url=url)
            pages = Page.objects.filter(category=category).order_by('-views')
    return render(request, 'rangoapp/parts/page_list.html', {'pages': pages, 'page': page})


@login_required
def like_category(request):
    """
    Increase likes amount of category
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - number of likes of category
    """
    likes = 0
    if request.method == 'POST':
        cat_id = request.POST['category_id']
        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            if cat:
                cat.likes += 1
                cat.save()
                likes = cat.likes
    return HttpResponse(likes)


@login_required
def add_category(request):
    """
    Add category view
    :param request: WSGIRequest object
    :return: HTTPResponse with content type 'text-html' - add category form or redirect to index view
    """
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rangoapp:index'))
        else:
            print(form.errors)

    return render(request, 'rangoapp/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    """
    Add page view
    :param request: WSGIRequest object
    :param category_name_slug: category slug to add page
    :return: HTTPResponse with content type 'text-html' - add page to category form or redirect to category page
    """
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

            return redirect(reverse('rangoapp:category', args=(category_name_slug,)))
        else:
            print(form.errors)

    return render(request, 'rangoapp/add_page.html', {'form': form, 'category': category})


def goto(request):
    """
    Increases number of views of the page and redirect to page url
    :param request: WSGIRequest object
    :param category_name_slug: category slug to add page
    :return: redirect to category page
    """
    page_number = int(request.GET.get('page', 0))
    if page_number:
        page = Page.objects.get(id=page_number)
        if page:
            page.views += 1
            page.save()

            return redirect(page.url)

    return redirect(reverse('rangoapp:index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            # hash password with set_password method
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
            try:
                # try to login new registered user
                user = authenticate(username=user.username,
                                    password=request.POST.get('password'))
                if user and user.is_active:
                    login(request, user)
            except Exception as e:
                print("Exception, ", str(e))
                pass

        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    return render(request, 'rangoapp/register.html', {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'registered': registered
    })


def user_login(request):
    error_msg = None

    redirect_next = request.GET.get('next', '/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_next)
            else:
                error_msg = 'Your Rango account is disabled.'
        else:
            error_msg = 'Invalid login details supplied.'

    return render(request, 'rangoapp/login.html', {'error_msg': error_msg, 'next': redirect_next})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rangoapp:index'))



@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('rangoapp:index'))

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rangoapp:profile', args=(user.username,)))
        else:
            print(form.errors)

    return render(request, 'rangoapp/profile.html', {'userprofile': userprofile,
                                                     'selecteduser': user,
                                                     'form': form})



@login_required
def list_profiles(request):
    return render(request, 'rangoapp/user_profiles.html', {'userprofile_list': UserProfile.objects.all()})


