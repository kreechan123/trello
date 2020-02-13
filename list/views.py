from django.shortcuts import render, get_object_or_404
from .models import Boardlist,Board, BoardMember, Card
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate
from .forms import LoginForm

# def dashboard_view(request):
#     boards = Board.objects.all()
#     return render(request,'list/dashboard.html',{'boards': boards})

# def list_view(request,pk):
#     blist = post = get_object_or_404(Boardlist, pk=pk)
#     return render(request,'list/list.html',{'blist': blist})
class LoginView(TemplateView):
    template_name = "list/login.html"
    # This mix in throws home if not logged in
    form = LoginForm

    def get(self, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return render(self.request, self.template_name,context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        username = self.request.POST.get['username']
        password = self.request.POST.get['password']
        user = authenticate(self.request, username = username, password = password)
        if form.is_valid():
            user = form.login()
            if user is not None:
                login(self.request, user)
                return render(self.request, self.template_name, {})
        context = {'form': form}
        return render(self.request, self.template, context)
            


class DashboardView(TemplateView):
    template = "list/dashboard.html"

    def get(self, *args, **kwargs):
        boards = Board.objects.all()
        return render(self.request, self.template, {})
        
