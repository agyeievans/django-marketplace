from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from item.models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
# to search items in description
from django.db.models import Q

# search items
def items(request):
    # get search query
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    # get all categories
    categories = Category.objects.all()
    # check if item is sold
    items = Item.objects.filter(is_sold=False)

    # filter items by category
    if category_id:
        items = items.filter(category_id=category_id)

    #  filter items by name and description
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {'items': items, 'query': query, 'categories': categories, 'category_id': int(category_id)})

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # related items
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {'item': item, 'related_items': related_items})


# check if user is logged in
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        
    return render(request, 'item/form.html', {'form': form, 'title': 'New Item',})

# delete item
@login_required
def delete(request, pk):
    # Get item with pk and created_by=request.user
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
        
    return render(request, 'item/form.html', {'form': form, 'title': 'Edit Item',})