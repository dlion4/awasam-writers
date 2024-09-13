from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('testimonials/', views.TestimonialView.as_view(), name='testimonials'),
    path('frequently-asked-questions/', views.FrequentlyAskedQuestionsView.as_view(), name='faqs'),
    path("samples/", views.SampleOrderView.as_view(), name="sample_orders"),
]