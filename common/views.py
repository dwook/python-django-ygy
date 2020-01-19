from django.shortcuts import render
from django.views.generic import View, TemplateView
from groups import models as group_models


class HomeView(TemplateView):
    template_name = "home/home.html"


"""
def home_view(request):
    return render(request, "home/home.html")
"""

"""
class HomeView(View):
    def get(self, *args, **kwargs):
        groups = group_models.Group.objects.all()
        return render(self.request, "home/home.html", {"groups": groups})

"""
