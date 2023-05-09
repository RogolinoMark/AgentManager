from django.urls import path
from .views import index, session_management, mode_management, feedback_management, AddObjective,AddApikey

urlpatterns = [
    path('', index, name="index"),
    path('session', session_management, name="session_management"),
    path('mode', mode_management, name="mode_management"),
    path('feedback', feedback_management, name="feedback"),
    path('objective', AddObjective, name="addobjective"),
    path('addapikey', AddApikey, name="addkey")
]
