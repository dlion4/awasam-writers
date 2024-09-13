from django.urls import path


from . import views

app_name = "writers"

urlpatterns = [
    path("", view=views.writer_home_view, name="home"),
    path("account/", view=views.writer_dashboard_account, name="account"),
    path("orders/", view=views.WriterOrdersListView.as_view(), name="writer_orders_view"),
    path("orders/normal/<pk>/<normal_order_slug>/", view=views.WriterNormalOrderDetailView.as_view(), name="normal_order_detail_view"),
    path("orders/course/<pk>/<course_order_slug>/", view=views.WriterCourseOrderDetailView.as_view(), name="course_order_detail_view"),
]
