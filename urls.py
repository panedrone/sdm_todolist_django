"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from django.views.generic import TemplateView

from views import GroupListView, GroupView, GroupTasksView, TaskView

# router = routers.DefaultRouter()
# router.register(r'groups', GroupViewSet, basename="groups")
# router.register(r'groups', Tas)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # https://stackoverflow.com/questions/1123898/django-static-page
    path('', TemplateView.as_view(template_name='static/index.html'), name='home'),
    # path('', include(router.urls)),
    path('groups', GroupListView.as_view()),
    # https://stackoverflow.com/questions/47661536/django-2-0-path-error-2-0-w001-has-a-route-that-contains-p-begins-wit
    path('groups/<int:g_id>', GroupView.as_view()),
    path('groups/<int:g_id>/tasks', GroupTasksView.as_view()),
    path('tasks/<int:t_id>', TaskView.as_view())
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
