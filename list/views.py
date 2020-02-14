from django.shortcuts import render, get_object_or_404, redirect
from .models import Boardlist,Board, BoardMember, Card
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm, CreateBoardForm
from .mixins import LoggedInAuthMixin
from django.http import HttpResponse, HttpResponseRedirect


class LoginView(LoggedInAuthMixin,TemplateView):
    template_name = 'list/login.html'
    form = LoginForm

    def get(self, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(self.request, username = username, password = password)
        if form.is_valid():
            if user is not None:
                login(self.request, user)
                return redirect('dashboard_view')
        context = {'form': form}
        return render(self.request, self.template_name, context)

class LogoutView(TemplateView):
    template_name = 'list/logout.html'

    def get(self, *arg, **kwargs):
        logout(self.request)
        return render(self.request, self.template_name)
    
class DashboardView(TemplateView):
    template_name = "list/dashboard.html"
    form = CreateBoardForm

    def get(self, *args, **kwargs):
        boards = Board.objects.all()
        form = CreateBoardForm()
        return render(self.request, self.template_name, {'boards': boards,'form':form})

    def post(self, *args, **kwargs):
        boards = Board.objects.all()
        if self.request.method == 'POST':
            form = CreateBoardForm(self.request.POST)
            if form.is_valid():
                add = form.save(commit=False)
                add.owner = self.request.user
                add.save()
                # return render(self.request, self.template_name, {'boards': boards, 'form':form})
                return HttpResponseRedirect("/")
        else:
            form = CreateBoardForm()

        return render(self.request, self.template_name, {'form':form})

class BoardlistView(TemplateView):
    template_name = "list/list.html"

    def get(self, *args, **kwargs):
        title = kwargs.get('title')
        blists = Boardlist.objects.filter(board__title=title)
        return render(self.request, self.template_name, {'blists': blists})
        