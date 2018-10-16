from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from kupeza.admin import UserCreationForm
from django.utils import  timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from kupeza.tokens import account_activation_token
from .models import Agencie, Agent, Prop, Bookmarks, Agency, MyUser, Comments, ordinaryuser
from .forms import SignupForm, AgencyCreate, PropertyCreate, SendmessageForm, PropCreate, SearchForm, ProfileForm, \
    PropEdit, ProfileAgencyForm, ratingForm, nonratingForm, ProfileOrdForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
def comments(request,page):
    #if request.user.is_authenticated:
    if request.method == 'POST':
        form = nonratingForm(request.POST)
        #return HttpResponse(page)
        if form.is_valid():
            form.clean()
            if request.user.is_authenticated:
                comment = Comments.objects.create(prop_id = page,user_id = request.user.pk)
                comment.name = form.cleaned_data.get('Your_Name')
                comment.msg = form.cleaned_data.get('Your_Comment')
                comment.prop_id = page
                #comment.user_id = request.user.pk
                comment.email = form.cleaned_data.get('Your_Email')
                comment.save()
            else:
                comment = Comments.objects.create(prop_id = page)
                comment.name = form.cleaned_data.get('Your_Name')
                comment.msg = form.cleaned_data.get('Your_Comment')
                #comment.prop_id = page
                #comment.user_id = request.user.pk
                comment.email = form.cleaned_data.get('Your_Email')
                comment.save()



    return redirect(reverse(property_details, kwargs={'page': page}))

def shortcodes(request):
    return render(request, 'shortcodes.html', {})

def slider(request):
    return render(request, 'index-slider.html', {})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(home)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})
    return render(request, 'password.html', {
        'form': form,
        'user_n': users_n
    })

def sign_in(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(home)
    return render(request, 'sign-in.html', {})

def submit(request):
    return render(request, 'submit.html', {})

def contact(request):
    if request.method == 'POST':
        form = SendmessageForm(request.POST)
        if form.is_valid():
            return HttpResponse(form)
            #pass  # does nothing, just trigger the validation
    else:
        form = SendmessageForm()
        form1 = SearchForm()
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})

    return render(request, 'contact.html', {'user_n': users_n,'form':form ,'form1':form1,})

def search(request):

    return render(request, 'contact.html', {})

def register(request):


    return render(request, 'create-account.html', {})

def reassign(request):


    return render(request, 'create-account.html', {})

@login_required
def edit_prop(request ,page):
    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        form = PropCreate(request.POST)
        if form.is_valid():
           form.clean()
           prop_id = page

           #agent = Agent.objects.get(duser=request.user.pk)
           #agency = Agencie.objects.get(pk=agent.agency_id)
           if request.user.account_type == "agency":
               agency = Agencie.objects.get(duser=request.user.pk)
               prop = Prop.objects.get(pk=prop_id,agency = agency.pk )
           else:
               prop = Prop.objects.get(pk=prop_id)

           #prop = Prop.objects.get(pk= prop_id)
           #,agent = agent.pk ,number_of_garages = form.cleaned_data.get('garages') ,area_dimension = form.cleaned_data.get('area'),number_of_bathrooms = form.cleaned_data.get('baths') ,number_of_bedrooms = form.cleaned_data.get('beds'),date_updated=timezone.now() ,property_price = form.cleaned_data.get('price'))
           prop.title = form.cleaned_data.get('title')
           prop.property_price = form.cleaned_data.get('price')
           prop.address = form.cleaned_data.get('address')
           prop.description = form.cleaned_data.get('description')
           prop.currency= 'k'
           prop.house_plan_file = uploaded_file_url
           prop.date_updated=timezone.now()
           prop.number_of_bedrooms = form.cleaned_data.get('beds')
           prop.number_of_rooms= form.cleaned_data.get('address')
           prop.number_of_bathrooms = form.cleaned_data.get('baths')
           prop.number_of_garages = form.cleaned_data.get('garages')
           prop.area_dimension = form.cleaned_data.get('area')
           prop.payment_options = form.cleaned_data.get('status')
           prop.tags = form.cleaned_data.get('tags')
           prop.property_type = form.cleaned_data.get('Property_type')
           prop.video = form.cleaned_data.get('video')
           if form.cleaned_data.get('town') != "Towns":
              prop.town = form.cleaned_data.get('town')
           if form.cleaned_data.get('city') != "City":
              prop.city = form.cleaned_data.get('city')
           if form.cleaned_data.get('provinces') != "provinces":
              prop.province = form.cleaned_data.get('provinces')
           prop.save()

        #next = request.POST.get('next', '/')
        #return HttpResponseRedirect(next)

        return redirect(reverse(edit_props, kwargs={'page': page}))

        #return redirect(my_properties)
    elif request.method == 'POST':
        form = PropEdit(request.POST)
        if form.is_valid():
           form.clean()
           prop_id = page

           # agent = Agent.objects.get(duser=request.user.pk)
           if request.user.account_type == "agency":
               agency = Agencie.objects.get(duser=request.user.pk)
               prop = Prop.objects.get(pk=prop_id)
               #prop = Prop.objects.get(pk=prop_id,agency = agency.pk )
           else:
               prop = Prop.objects.get(pk=prop_id)

               #text - field

           #return HttpResponse(form.cleaned_data.get('tags'))
           # agency = Agencie.objects.get(pk=agent.agency_id)

           #prop = Prop.objects.get(pk=prop_id)
           # ,agent = agent.pk ,number_of_garages = form.cleaned_data.get('garages') ,area_dimension = form.cleaned_data.get('area'),number_of_bathrooms = form.cleaned_data.get('baths') ,number_of_bedrooms = form.cleaned_data.get('beds'),date_updated=timezone.now() ,property_price = form.cleaned_data.get('price'))
           prop.title = form.cleaned_data.get('title')
           prop.tags = form.cleaned_data.get('tags')
           prop.property_price = form.cleaned_data.get('price')
           prop.address = form.cleaned_data.get('address')
           prop.description = form.cleaned_data.get('description')
           prop.currency = 'k'
           #prop.house_plan_file = uploaded_file_url
           prop.date_updated = timezone.now()
           prop.number_of_bedrooms = form.cleaned_data.get('beds')
           prop.number_of_rooms = form.cleaned_data.get('address')
           prop.number_of_bathrooms = form.cleaned_data.get('baths')
           prop.number_of_garages = form.cleaned_data.get('garages')
           prop.area_dimension = form.cleaned_data.get('area')
           prop.video = form.cleaned_data.get('video')
           prop.payment_options = form.cleaned_data.get('status')
           prop.property_type = form.cleaned_data.get('Property_type')
           if form.cleaned_data.get('town') != "Towns":
               prop.town = form.cleaned_data.get('town')
           if form.cleaned_data.get('city') != "City":
               prop.city = form.cleaned_data.get('city')
           if form.cleaned_data.get('provinces') != "provinces":
               prop.province = form.cleaned_data.get('provinces')
           prop.save()

           return redirect(reverse(edit_props, kwargs={'page': page}))
           #return HttpResponse(prop_id)

        return redirect(my_properties)
            #pass  # does nothing, just trigger the validation
    else:
        page = request.GET.get('page', 1)
        try:
            users = Prop.objects.get(pk = page)
        except PageNotAnInteger:
            users = Prop.objects.get(pk=page)
        except EmptyPage:
            users  = Prop.objects.get(pk = page)
        request.session['prop_id'] = page
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})
        #agency = Agencie.objects.get(duser=request.user.pk)

        #return HttpResponse(agency.pk)

        form = PropEdit(initial={'video':users.video,'choiceprop':users.property_type,'town':users.town,'city':users.city ,'price':users.property_price,'beds':users.number_of_bedrooms,'garages': users.number_of_garages,'status':users.property_status,'area':users.area_dimension,'payment_option':users.payment_options,'baths':users.number_of_bathrooms,'description':users.description,'provinces':users.province,'title':users.title,'address':users.address})
    #return render(request, 'sukit.html', {'form':form})
    return render(request, 'sub.html', {'user_n': users_n,'form':form ,'image_profile': users.house_plan_file})

@login_required
def edit_props(request,page):
    if request.user.account_type == "agency":
        agency = Agencie.objects.get(duser=request.user.pk)
        users = get_object_or_404(Prop, pk=page, agency=agency.pk)
    elif request.user.account_type == "agent":
        agency = Agent.objects.get(duser_id=request.user.pk)
        users = get_object_or_404(Prop, pk=page, agent=agency.pk)


    #agency = Agencie.objects.get(duser=request.user.pk)
    #users = get_object_or_404(Prop, pk=page ,agency= agency.pk)

    # return HttpResponse(agency.pk)

    form = PropEdit(
        initial={'tags':users.tags,'video': users.video, 'choiceprop': users.property_type, 'town': users.town, 'city': users.city,
                 'price': users.property_price, 'beds': users.number_of_bedrooms, 'garages': users.number_of_garages,
                 'status': users.property_status, 'area': users.area_dimension, 'payment_option': users.payment_options,
                 'baths': users.number_of_bathrooms, 'description': users.description, 'provinces': users.province,
                 'title': users.title, 'address': users.address})
    # return render(request, 'sukit.html', {'form':form})
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})


    return render(request, 'sub.html', {'user_n': users_n,'form':form ,'image_profile': users.house_plan_file,'id':users.pk})

@login_required
def create_prop(request):
    if request.method == 'POST' and 'image' in request.FILES:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        form = PropCreate(request.POST)
        if form.is_valid():
           form.clean()

           agent = Agent.objects.get(duser=request.user.pk)
           agency = Agencie.objects.get(pk=agent.agency_id)

           prop = Prop.objects.create(agency= agency.pk ,agent = agent.pk ,number_of_garages = form.cleaned_data.get('garages') ,area_dimension = form.cleaned_data.get('area'),number_of_bathrooms = form.cleaned_data.get('baths') ,number_of_bedrooms = form.cleaned_data.get('beds'),date_updated=timezone.now() ,property_price = form.cleaned_data.get('price'))
           prop.title = form.cleaned_data.get('title')
           #prop.property_price = form.cleaned_data.get('price')
           prop.address = form.cleaned_data.get('address')
           prop.description = form.cleaned_data.get('description')
           prop.currency= 'k'
           prop.house_plan_file = uploaded_file_url
           #prop.number_of_bedrooms = form.cleaned_data.get('beds')
           #prop.number_of_rooms= form.cleaned_data.get('address')
           #prop.number_of_bathrooms = form.cleaned_data.get('baths')
           #prop.number_of_garages = form.cleaned_data.get('garages')
           #prop.area_dimension = form.cleaned_data.get('area')
           prop.payment_options = form.cleaned_data.get('status')
           prop.property_type = form.cleaned_data.get('Property_type')
           if form.cleaned_data.get('town') != "Towns":
              prop.town = form.cleaned_data.get('town')
           if form.cleaned_data.get('city') != "City":
              prop.city = form.cleaned_data.get('city')
           if form.cleaned_data.get('provinces') != "provinces":
              prop.province = form.cleaned_data.get('provinces')
           prop.save()

        return redirect(my_properties)

        #return HttpResponse("hi")

    elif request.method == 'POST':
        form = PropCreate(request.POST)
        if form.is_valid():
           form.clean()
           agent = Agent.objects.get(duser=request.user.pk)
           agency = Agencie.objects.get(pk=agent.agency_id)

           prop = Prop.objects.create(agency= agency.pk ,agent = agent.pk ,number_of_garages = form.cleaned_data.get('garages') ,area_dimension = form.cleaned_data.get('area'),number_of_bathrooms = form.cleaned_data.get('baths') ,number_of_bedrooms = form.cleaned_data.get('beds'),date_updated=timezone.now() ,property_price = form.cleaned_data.get('price'))
           prop.title = form.cleaned_data.get('title')
           #prop.property_price = form.cleaned_data.get('price')
           prop.address = form.cleaned_data.get('address')
           prop.description = form.cleaned_data.get('description')
           prop.currency= 'k'
           #prop.number_of_bedrooms = form.cleaned_data.get('beds')
           #prop.number_of_rooms= form.cleaned_data.get('address')
           #prop.number_of_bathrooms = form.cleaned_data.get('baths')
           #prop.number_of_garages = form.cleaned_data.get('garages')
           #prop.area_dimension = form.cleaned_data.get('area')
           prop.payment_options = form.cleaned_data.get('status')
           prop.property_type = form.cleaned_data.get('Property_type')
           if form.cleaned_data.get('town') != "Towns":
              prop.town = form.cleaned_data.get('town')
           if form.cleaned_data.get('city') != "City":
              prop.city = form.cleaned_data.get('city')
           if form.cleaned_data.get('provinces') != "provinces":
              prop.province = form.cleaned_data.get('provinces')
           prop.save()


           return redirect(my_properties)
            #pass  # does nothing, just trigger the validation
    else:
        form = PropCreate()
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})
    return render(request, 'sukit.html', {'user_n': users_n,'form':form})
@login_required
def agency_create_prop(request):
    if request.method == 'POST' and 'image' in request.FILES:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        form = PropCreate(request.POST)
        if form.is_valid():
           form.clean()

           agency = Agencie.objects.get(duser=request.user.pk)
           prop = Prop.objects.create(agency= agency.pk ,number_of_garages = form.cleaned_data.get('garages') ,area_dimension = form.cleaned_data.get('area'),number_of_bathrooms = form.cleaned_data.get('baths') ,number_of_bedrooms = form.cleaned_data.get('beds'),date_updated=timezone.now() ,property_price = form.cleaned_data.get('price'))
           prop.title = form.cleaned_data.get('title')
           #prop.property_price = form.cleaned_data.get('price')
           prop.address = form.cleaned_data.get('address')
           prop.description = form.cleaned_data.get('description')
           prop.currency= 'k'
           prop.house_plan_file = uploaded_file_url
           #prop.number_of_bedrooms = form.cleaned_data.get('beds')
           #prop.number_of_rooms= form.cleaned_data.get('address')
           #prop.number_of_bathrooms = form.cleaned_data.get('baths')
           #prop.number_of_garages = form.cleaned_data.get('garages')
           #prop.area_dimension = form.cleaned_data.get('area')
           prop.property_status = form.cleaned_data.get('status')

           prop.payment_options = form.cleaned_data.get('payment_option')
           prop.property_type = form.cleaned_data.get('Property_type')
           if form.cleaned_data.get('town') != "Towns":
              prop.town = form.cleaned_data.get('town')
           if form.cleaned_data.get('city') != "City":
              prop.city = form.cleaned_data.get('city')
           if form.cleaned_data.get('provinces') != "provinces":
              prop.province = form.cleaned_data.get('provinces')
           prop.save()

        return redirect(my_properties)

        #return HttpResponse("hi")

    elif request.method == 'POST':
        form = PropCreate(request.POST)
        if form.is_valid():
           form.clean()
           agency = Agencie.objects.get(duser=request.user.pk)

           prop = Prop.objects.create(agency= agency.pk ,number_of_garages = form.cleaned_data.get('garages') ,area_dimension = form.cleaned_data.get('area'),number_of_bathrooms = form.cleaned_data.get('baths') ,number_of_bedrooms = form.cleaned_data.get('beds'),date_updated=timezone.now() ,property_price = form.cleaned_data.get('price'))
           prop.title = form.cleaned_data.get('title')
           #prop.property_price = form.cleaned_data.get('price')
           prop.address = form.cleaned_data.get('address')
           prop.description = form.cleaned_data.get('description')
           prop.currency= 'k'
           #prop.number_of_bedrooms = form.cleaned_data.get('beds')
           #prop.number_of_rooms= form.cleaned_data.get('address')
           #prop.number_of_bathrooms = form.cleaned_data.get('baths')
           #prop.number_of_garages = form.cleaned_data.get('garages')
           #prop.area_dimension = form.cleaned_data.get('area')
           prop.property_status = form.cleaned_data.get('status')
           prop.payment_options = form.cleaned_data.get('payment_option')
           prop.property_type = form.cleaned_data.get('Property_type')
           if form.cleaned_data.get('town') != "Towns":
              prop.town = form.cleaned_data.get('town')
           if form.cleaned_data.get('city') != "City":
              prop.city = form.cleaned_data.get('city')
           if form.cleaned_data.get('provinces') != "provinces":
              prop.province = form.cleaned_data.get('provinces')
           prop.save()

           return redirect(my_properties)
            #pass  # does nothing, just trigger the validation
    else:
        form = PropCreate()
    return render(request, 'sukit.html', {'form':form})

def create_agency(request):
    #form = AgencyForm()
    if request.method == 'POST':
        form = AgencyCreate(request.POST)
        if form.is_valid():
            form.clean()
            package_map = ["free","silver","gold"]
            agency = Agencie.objects.create()
            agency.duser = request.user.pk
            agency.agency_name = form.cleaned_data.get('Agent_name')
            agency.address = form.cleaned_data.get('address_line_1')
            agency.address1 = form.cleaned_data.get('address_line_2')
            agency.description = form.cleaned_data.get('description')
            agency.phone = form.cleaned_data.get('phone')
            agency.email = form.cleaned_data.get('email')
            agency.website = form.cleaned_data.get('website')
            agency.package =  package_map.index(form.cleaned_data.get('package')) + 1
            agency.save()
            return HttpResponse(Agencie.objects.order_by('agency_name'))

            #pass  # does nothing, just trigger the validation
    else:
        form = AgencyCreate()
    return render(request, 'agency.html', {'form':form})



def user_create_prop(request):
    if request.method == 'POST':
        form = PropertyCreate(request.POST)
        #if form.is_valid():
        return HttpResponse(form)
            #pass  # does nothing, just trigger the validation
    else:
        form = PropertyCreate()
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})

    return render(request, 'sumit.html', {'user_n': users_n,'form':form})

def about_us(request):
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})
    return render(request, 'about-us.html', {'user_n': users_n})

def agent_detail(request):
    if request.method == 'POST':
        form = SendmessageForm(request.POST)
        if form.is_valid():
            return HttpResponse(form)
            #pass  # does nothing, just trigger the validation
    else:
        page = request.GET.get('page', 1)
        book = get_object_or_404(Agent, pk=page)

        if book:
            props = Prop.objects.filter(agent=book.pk)
            props_number = Prop.objects.filter(agent=book.pk).count()

        form = SendmessageForm()
        form1 = SearchForm()

        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})
    return render(request, 'agent-detail.html', {'user_n': users_n,'form':form ,'form1':form1,'book':book ,'props':props ,'props_number':props_number })

def agency_detail(request):
    if request.method == 'POST':
        form = SendmessageForm(request.POST)
        if form.is_valid():
            return HttpResponse(form)
            #pass  # does nothing, just trigger the validation
    else:

        page = request.GET.get('page', 1)
        book = get_object_or_404(Agencie, pk=page)
        if book:
            props = Prop.objects.filter(agency=book.pk)
            props_number = Prop.objects.filter(agency=book.pk).count()
            agents = Agent.objects.filter(agency_id = book.pk , account_status = 1)
            agents_number = Agent.objects.filter(agency_id = book.pk).count()


        form = SendmessageForm()
        form1 = SearchForm()
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})
    return render(request, 'agency-detail.html', {'user_n': users_n,'form':form ,'form1':form1 ,'agents':agents,'agents_number': agents_number,'book':book ,'props':props ,'props_number':props_number})

def invoice(request):
    return render(request, 'invoice-print.html', {})

@login_required
def profile(request):
    if request.method == 'POST':
        if request.user.account_type == "agent":
            form = ProfileForm(request.POST)
            if form.is_valid():
                form.clean()
                book = Agent.objects.get(duser=request.user.pk)
                book.phone_number = form.cleaned_data.get('Phone')
                book.facebook = form.cleaned_data.get('facebook')
                book.twitter = form.cleaned_data.get('twitter')
                book.bio = form.cleaned_data.get('bio')
                book.first_name = form.cleaned_data.get('First_Name')
                book.last_name = form.cleaned_data.get('Last_Name')
                book.skype = form.cleaned_data.get('skype')
                book.pintrest = form.cleaned_data.get('Pintrest')
                book.save()
                return redirect(profile)
        else:
            form = ProfileOrdForm(request.POST)
            if form.is_valid():
                form.clean()
                book = ordinaryuser.objects.get(duser=request.user.pk)
                book.phone_number = form.cleaned_data.get('Phone')
                book.facebook = form.cleaned_data.get('facebook')
                book.twitter = form.cleaned_data.get('twitter')
                # book.bio = form.cleaned_data.get('bio')
                book.first_name = form.cleaned_data.get('First_Name')
                book.last_name = form.cleaned_data.get('Last_Name')
                book.skype = form.cleaned_data.get('skype')
                book.pintrest = form.cleaned_data.get('Pintrest')
                book.save()
                # request.user.email= form.cleaned_data.get('Email')

                return redirect(profile)
            #pass  # does nothing, just trigger the validation
    else:
        if request.user.account_type =="user":
            book = ordinaryuser.objects.get(duser=request.user.pk)
            user_new = Prop.objects.all().order_by('-date_added')
            # paginator = Paginator(user_list, 6)

            page = request.GET.get('page', 1)

            paginator = Paginator(user_new, 2)
            try:
                users_n = paginator.page(page)
            except PageNotAnInteger:
                users_n = paginator.page(1)
            except EmptyPage:
                users_n = paginator.page(paginator.num_pages)
                # return render(request, 'index-slider-horizontal-search-box.html',
                #              {'users': users, 'user_n': users_n})
                # get_object_or_404(Agent, pk=request.user.pk)

            form = ProfileOrdForm(
                initial={ 'First_Name': book.first_name, 'Last_Name': book.last_name,
                         'Email': request.user.email, 'Phone': book.phone_number, 'skype': book.skype,
                         'twitter': book.twitter, 'facebook': book.facebook, 'Pintrest': book.pintrest})

            return render(request, 'profiler.html', {'user_n': users_n, 'form': form, 'image': book.profile_photo})

            # book =Agent.objects.get(duser=request.user.pk)

        else:
            book = Agent.objects.get(duser=request.user.pk)
            user_new = Prop.objects.all().order_by('-date_added')
            # paginator = Paginator(user_list, 6)

            page = request.GET.get('page', 1)

            paginator = Paginator(user_new, 2)
            try:
                users_n = paginator.page(page)
            except PageNotAnInteger:
                users_n = paginator.page(1)
            except EmptyPage:
                users_n = paginator.page(paginator.num_pages)
                # return render(request, 'index-slider-horizontal-search-box.html',
                #              {'users': users, 'user_n': users_n})
                # get_object_or_404(Agent, pk=request.user.pk)

            form = ProfileForm(
                initial={'Your_Agency': book.agency_id, 'First_Name': book.first_name, 'Last_Name': book.last_name,
                         'Email': request.user.email, 'Phone': book.phone_number, 'bio': book.bio, 'skype': book.skype,
                         'twitter': book.twitter, 'facebook': book.facebook, 'Pintrest': book.pintrest})
        #book =Agent.objects.get(duser=request.user.pk)

            return render(request, 'profile.html', {'user_n': users_n,'form':form ,'image':book.profile_photo})

@login_required
def agency_profile(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        form = ProfileAgencyForm(request.POST)
        book = Agencie.objects.get(duser=request.user.pk)
        if form.is_valid():
           form.clean()
           #book.image_logo = uploaded_file_url
           book = Agencie.objects.get(duser=request.user.pk)
           book.image_logo = uploaded_file_url
           book.phone_number = form.cleaned_data.get('Phone')
           book.facebook = form.cleaned_data.get('facebook')
           book.twitter = form.cleaned_data.get('twitter')
           book.description = form.cleaned_data.get('bio')
           book.address1 = form.cleaned_data.get('Address_Line_2')
           book.address = form.cleaned_data.get('Address_Line_1')
           book.skype = form.cleaned_data.get('skype')
           book.pintrest = form.cleaned_data.get('Pintrest')
           book.agency_name = form.cleaned_data.get('Agency_Name')
           book.city = form.cleaned_data.get('City')
           book.website = form.cleaned_data.get('Website')
           book.description = form.cleaned_data.get('bio')
           #book.email = form.cleaned_data.get('email')

           book.save()
    elif request.method == 'POST':
        form = ProfileAgencyForm(request.POST)

        if form.is_valid():
            form.clean()
            book = Agencie.objects.get(duser=request.user.pk)
            book.phone_number = form.cleaned_data.get('Phone')
            #book.email = form.cleaned_data.get('email')
            book.facebook= form.cleaned_data.get('facebook')
            book.twitter = form.cleaned_data.get('twitter')
            book.description = form.cleaned_data.get('bio')
            book.address1 = form.cleaned_data.get('Address_Line_2')
            book.address = form.cleaned_data.get('Address_Line_1')
            book.skype = form.cleaned_data.get('skype')
            book.pintrest = form.cleaned_data.get('Pintrest')
            book.agency_name = form.cleaned_data.get('Agency_Name')
            book.city = form.cleaned_data.get('City')
            book.description = form.cleaned_data.get('bio')
            book.website =  form.cleaned_data.get('Website')
            book.save()
            #request.user.email= form.cleaned_data.get('Email')

            return redirect(agency_profile)
            #pass  # does nothing, just trigger the validation
    else:
        #form = ProfileAgencyForm()
        book =Agencie.objects.get(duser=request.user.pk)
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})
            # get_object_or_404(Agent, pk=request.user.pk)



            #get_object_or_404(Agent, pk=request.user.pk)




        form = ProfileAgencyForm(initial={'Agency_Name':book.agency_name,'City':book.city,'Address_Line_1': book.address,'Address_Line_2': book.address1,'Email':book.email,'Phone':book.phone ,'bio':book.description ,'Website':book.website ,'skype':book.skype,'twitter':book.twitter,'facebook':book.facebook,'Pintrest':book.pintrest })
    return render(request, 'profiles.html', {'user_n': users_n,'form':form ,'image':book.image_logo})

def property_detail(request):
    if request.method == 'POST':
        form = SendmessageForm(request.POST)
        if form.is_valid():
            return HttpResponse(form)

            #pass  # does nothing, just trigger the validation
    else:
        page = request.GET.get('page', 1)
        book = get_object_or_404(Prop, pk=page)
        if book :
           agent = Agent.objects.get(pk=book.agent)
           num = Bookmarks.objects.filter(prop_id=book.pk ,user_id = request.user.pk).count()
           bkmrk = False
           if num > 0:
               bookmark = Bookmarks.objects.get(prop_id=book.pk,user_id = request.user.pk)
               bkmrk = bookmark.state
               #return HttpResponse(str(bkmrk)+" "+str(bookmark.pk))


        form2 = SendmessageForm()
        if request.user.is_authenticated :
            if request.user.account_type =="agency":
               agency = Agencie.objects.get(duser=request.user.pk)
               form = ratingForm(initial={'Your_Email':request.user.email, 'Your_Name':agency.agency_name})
            elif request.user.account_type =="agent":
                agency = Agent.objects.get(duser_id=request.user.pk)
                form = ratingForm(initial={'Your_Email': request.user.email, 'Your_Name': agency.first_name+" "+agency.last_name})
            else:
                form = nonratingForm()



        else:
            form = nonratingForm()

        form1 = SearchForm()
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
            # return render(request, 'index-slider-horizontal-search-box.html',
            #              {'users': users, 'user_n': users_n})

    return render(request, 'property-detail.html', {'user_n': users_n,'bookmark':bkmrk,'form':form ,'form1':form1 ,'book':book ,'agent':agent})

def property_details(request, page):
    #page = request.GET.get('page', 1)

    #return HttpResponse(page)
    book = get_object_or_404(Prop, pk=page)
    tags_len = 0
    tags = ""
    if book:
        agent = Agent.objects.get(pk=book.agent)
        num = Bookmarks.objects.filter(prop_id=book.pk, user_id=request.user.pk).count()
        comments = Comments.objects.filter(subcomment = 0,prop_id = page).order_by('-date_added')
        comments_num = Comments.objects.filter(subcomment = 0,prop_id = page).count()
        bkmrk = False
        if book.tags:
            tags = book.tags
            tags = tags.split(",")
            tags_len = len(tags)
        if num > 0:
            bookmark = Bookmarks.objects.get(prop_id=book.pk, user_id=request.user.pk)
            bkmrk = bookmark.state




            #return HttpResponse(james)

    form = SendmessageForm()
    form1 = SearchForm()
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})


    return render(request, 'property-detail.html', {'comments_num':comments_num,'comments':comments,'user_n': users_n,'tags_len':tags_len,'tags':tags,'bookmark':bkmrk,'form':form ,'form1':form1 ,'book':book ,'agent':agent})



def property_listing(request):
    return render(request, 'properties-listing.html', {})

def agents_listing(request):
    user_list = Agent.objects.exclude(first_name='')
    #paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    form1 = SearchForm()
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})


    return render(request, 'agents-listing.html', {'users': users ,'form1':form1 ,'user_n': users_n})

def agency_listing(request):
    user_list = Agencie.objects.all()
    #paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    form1 = SearchForm()
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})

    return render(request, 'agencies-listing.html', {'users': users,'form1':form1,'user_n': users_n })
def add_bookmark(request):
    page = request.GET.get('page', 1)
    book = get_object_or_404(Prop, pk=page)

    if  not request.user.is_authenticated:
        return redirect(reverse(property_details, kwargs={'page': page}))


    if book:
       num = Bookmarks.objects.filter(prop_id = book.pk ,user_id= request.user.pk).count()
       if num > 0 :
            bookmark = Bookmarks.objects.get(prop_id = book.pk ,user_id= request.user.pk)


            if bookmark.state == True:
               bookmark.state = False
               bookmark.save()

            else:
                bookmark.state =  True
                bookmark.save()
            #return HttpResponse(bookmark.state)
                #request.build_absolute_uri()
       else:
           Bookmarks.objects.create(prop_id = book.pk ,user_id= request.user.pk , state = True)
       #response = redirect('url-name', x)
       #response['Location'] += '?your=querystring'

       return  redirect(reverse(property_details, kwargs={'page': page}))

       #return HttpResponseRedirect(str(request.build_absolute_uri()))


    #return request

def property_grid_listing(request):
    city = request.GET.get('city', "City")
    status = request.GET.get('status', "status")
    town = request.GET.get('town', "Towns")
    provinces = request.GET.get('provinces', "provinces")
    Property_type = request.GET.get('Property_type', "Type")
    price_range = request.GET.get('price_range', "0;10000000000000")
    price_ranger = price_range.split(";")
    #return HttpResponse(price_ranger)
    if len(price_ranger) > 1:
        lower = int(price_ranger[0])
        upper = int(price_ranger[1])
        param = "price_range=" + price_ranger[0] + ";price_range2=" + price_ranger[
            1] + "&city=" + city + "&status=" + status + "&town=" + town + "&provinces=" + provinces + "&Property_type=" + Property_type

    else:
        lower =  request.GET.get('price_range', "0")
        upper  = request.GET.get('price_range2', "1000000000000000")
        param = "price_range="+lower+";price_range2="+upper+"&city="+city+"&status="+status+"&town="+town+"&provinces="+provinces+"&Property_type="+Property_type
        lower = int(lower)
        upper = int(upper)
    #lower = int(price_ranger[0])
    #upper = int(price_ranger[1])
    user_list = Prop.objects.filter(property_price__gte=lower,property_price__lte= upper)
    user_count = Prop.objects.filter(property_price__gte=lower, property_price__lte=upper).count()
    if city != "City" and status != "status" and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(city=city ,province__icontains=provinces ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(city=city ,province__icontains=provinces ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif status != "status" and town !="Towns" and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(town__icontains= town,province__icontains=provinces ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(town__icontains= town,province__icontains=provinces ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif city != "City" and status != "status" and town !="Towns" and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(Q(city__icontains=city) | Q(town__icontains= town),province__icontains=provinces ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(Q(city__icontains=city) | Q(town__icontains= town),province__icontains=provinces ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif city != "City" and town !="Towns" and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(Q(city__icontains=city) | Q(town__icontains= town),province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(Q(city__icontains=city) | Q(town__icontains= town),province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif city != "City"  and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(city=city ,province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(city=city ,province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif city != "City" and status != "status"  and Property_type != "Type" :
        user_count = Prop.objects.filter(city=city ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(city=city ,property_type__icontains= Property_type ,property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif city != "City" and status != "status"  and provinces != "provinces" :
        user_count = Prop.objects.filter(city=city ,province__icontains=provinces ,property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(city=city ,province__icontains=provinces ,property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif town !="Towns"   and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(town__icontains =city ,province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(town__icontains =city ,province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif town !="Towns"  and status != "status"  and Property_type != "Type" :
        user_count = Prop.objects.filter(town__icontains =city ,property_status =status ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(town__icontains =city ,property_status =status ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif town !="Towns"  and status != "status"  and provinces != "provinces" :
        user_count = Prop.objects.filter(town__icontains =city ,property_status =status ,province__icontains=provinces,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(town__icontains =city ,property_status =status ,province__icontains=provinces,property_price__gte=lower,property_price__lte= upper)
    elif  status != "status"  and provinces != "provinces" and Property_type != "Type" :
        user_count = Prop.objects.filter(province__icontains=provinces ,property_type__icontains= Property_type,property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(province__icontains=provinces ,property_type__icontains= Property_type,property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif provinces != "provinces" and Property_type != "Type":
        user_count = Prop.objects.filter(province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(province__icontains=provinces ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif status != "status" and Property_type != "Type":
        user_count = Prop.objects.filter(property_status =status ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(property_status =status ,property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif status != "status" :
        user_count = Prop.objects.filter(property_status =status,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(property_status =status,property_price__gte=lower,property_price__lte= upper)
    elif provinces != "provinces" :
        user_count = Prop.objects.filter(province__icontains=provinces,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(province__icontains=provinces,property_price__gte=lower,property_price__lte= upper)
    elif  Property_type != "Type":
        user_count = Prop.objects.filter(property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(property_type__icontains= Property_type,property_price__gte=lower,property_price__lte= upper)
    elif city != "City"  :
        user_count = Prop.objects.filter(city__icontains=city,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(city__icontains=city,property_price__gte=lower,property_price__lte= upper)
    elif town !="Towns"  :
        user_count = Prop.objects.filter(town__icontains = town,property_price__gte=lower,property_price__lte= upper).count()
        user_list = Prop.objects.filter(town__icontains = town,property_price__gte=lower,property_price__lte= upper)




    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    form1 = SearchForm()

    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
    #return render(request, 'index-slider-horizontal-search-box.html',
    #              {'users': users, 'user_n': users_n})

    #return HttpResponse(param)

    return render(request, 'properties-listing-grid.html', {'user_n': users_n,'param':param,'users': users ,'user_count':user_count,'form1':form1})

def property_line_listing(request):
    return render(request, 'properties-listing-lines.html', {})

@login_required
def my_agents(request):

    book = Agencie.objects.get(duser=request.user.pk)
    user_count = Agent.objects.filter(agency_id=book.pk).count()
    user_list = Agent.objects.filter(agency_id=book.pk)
    #user_list = Prop.objects.filter(agency=request.user.pk)
    #user_list = Prop.objects.all()
    paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})
    return render(request, 'my-agents.html', {'user_n': users_n,'users': users,'user_count':user_count })

@login_required
def assign_prop(request):

    book = Agencie.objects.get(duser=request.user.pk)
    user_count = Agent.objects.filter(agency_id=book.pk).count()
    page = request.GET.get('page', 1)
    prop = Prop.objects.get(pk=page)
    user_list = Agent.objects.filter(agency_id=book.pk , account_status = 1).exclude(pk = prop.agent)


    return render(request, 'assign-prop.html', {'users': user_list,'user_count':user_count,'page':page })

@login_required
def assign_agents(request):

    book = Agencie.objects.get(duser=request.user.pk)
    user_count = Agent.objects.filter(agency_id=book.pk).count()
    page = request.GET.get('page', 1)
    user_list = Agent.objects.filter(agency_id=book.pk , account_status = 1).exclude(pk = page)


    return render(request, 'assign-agents.html', {'users': user_list,'user_count':user_count,'page':page })

@login_required
def prop_trans(request):
    page = request.GET.get('page', 1)
    intented_change = request.GET.get('intented', 1)
    book = get_object_or_404(Agent, pk=page)
    book1 = get_object_or_404(Prop, pk=intented_change)
    agency = Agencie.objects.get(duser=request.user.pk)
    #prop =
    if book and book1:
        if book1.agency == agency.pk and  book.agency_id == agency.id:
            prop_count = Prop.objects.filter(pk=book1.pk, agency=agency.pk)
            prop_count.update(agent=book.pk)




    return redirect(my_properties)

@login_required
def prop_transfare(request):
    page = request.GET.get('page', 1)
    intented_change = request.GET.get('intented', 1)
    book = get_object_or_404(Agent, pk=page)
    book1 = get_object_or_404(Agent, pk=intented_change)
    agency = Agencie.objects.get(duser=request.user.pk)
    #prop =
    if book and book1:
        prop_count = Prop.objects.filter(agent=book1.pk ,agency = agency.pk).count()
        if prop_count > 0:
            prop = Prop.objects.filter(agent=book1.pk, agency=agency.pk)
            prop.update(agent=book.pk)
            #prop.save()

        #book.account_status = 1
        #book.save()

    return redirect(my_agents)
@login_required
def accept_agents(request):



    page = request.GET.get('page', 1)
    book = get_object_or_404(Agent, pk=page)
    if book:
        book.account_status= 1
        book.save()


    return redirect(my_agents)

@login_required
def deactivate_agents(request):
    page = request.GET.get('page', 1)
    book = get_object_or_404(Agent, pk=page)
    if book:
        book.account_status= 2
        book.save()


    return redirect(my_agents)

@login_required
def my_properties(request):
    if request.user.account_type=="agent":
       book = Agent.objects.get(duser=request.user.pk)
       user_count = Prop.objects.filter(agent=book.pk).count()
       user_list = Prop.objects.filter(agent=book.pk)
    elif request.user.account_type=="agency":
        book = Agencie.objects.get(duser=request.user.pk)
        user_count = Prop.objects.filter(agency=book.pk).count()
        user_list = Prop.objects.filter(agency=book.pk)
    else:
        user_count = Prop.objects.filter(ord_user = 1).count()
        user_list = Prop.objects.filter(ord_user = 1)

    #user_list = Prop.objects.filter(agency=request.user.pk)
    #user_list = Prop.objects.all()
    paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})
    return render(request, 'my-properties.html', {'user_n': users_n,'users': users ,'user_count':user_count })
@login_required
def bookmarked(request):
    bookmarks = Bookmarks.objects.filter(user_id=request.user.pk , state = True).values_list('prop_id', flat=True)

    #return HttpResponse(request.build_absolute_uri())
    user_count = Prop.objects.filter(id__in=bookmarks).count()
    user_list = Prop.objects.filter(id__in=bookmarks)
    #user_list = Prop.objects.all()
    paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    user_new = Prop.objects.all().order_by('-date_added')
    # paginator = Paginator(user_list, 6)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_new, 2)
    try:
        users_n = paginator.page(page)
    except PageNotAnInteger:
        users_n = paginator.page(1)
    except EmptyPage:
        users_n = paginator.page(paginator.num_pages)
        # return render(request, 'index-slider-horizontal-search-box.html',
        #              {'users': users, 'user_n': users_n})
    return render(request, 'bookmarked.html', {'user_n': users_n ,'users': users ,'user_count':user_count })

def fourzerothree(request):
    return render(request, '403.html', {})

def fourzerofour(request):
    return render(request, '404.html', {})

def emailactivate(request):
    return render(request, 'email-you.html', {})

def fivehundred(request):
    return render(request, '500.html', {})

def faq(request):
    return render(request, 'faq.html', {})

def privacypolicy(request):
    return render(request, 'faq.html', {})

def termsandconditions(request):
    return render(request, 'terms-conditions.html', {})

def right_side(request):
    return render(request, 'right-sidebar.html', {})

def left_side(request):
    return render(request, 'left-sidebar.html', {})

def timeline(request):
    return render(request, 'timeline.html', {})

def terms_conditions(request):
    return render(request, 'terms-conditions.html', {})

def rtl(request):
    return render(request, 'rtl.html', {})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        book = Agent.objects.get(duser=request.user.pk)
        book.profile_photo = uploaded_file_url
        book.save()

        return redirect(profile)
    return render(request, 'simple_upload.html')

def signs(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            agency_account = request.POST['package']
            if agency_account == "user":
                user = form.save(commit=False)
                user.is_active = False
                user.account_type = agency_account
                user.save()
                current_site = get_current_site(request)
                agent = ordinaryuser.objects.create(duser_id=user.pk)
                agent.email_address = user.email
                # agent.duser_id(2)
                agent.phone_number = "0775682349"
                # agency = Agencie.objects.get(pk=int(request.POST['Select_Your_Agency']))
                # agent.agency=request.POST['Select_Your_Agency']
                agent.save()
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                #ord_user = Users.objects.create(user_h=user.pk, account_type_user=agency_account)
                #ord_user.save()
                email.send()
                return redirect(emailactivate)
            elif agency_account == "agent":
                user = form.save(commit=False)
                user.is_active = False
                user.account_type = agency_account

                user.save()
                agency = Agencie.objects.get(pk=int(request.POST['Select_Your_Agency']))

                agent = Agent.objects.create(duser_id=user.pk, agency_id=agency.pk)
                agent.email_address = user.email
                # agent.duser_id(2)
                agent.phone_number = "0775682349"
                # agency = Agencie.objects.get(pk=int(request.POST['Select_Your_Agency']))
                # agent.agency=request.POST['Select_Your_Agency']
                agent.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()


                return redirect(emailactivate)
            elif agency_account == "agency":
                user = form.save(commit=False)
                user.is_active = False
                user.account_type = agency_account
                user.save()
                #agency = Agencie.objects.get(pk=int(request.POST['Select_Your_Agency']))

                #agent = Agencie.objects.create(duser=user.pk)
                #agent.email = user.email
                # agent.duser_id(2)
                #agent.phone = "0775682349"
                # agency = Agencie.objects.get(pk=int(request.POST['Select_Your_Agency']))
                # agent.agency=request.POST['Select_Your_Agency']
                #agent.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

                return redirect(emailactivate)


    else:
        form = SignupForm()
    return render(request, 'sign.html', {'form': form})

def home(request):
    if request.user.is_authenticated :
        if request.user.account_type == "agency":
            agency = Agencie.objects.filter(duser=request.user.pk).count()
            #return render(request, 'home.html', {})
            if agency == 0:
               return redirect(create_agency)
            else:
                user_list = Prop.objects.all().order_by('-date_added')
                # paginator = Paginator(user_list, 6)

                page = request.GET.get('page', 1)

                paginator = Paginator(user_list, 9)
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                user_new = Prop.objects.all().order_by('-date_added')
                # paginator = Paginator(user_list, 6)

                page = request.GET.get('page', 1)

                paginator = Paginator(user_new, 2)
                try:
                    users_n = paginator.page(page)
                except PageNotAnInteger:
                    users_n = paginator.page(1)
                except EmptyPage:
                    users_n = paginator.page(paginator.num_pages)
                return render(request, 'index-slider-horizontal-search-box.html',
                              {'users': users, 'user_n': users_n})
               #return render(request, 'index-slider-horizontal-search-box.html', {})

                #redirect(create_agency)
        else:
            user_list = Prop.objects.all().order_by('-date_added')
            # paginator = Paginator(user_list, 6)

            page = request.GET.get('page', 1)

            paginator = Paginator(user_list, 9)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            user_new = Prop.objects.all().order_by('-date_added')
            # paginator = Paginator(user_list, 6)

            page = request.GET.get('page', 1)

            paginator = Paginator(user_new, 2)
            try:
                users_n = paginator.page(page)
            except PageNotAnInteger:
                users_n = paginator.page(1)
            except EmptyPage:
                users_n = paginator.page(paginator.num_pages)
            return render(request, 'index-slider-horizontal-search-box.html',
                          {'users': users, 'user_n': users_n})
            #return render(request, 'index-slider-horizontal-search-box.html', {})

    else:

        user_list = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_list, 9)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        user_new = Prop.objects.all().order_by('-date_added')
        # paginator = Paginator(user_list, 6)

        page = request.GET.get('page', 1)

        paginator = Paginator(user_new, 2)
        try:
            users_n = paginator.page(page)
        except PageNotAnInteger:
            users_n = paginator.page(1)
        except EmptyPage:
            users_n = paginator.page(paginator.num_pages)
        return render(request, 'index-slider-horizontal-search-box.html',
                      {'users': users, 'user_n': users_n})
    #return render(request, 'home.html', {})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect(home)
    else:
        return HttpResponse('Activation link is invalid!')