from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from rango.models import Category, Piece, Comment

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from datetime import datetime

from rango.webhose_search import run_query

from django.shortcuts import redirect
from django.contrib.auth.models import User
from rango.models import UserProfile


    

def piece(request, piece_title_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a piece title slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        piece = Piece.objects.get(slug=piece_title_slug)
        comment_list = Comment.objects.filter(song=piece)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        #pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        #context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        #context_dict['category'] = category
        context_dict['piece'] = piece
        context_dict['comment_list'] = comment_list

    except Piece.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        #context_dict['category'] = None
        context_dict['piece'] = None
        context_dict['comment_list'] = None
        

    # Go render the response and return it to the client.
    return render(request, 'rango/piece.html', context_dict)

    
def music(request):
    piece_list_date = Piece.objects.order_by('-title')[:5]
    piece_list_rating = Piece.objects.order_by('artist')[:5]
    context_dict = {'piece_dates': piece_list_date,'piece_rates':piece_list_rating}
    result_list = []
    if request.method == "POST":
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
    return render(request, 'rango/music.html', context_dict)

def index(request):
	request.session.set_test_cookie()

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
	category_list_views = Category.objects.order_by('-id')[:5]
	piece_list_rating = Piece.objects.order_by('-score')[:5]
	context_dict = {'cat_likes': category_list_views,'page_views':piece_list_rating}
	
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'rango/index.html', context_dict)
	# Return response back to the user, updating any cookies that need changed.
	return response

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}

    return render(request, 'rango/about.html', context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        piece_list = Piece.objects.filter(category = category).order_by('-title')

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        #pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        #context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        context_dict['piece_list'] = piece_list

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['piece_list'] = None
        

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()    

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            ###print(cat, cat.slug) 
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_piece(request, category_name_slug):
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
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits   

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'rango/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website,'bio': userprofile.bio,
        'picture': userprofile.picture})
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'rango/profile.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form})
