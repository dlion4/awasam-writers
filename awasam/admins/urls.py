from django.urls import path, include


from . import views

app_name = "admins"

urlpatterns = [
    path("", view=views.admin_home_view, name="home"),
    path("orders/", view=views.admin_orders_view, name="admin_orders_view"),
    path("orders/<pk>/<normal_order_slug>/approve/", view=views.admin_orders_mark_approved_view, name="mark_normal_approved_order_view"),
    path("courses/", view=views.AdminCoursesListView.as_view(), name="admin_courses_view"),
    path("orders/approve/<int:pk>/<file_type>/<path:file_name>/", view=views.serve_file, name="admin_approve_order_view"),
]
