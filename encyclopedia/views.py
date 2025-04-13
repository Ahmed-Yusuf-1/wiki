from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
entries = util.list_entries()

def index(request):
    value = None
   
    if request.method == "POST":
        value = request.POST.get("q")
        print(entries)
        for entry in entries:
            if value.lower() == entry.lower():
                return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"name": value}))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
    })

def page(request, name):
    return render(request, "encyclopedia/css.html", {
        "page": util.get_entry(name), "name": name.capitalize(),
    })

def create(request):
    if request.method == "POST":
        page = request.POST.get("addpage")
        pagedes = request.POST.get("addpagedes")
        for entry in entries:
            if page.lower() == entry.lower():
                return render(request, "encyclopedia/error.html")
        util.save_entry(page, pagedes)
        return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"name": page}))
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request, page):
    return render(request, "encyclopedia/edit.html", {
        "editpage": page
    })