from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
import json
from datetime import datetime
from django.shortcuts import redirect

class MainView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news')

class NewsView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        n_link = kwargs['n_link']
        with open("news.json", "r") as json_file:
            newsy = json.load(json_file)
        for news in newsy:
            if news["link"] == int(n_link):
                context["news"] = news
                break
        return context

class NewsyView(TemplateView):
    template_name = 'news/newsy.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        query = request.GET.get('q')
        record = []
        with open("news.json", "r") as json_file:
            newsy = json.load(json_file)
        if query:
            for x in newsy:
                if query in x["title"]:
                    record.append(x)
        else:
            record = newsy
        czasy = list(set(str(datetime.strptime(x["created"], '%Y-%m-%d %H:%M:%S').date()) for x in record))
        czasy.sort(reverse=True)
        context["newsy"] = record
        context["czasy"] = czasy
        #return context
        return render(request, 'news/newsy.html', context=context)

class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        rekord = {}
        with open("news.json", "r+") as json_file:
            newsy = json.load(json_file)
            now = datetime.now()

            rekord["created"] = now.strftime('%Y-%m-%d %H:%M:%S')
            rekord["title"] = request.POST.get('title')
            rekord["text"] = request.POST.get('text')
            rekord["link"] = max([x["link"] for x in newsy]) + 1

            newsy.append(rekord)
            json_file.seek(0)
            json.dump(newsy, json_file)
        return redirect('/news')
