from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import BiturlForm
from .models import BitURL
from event.models import ClickEvent
# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = BiturlForm()
        context = {
            'title': 'Bitly.co',
            'form': form
        }
        return render(request,'shortener/home.html', context)

    def post(self, request, *args, **kwargs):
        form = BiturlForm(request.POST) 
        template_name = 'shortener/home.html'
        context = {}
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            another_url = new_url
            # as the same method is implemented while overriding save method in model
            # when we implement this here, it will remove the error that is caused by the unqiue attribute of url property  
            if "http" not in new_url:
                another_url = "http://" + new_url  
            obj, created = BitURL.objects.get_or_create(url = another_url) 
            context.update({'object':obj, 'created': created})

            if created:
                template_name = 'shortener/created.html'
            else: 
                template_name = 'shortener/exists.html'
        return render(request, template_name , context)

class RedirectToURLView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        print("*"*10)
        qs = BitURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count()!=1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print("--------------", ClickEvent.objects.create_event(obj)) 
        return redirect(obj.url)