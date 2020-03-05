from django.shortcuts import render, get_object_or_404, redirect,Http404
from .models import Boardlist,Board, BoardMember, Card,User, BoardMember, Profile, Invite, CardComment
from django.utils import timezone, dateparse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timesince import timesince
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .mixins import BoardPermissionMixin
from django.contrib import messages

from .forms import LoginForm, CreateBoardForm, AddListForm, AddCardForm, RegisterForm
from django.core import serializers


# New Code Below
class LoginView(TemplateView):
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
                next_url = self.request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('dashboard')
        context = {'form': form}
        return render(self.request, self.template_name, context)
    

class RegisterView(TemplateView):
    template_name = 'board/register.html'

    def get(self, *args, **kwargs):
        form = RegisterForm(use_required_attribute=False)
        # import pdb; pdb.set_trace()
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = RegisterForm(self.request.POST)
        username = form.fields['username']
        # import pdb; pdb.set_trace()
        # if form.has_error(username, code=None):
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Registration Successful')
            # else:
            #     form = RegisterForm()
        
        return render(self.request, self.template_name, {})

class LogoutView(TemplateView):
    template_name = 'list/logout.html'

    def get(self, *arg, **kwargs):
        logout(self.request)
        return render(self.request, self.template_name)

class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'board/dashb.html'
    login_url = 'index'
    
    def get(self, *args, **kwargs):
        user = User.objects.get(username = self.request.user.username)
        boards = Board.objects.filter(owner = user)
        form = CreateBoardForm()
        return render(self.request, self.template_name, {'boards':boards, 'form': form})

    def post(self, *args, **kwargs):
        form = CreateBoardForm(self.request.POST)
        if form.is_valid():
            newboard = form.save(commit=False)
            newboard.owner = self.request.user
            newboard.save()

            serialized_object = serializers.serialize('json', [newboard,])
            return JsonResponse(serialized_object, safe=False)


class BoardDetailView(LoginRequiredMixin, BoardPermissionMixin, TemplateView):
    """ View for retreiving board detail 
    """
    template_name = 'board/detail.html'
    login_url = 'index'

    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get('id'))
        id=kwargs.get('id')
        form = AddListForm()
        members = BoardMember.objects.filter(board__id=id)
        users = User.objects.all()
        return render(self.request, self.template_name, {
            'board': board,
            'form':form,
            'members': members,
            'users' : users,
            }
            )

    def post(self, *args, **kwargs):
        id = kwargs.get('id')
        form = AddListForm(self.request.POST)
        board = self.request.POST.get('board')
        title = self.request.POST.get('title')
        board = Board.objects.get(id = board)
        obj = Boardlist.objects.filter(title = title, board = board)
        # import pdb; pdb.set_trace()
        if not obj:
            if form.is_valid():
                add = form.save(commit=False)
                add.board = Board.objects.get(id=id)
                add.save()
                serialized_object = serializers.serialize('json', [add,])
                return JsonResponse(serialized_object, safe=False)
        else:
            # return HttpResponseNotFound('<h1>Title already exist ;p</h1>')
            response = JsonResponse({"error": "Title already exist"})
            response.status_code = 403
            return response
            
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
        # import pdb; pdb.set_trace()
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
        cards = Card.objects.filter(board__id=list_id).order_by('position')
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

    def post(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        form = AddCardForm(self.request.POST)
       
        if form.is_valid():
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
        comment_lists = CardComment.objects.filter(card_id = card_id).order_by('-date_created')
        return render(self.request,self.template_name,{'card':card, 'comment_lists': comment_lists})

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
        position = self.request.POST.get('position')
        card_id = self.request.POST.get('card_id')

        card = Card.objects.get(id=card_id)
        newlist = self.request.POST.get('board')
        # import pdb; pdb.set_trace()
        card.position = position
        card.board_id = newlist
        card.save()
        return JsonResponse({})

class CardDescriptionView(View):

    def post(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        obj = Card.objects.get(id=card_id)
        desc = self.request.POST.get('description')
        obj.description = desc
        obj.save()
        return HttpResponse(desc)

class CardUploadView(View):
    
    def post(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        upload = self.request.FILES.get('file')
        card = Card.objects.get(id=card_id)
        card.image = upload 
        card.card_image_name = upload.name
        card.save()
        # import pdb; pdb.set_trace()
        return JsonResponse({'image_url': card.image.url, 'image_name': card.card_image_name, 'date_created': card.date_created}, safe=False)

class AddMemberView(View):

    def post(self, *args, **kwargs):
        board_id = kwargs.get('id')
        email = self.request.POST.get('email')
        queryset = User.objects.filter(email = email)
        board = Board.objects.get(id=board_id)
        invite = Invite.objects.create(
            email=email,
            board=board,
            invited_by=self.request.user
        )
        recipient = Invite.objects.filter(email = email)
        recipient = recipient.latest('date_invited')
        # send message
        recipient_email = recipient.email

        from_email = settings.EMAIL_HOST_USER
        subject, from_email, to = 'Board Invitation', from_email , recipient_email
        text_content = 'This is an important message.'
        html_content = render_to_string(
            'board/mail.html',
            {'token': recipient.token, 'request': self.request, 'board_id': board_id}
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return JsonResponse({"message":"Message Sent!"})

class UserConfirmationView(LoginRequiredMixin,TemplateView):
    template_name = 'board/userconfirm.html'
    login_url = 'index'

    def get(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        token = kwargs.get('token')
        board = Board.objects.get(id=board_id)

        confirm = Invite.objects.get(token = token)
        new_member = User.objects.get(email = confirm.email)
        confirm.is_confirmed = True
        confirm.save()
        BoardMember.objects.create(
            board = board,
            member = new_member
        )
        print("User Confirmation Success")

        if self.request.user.is_authenticated:
            return redirect('detail', id = board_id)
        else:
            return render(self.request, self.template_name, {})

class PostCommentView(LoginRequiredMixin, TemplateView):
    template_name = 'board/modalcard.html'
    login_url = 'index'
    
    def post(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        comment = self.request.POST.get('comment')
        card = Card.objects.get(id = card_id)
        obj = CardComment.objects.create(
            user = self.request.user,
            comment = comment,
            card = card
        )
        return JsonResponse({'id':obj.id, 'user':obj.user.username, 'comment': obj.comment, 'time':timesince(obj.date_created) })

class DeleteComment(View):

    def post(self, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = CardComment.objects.get(id = comment_id)
        comment.delete()
        return HttpResponse("deleted")

class BoardDelete(View):

    def post(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = Board.objects.get(id = board_id)
        board.delete()
        return HttpResponse("deleted")
