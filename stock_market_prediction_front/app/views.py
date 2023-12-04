from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_http_methods
from .application.company_mapper import CompanyMapper
from .application.utils import GraphUtils
from .application.file_validator import FileValidator
from .forms.choose_company_form import ChooseCompanyForm
from .forms.profile_edit_form import EditProfileForm
from lstm_model.lstm_model import LSTMModel
from pathlib import Path
from datetime import datetime

import shutil
import os

# fixme
lstm_model_instance = LSTMModel('C:\\dev\\git\\inzynierka\\lstm_model\\saved_models\\model.keras')
company_mapper = CompanyMapper()


def home_page(request):
    if request.method == "GET":
        form = ChooseCompanyForm()
        selected_company = request.session.get('selected_company', 'APPLE')
        form.fields['company'].initial = selected_company
        return render(request, "home_page/index.html", {"choose_company_form": form})


def model_page(request):
    return render(request, "model/index.html")


def ai_model_prediction(request):
    selected_company = request.POST.get('company')
    request.session['selected_company'] = selected_company
    selected_company_ticker = company_mapper.map_name_to_ticker(selected_company)
    if request.session.get('model_type', 'lstm') == 'lstm':
        graph_prices = lstm_model_instance.predict_for_ticker(selected_company_ticker)
        GraphUtils.get_graph(graph_prices)
    elif request.session.get('model_type') == 'cnn':
        if os.path.exists("./stock_market_prediction_front/app/static/home_page/plots/plot.png"):
            os.remove("./stock_market_prediction_front/app/static/home_page/plots/plot.png")
        shutil.copyfile("./cnn/charts/" + selected_company_ticker + ".png", "./stock_market_prediction_front/app/static/home_page/plots/plot.png")
    return redirect("home-page")


@require_http_methods(["POST", "GET", "PUT"])
def ai_model(request):
    global lstm_model_instance
    # choose AI model type
    if request.method == "POST":
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
            if FileValidator().validate_file(file=train_file) == True:
                lstm_model_instance.train_model(train_file)
            print('to be implemented')
    # save AI model
    if request.method == 'GET':
        model_save_file_name = 'Downloads\\model_' + datetime.now().strftime('%Y-%m-%d') + '.keras'
        model_save_path = str(os.path.join(Path.home(), model_save_file_name))
        lstm_model_instance.save_model(model_save_path)
    return redirect('model-page')


def ai_model_upload(request):
    global lstm_model_instance
    if request.FILES['ai-model-upload-path']:
        uploaded_model = request.FILES['ai-model-upload-path']

        fs = FileSystemStorage()
        model_filename = fs.save(os.path.join('uploaded-models', uploaded_model.name), uploaded_model)
        lstm_model_instance = LSTMModel(model_filename)
    return redirect("model-page")


def profile(request):
    if request.method == "POST":
        #fixme
        print("do stuff")

    else:
        edit_profile_form = EditProfileForm()

    return render(request, "profile/index.html", {"edit_profile_form" : edit_profile_form})
