from django.shortcuts import render
from django.shortcuts import get_object_or_404
from item.models import Item

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # related items
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {'item': item, 'related_items': related_items})