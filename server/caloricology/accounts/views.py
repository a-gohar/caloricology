from django.urls import reverse_lazy
from django.views import generic
from django.template import loader
from .forms import UserCreationForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("dashboard")
    template_name = "registration/signup.html"