from typing import Any
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from awasam.orders.models import Normal, NormalOrderCompleted


# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/home.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    def post(self, request:HttpRequest, *args: Any, **kwargs: Any):
        return JsonResponse({"message": "success"})
# Create your views here.
class AboutView(TemplateView):
    template_name = "pages/about.html"
    
class ContactView(TemplateView):
    template_name = "pages/contact.html"
    
class PricingView(TemplateView):
    template_name = "pages/pricing.html"
    
    
class TestimonialView(TemplateView):
    template_name = "pages/testimonials.html"
    
    
class FrequentlyAskedQuestionsView(TemplateView):
    template_name = "pages/faqs.html"
    
    
class SampleOrderView(TemplateView):
    template_name = "pages/samples.html"
    queryset = NormalOrderCompleted.objects.prefetch_related("writer", "normal_order").filter(approved=True)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["sample_orders"] = self.queryset[:10]
        return context
    
    