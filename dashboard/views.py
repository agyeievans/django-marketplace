from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item
from django.contrib.auth.decorators import login_required

# Creating dashboard for user to view their items
@login_required
def index(request):
    # Get all items created by the user
    items = Item.objects.filter(created_by=request.user)
  
    return render(request, 'dashboard/index.html', {'items': items, })