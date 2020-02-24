from django.shortcuts import render, get_object_or_404, redirect,Http404
from .models import Boardlist,Board, BoardMember, Card
from django.utils import timezone
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .forms import LoginForm, CreateBoardForm, AddListForm, AddCardForm
from .mixins import LoggedInAuthMixin
from django.core import serializers


    
# class DashboardView(TemplateView):
#     template_name = "list/dashboard.html"
#     form = CreateBoardForm

#     def get(self, *args, **kwargs):
#         boards = Board.objects.all()
#         form = CreateBoardForm()
#         return render(self.request, self.template_name, {'boards': boards,'form':form})

#     def post(self, *args, **kwargs):
#         if self.request.method == 'POST':
#             form = CreateBoardForm(self.request.POST)
#             if form.is_valid():
#                 add = form.save(commit=False)
#                 add.owner = self.request.user
#                 add.save()
#                 return HttpResponseRedirect("/")
#         else:
#             form = CreateBoardForm()

#         return render(self.request, self.template_name, {'form':form})

# class BoardlistView(TemplateView):
#     template_name = "list/list.html"

#     def get(self, *args, **kwargs):
#         title = kwargs.get('title')
#         blists = Boardlist.objects.filter(board__title=title)
#         clists = Card.objects.all()
#         form = AddListForm()
#         return render(self.request, self.template_name, {'blists': blists, 'clists': clists, 'form': form})

#     def post(self, *args, **kwargs):
#         title = kwargs.get('title')
#         form = AddListForm(self.request.POST)
#         if form.is_valid():
#             add = form.save(commit=False)
#             add.board = Board.objects.get(title=title)
#             add.save()
#             return HttpResponseRedirect(self.request.path_info)
#         return render(self.request, self.template_name, {'form':form})


# class CardView(TemplateView):
#     template_name = "list/list.html"

#     def get(self, *args, **kwargs):
#         cards = Card.objects.all()
#         form = AddCardForm()
#         return render(self.request, self.template_name, {'cards': cards, 'form':form})

    # def post(self, *args, **kwargs):
    #     id = kwargs.get('list_id')
    #     form = AddCardForm(self.request.POST)
    #     if form.is_valid():
    #         add = form.save(commit=False)
    #         add.board = Card.objects.get(board__id=id)
    #         add.save()
    #         print('valid')
    #         return HttpResponseRedirect(self.request.path_info)
    #     return render(self.request, self.template_name, {'form':form})

# New Code Below
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
                # return redirect('dashboard')
        context = {'form': form}
        return render(self.request, self.template_name, context)

class LogoutView(TemplateView):
    template_name = 'list/logout.html'

    def get(self, *arg, **kwargs):
        logout(self.request)
        return render(self.request, self.template_name)

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
        form = AddListForm()
        return render(self.request, self.template_name, {'board': board, 'form':form})

    def post(self, *args, **kwargs):
        id = kwargs.get('id')
        form = AddListForm(self.request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.board = Board.objects.get(id=id)
            add.save()
            
            serialized_object = serializers.serialize('json', [add,])
            return JsonResponse(serialized_object, safe=False)
            
        return render(self.request, self.template_name, {'form':form,})
    

class BoardListView(TemplateView):
    """ View for retreiving the lists of Board lists
    """
    template_name = 'board/list.html'

    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get('id'))
        if not  self.request.is_ajax():
            raise Http404
        board_id = kwargs.get('id')
        lists = Boardlist.objects.filter(board__id=board_id)
        add_card_form = AddCardForm()
        return render(
            self.request, 
            self.template_name, 
            {
                'blists': lists, 
                'add_card_form': add_card_form
            }
        )
    

class CardListView(TemplateView):
    template_name = 'board/cardb.html'

    def get(self, *args, **kwargs):
        board_id = kwargs.get('board_id') #3
        list_id = kwargs.get('list_id') #1
        cards = Card.objects.filter(board__id=list_id)
        return render(self.request, self.template_name, {'cards':cards})

class DeleteList(TemplateView):
    template_name = 'board/list.html'

    def get(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        blist = get_object_or_404(Boardlist, id=list_id)
        blist.delete()
        return HttpResponse('/')

class AddCard(TemplateView):
    template_name = 'board/list.html'

    # def get(self,*args,**kwargs):
    #     form = AddCardForm()
    #     return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        form = AddCardForm(self.request.POST)
       
        if form.is_valid():
            # import pdb; pdb.set_trace()
            card = form.save(commit=False)
            card.board = Boardlist.objects.get(id=list_id)
            card.save()
            serialized_object = serializers.serialize('json', [card,])
            return JsonResponse(serialized_object, safe=False)
        return render(self.request, self.template_name, {'form':form})

class CardDetail(TemplateView):
    template_name = 'board/modalcard.html'

    def get(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card = get_object_or_404(Card, id=card_id)

        return render(self.request,self.template_name,{'card':card})

class DeleteCard(TemplateView):
    template_name = 'board/list.html'

    def get(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card = get_object_or_404(Card, id = card_id)
        card.delete()
        return HttpResponse('success')

class ListUpdateView(View):

    def post(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        lists = Boardlist.objects.get(id=list_id)
        title = self.request.POST.get('title')
        lists.title = title
        lists.save()
        return JsonResponse({'title': title})

class CardPositionView(View):

    def post(self, *args, **kwargs):
        list_id = kwargs.get('card_id')
        card = Card.objects.get(id=list_id) #152
        newlist = self.request.POST.get('board') #271
        card.board_id = newlist
        card.save()
        return JsonResponse({})
