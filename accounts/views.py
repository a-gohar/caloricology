from django.urls import reverse_lazy
from django.views import generic
from django.template import loader
from .forms import CustomUserCreationForm
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("dashboard")
    template_name = "registration/signup.html"