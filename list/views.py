from django.shortcuts import render, get_object_or_404, redirect,Http404
from .models import Boardlist,Board, BoardMember, Card
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect

from .forms import LoginForm, CreateBoardForm, AddListForm, AddCardForm
from .mixins import LoggedInAuthMixin


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
        if self.request.method == 'POST':
            form = CreateBoardForm(self.request.POST)
            if form.is_valid():
                add = form.save(commit=False)
                add.owner = self.request.user
                add.save()
                return HttpResponseRedirect("/")
        else:
            form = CreateBoardForm()

        return render(self.request, self.template_name, {'form':form})

class BoardlistView(TemplateView):
    template_name = "list/list.html"

    def get(self, *args, **kwargs):
        title = kwargs.get('title')
        blists = Boardlist.objects.filter(board__title=title)
        clists = Card.objects.all()
        form = AddListForm()
        return render(self.request, self.template_name, {'blists': blists, 'clists': clists, 'form': form})

    def post(self, *args, **kwargs):
        title = kwargs.get('title')
        form = AddListForm(self.request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.board = Board.objects.get(title=title)
            add.save()
            return HttpResponseRedirect(self.request.path_info)
        return render(self.request, self.template_name, {'form':form})


class CardView(TemplateView):
    template_name = "list/list.html"

    def get(self, *args, **kwargs):
        cards = Card.objects.all()
        form = AddCardForm()
        return render(self.request, self.template_name, {'cards': cards, 'form':form})

    def get_card(self, *args, **kwargs):
        print("ini")
        form = AddCardForm(self.request.POST, prefix='addcard')
        if form.is_valid():
            add = form.save(commit=False)
            add.board = Boardlist.objects.get(title=q)
            add.save()
            print('valid')
            return HttpResponseRedirect(self.request.path_info)
        return render(self.request, self.template_name, {'form':form})



class DashBoardView(TemplateView):
    template_name = 'board/dashb.html'
    
    def get(self, *args, **kwargs):
        boards = Board.objects.all()
        return render(self.request, self.template_name, {'boards':boards})

class BoardDetailView(TemplateView):
    """ View for retreiving board detail 
    """
    template_name = 'board/detail.html'

    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get('id'))
        return render(self.request, self.template_name, {'board': board})

class BoardListView(TemplateView):
    """ View for retreiving the lists of Board lists
    """
    template_name = 'board/list.html'

    def get(self, *args, **kwargs):
        # board = get_object_or_404(Board, id=kwargs.get('id'))
        # if not  self.request.is_ajax():
        #     raise Http404
        board_id = kwargs.get('id')
        lists = Boardlist.objects.filter(board__id=board_id)
        return render(self.request, self.template_name, {'blists': lists})

class CardDetail(TemplateView):
    template_name = 'board/cardb.html'

    def get(self, *args, **kwargs):
        board_id = kwargs.get('board_id') #3
        list_id = kwargs.get('list_id') #1
        cards = Card.objects.filter(board__id=list_id)
        return render(self.request, self.template_name, {'cards':cards})