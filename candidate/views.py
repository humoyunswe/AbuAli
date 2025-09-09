from django.shortcuts import render
from .forms import CandadiateForm
from .models import Candidates
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.


def contact_to_us(request):
    return render(request, 'candidate/contact_to_us.html')



def joing_to_us(request):
    if request.method == 'POST':
        form = CandadiateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your application! \n We will contact you soon.')
            return redirect('contact_to_us')
    else:
        form = CandadiateForm()
    return render(request, 'candidate/joing_to_us.html', {'form': form})