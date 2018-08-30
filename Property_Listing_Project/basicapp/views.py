from django.shortcuts import render

#from basicapp.models import User
from basicapp.forms import FormName

# Create your views here.
def index(request):
    return render(request, 'basicapp/index.html')

def form_name_view(request):
    form = FormName()

    if request.method == 'POST':
        form = FormName(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print('Error Form Invalid')
    return render(request,'Basicapp/login.html', {'form':form})

    #do something LANGUAGE_CODE

            # print("Validation Success!")
            # print(form.cleaned_data['name'])
            # print(form.cleaned_data['email'])
            # print(form.cleaned_data['text'])


    return render(request,'basicapp/login.html',{'form':form})
