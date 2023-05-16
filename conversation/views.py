from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # get all conversations connected to the item
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # check if the conversation already exists and redirect to the conversation detail
    if conversations.exists():
        return redirect('conversation:detail', pk=conversations.first().id)

    # check if form is submitted
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        # check if form is valid
        if form.is_valid():
            # create a new conversation
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # create a new message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
        else:
            form = ConversationMessageForm()

    form = ConversationMessageForm()
    

    return render(request, 'conversation/new.html', {'form': form})

# fetch all conversations connected to the user
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'conversation/inbox.html', {'conversations': conversations})

# get the conversation detail
@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    # check if form is submitted
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        # check if form is valid
        if form.is_valid():
            # create a new message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()
            return redirect('conversation:detail', pk=pk)
        else:
            form = ConversationMessageForm()

    form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {'conversation': conversation, 'form': form})
