# Author: Piotr Cieślak

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.http import FileResponse

from .application.company_mapper import CompanyMapper
from .application.utils import GraphUtils
from .application.file_validator import FileValidator

from .forms.choose_company_form import ChooseCompanyForm
from .forms.profile_edit_form import EditProfileForm
from .forms.login_form import LoginForm
from .forms.register_form import RegisterForm

from .models import Profile, Address

from lstm_model.lstm_model import LSTMModel

import shutil
import os
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, wait

# Train model on startup or, if exists, load compiled model
if os.path.exists(os.getcwd() + '\\models\\lstm\\model.keras'):
    lstm_model_instance = LSTMModel(os.getcwd() + '\\models\\lstm\\model.keras')
else:
    lstm_model_instance = LSTMModel('')
    lstm_model_instance.train_model('')
    lstm_model_instance.save_model(os.getcwd() + '\\models\\lstm\\model.keras')

company_mapper = CompanyMapper()

executor = ThreadPoolExecutor(max_workers=2)


@login_required
def home_page(request):
    context = {}
    ''' This function renders the home page of the website '''
    if request.method == "GET":
        form = ChooseCompanyForm()
        ''' Set "APPLE" as the default company for predicting prices, or if chosen, set "selected_company" ticker '''
        selected_company = request.session.get('selected_company', 'apple')
        form.fields['company'].initial = selected_company
        context.update({'choose_company_form': form})

        ''' Get the maximum and minimum price for a company from yahoo finance'''
        selected_company_ticker = company_mapper.map_name_to_ticker(selected_company)
        selected_company_inst = yf.Ticker(selected_company_ticker)
        selected_company_info = selected_company_inst.basic_info

        context.update({'company': selected_company})
        context.update({'ticker': selected_company_ticker})
        context.update({'max_price': selected_company_info.year_high})
        context.update({'min_price': selected_company_info.year_low})
        context.update({'shares': selected_company_info.shares})

        return render(request, "home_page/index.html", context)


@login_required
def model_page(request):
    if request.session.get('show_success_training_message'):
        messages.success(request, "Model training finished")
        request.session['show_success_training_message'] = False
    return render(request, "model/index.html")


@login_required
def ai_model_prediction(request):
    ''' This function triggers AI model prediction and generates the graph '''

    ''' Get the selected_company name '''
    selected_company = request.POST.get('company')
    request.session['selected_company'] = selected_company

    ''' Map the name to a company ticker '''
    selected_company_ticker = company_mapper.map_name_to_ticker(selected_company)

    ''' Get the AI model to make predictions. Default is LSTM '''
    if request.session.get('model_type', 'lstm') == 'lstm':
        ''' Get prediction '''
        graph_prices = lstm_model_instance.predict_for_ticker(selected_company_ticker)
        GraphUtils.get_graph(graph_prices, lstm_model_instance.INPUT_DAYS,
                             lstm_model_instance.OUTPUT_DAYS)
    elif request.session.get('model_type') == 'cnn':
        if os.path.exists("./stock_market_prediction_front/app/static/home_page/plots/plot.png"):
            os.remove("./stock_market_prediction_front/app/static/home_page/plots/plot.png")
        shutil.copyfile("../cnn/charts/" + selected_company_ticker + ".png", "app/static/home_page/plots/plot.png")

    return redirect("home-page")


@login_required
@require_http_methods(["POST", "GET", "PUT"])
def ai_model(request):
    ''' This function modifies the working AI model instance '''
    global lstm_model_instance

    # choose AI model type
    if request.method == "POST":
        ''' Set the new model_type and train_file '''
        model_type = request.POST['model-type']
        train_file = request.FILES.get('train-data', None)
        if model_type == 'LSTM Model':
            request.session['model_type'] = 'lstm'
        elif model_type == 'CNN Model':
            request.session['model_type'] = 'cnn'
        if train_file is not None:
            # fixme
            # validate train_file
            # asynchronically train model
            ''' Train the model with a provided train_file '''
            if FileValidator().validate_file(file=train_file) == True:
                lstm_model_instance = LSTMModel('')
                futures = []
                futures.append(executor.submit(async_train_model, request, train_file))
                completed, pending = wait(futures)
    # save AI model
    if request.method == 'GET':
        ''' Save the AI model to the desktop '''
        lstm_model_instance.save_model(os.getcwd() + '\\download\\model.keras')
        lstm_model_download_file = open(
            os.getcwd() + '\\download\\model.keras', 'rb')
        return FileResponse(lstm_model_download_file, as_attachment=True, filename='model.keras')

    if request.session.get('show_success_training_message'):
        messages.success(request, "Model training finished")
        request.session['show_success_training_message'] = False

    return redirect('model-page')


@login_required
def ai_model_upload(request):
    ''' This function is used for uploading a saved AI model to the website '''

    global lstm_model_instance
    if request.FILES['ai-model-upload-path']:
        uploaded_model = request.FILES['ai-model-upload-path']

        fs = FileSystemStorage()
        model_filename = fs.save(os.path.join('uploaded-models', uploaded_model.name), uploaded_model)
        lstm_model_instance = LSTMModel(model_filename)
    return redirect("model-page")


@login_required
def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__email=request.user.email)

    if request.method == "POST":
        edit_profile_form = EditProfileForm(request.POST)
        if edit_profile_form.is_valid():
            profile.phone_number = edit_profile_form.cleaned_data.get('phone_number')
            profile.address.city = edit_profile_form.cleaned_data.get('city')
            profile.address.street = edit_profile_form.cleaned_data.get('street')
            profile.address.postal_code = edit_profile_form.cleaned_data.get('postal_code')
            profile.save()
    else:
        edit_profile_form = EditProfileForm()
        if request.user.is_authenticated:
            edit_profile_form.set_fields(profile)

    return render(request, "profile/index.html", {"edit_profile_form": edit_profile_form})


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=email, email=email, password=password)
            if not user:
                login_form.set_wrong_credentials_error()
                return render(request, "login/index.html", {"login_form": login_form}, status=403)
            else:
                django_login(request, user)
                return redirect('home-page')

    else:
        login_form = LoginForm();

    return render(request, "login/index.html", {"login_form": login_form})


@transaction.atomic
def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():

        # Initialize a Django User model for authentication
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            user = User.objects.create_user(username=email, email=email, password=password)
        # user.save()

        # Initialize inner Address model
            city = register_form.cleaned_data.get('city')
            street = register_form.cleaned_data.get('street')
            postal_code = register_form.cleaned_data.get('postal_code')
            address = Address.objects.create(city=city, street=street, postal_code=postal_code)

        # Initialize inner Profile model
            phone_number = register_form.cleaned_data.get('phone_number')
            profile = Profile.objects.create(user=user, address=address, phone_number=phone_number)

            profile.save()

            user = authenticate(username=email, email=email, password=password)
            django_login(request, user)
            return redirect('home-page')
        return render(request, "register/index.html", {"register_form": register_form}, status=400)

    else:
        register_form = RegisterForm();

    return render(request, "register/index.html", {"register_form": register_form})

def async_train_model(request, train_file):
    lstm_model_instance.train_model(train_file)
    request.session['show_success_training_message'] = True
