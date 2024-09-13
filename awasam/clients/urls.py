from django.urls import path, include


from . import views

app_name = "clients"

urlpatterns = [
    path("", view=views.client_home_view, name="home"),
    path("account/", view=views.client_dashboard_account, name="account"),
    path("add-order/", view=views.client_add_order_view, name="add_order"),
    path("add-exam-order/", view=views.client_add_exam_order_view, name="add_exam_order"),
    path("add-course-order/", view=views.client_add_course_order_view, name="add_course_order"),
    path("courses/", view=views.CoursesListView.as_view(), name="courses_list_view"),
    path("customer-rules/", view=views.recommendation_view, name="recommendation_view"),
    path("orders/", include("awasam.orders.urls", namespace="orders")),
    
    # Order payment
]
