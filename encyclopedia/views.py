from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
from markdown2 import Markdown

entries = util.list_entries()

def index(request):
    value = None
    if request.method == "POST":
        value = request.POST.get("q")
        for entry in entries:
            if value.lower() == entry.lower():
                return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"name": entry}))
        
        # If no exact match, search for substring
        substring_matches = []
        for entry in entries:
            if value.lower() in entry.lower():
                substring_matches.append(entry)
        
        # Render search results page with matches
        return render(request, "encyclopedia/search_results.html", {
            "results": substring_matches,
            "query": value
        })
    return render(request, "encyclopedia/index.html", {
        "entries": entries, 
    })

def page(request, name):
    markdowner = Markdown()
    page_content = util.get_entry(name)
    if page_content == 'Error':
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/css.html", {
        "page": markdowner.convert(util.get_entry(name)), "name": name.capitalize(),
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
    
def edit(request, name):
    if request.method == "POST":
        editpage = request.POST.get("editpage")
        editpagedes = request.POST.get("editpagedes")
        for entry in entries:
            if entry.lower() == editpage.lower():
                util.save_entry(editpage, editpagedes)
                return HttpResponseRedirect(reverse('encyclopedia:page', kwargs={"name": editpage}))
    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "pagedes": util.get_entry(name)
    })

def randompage(request):
    markdowner = Markdown()
    ranpage = random.choice(entries)
    return render(request, "encyclopedia/css.html", {
        "page": markdowner.convert(util.get_entry(ranpage)),
        "name": ranpage
    })