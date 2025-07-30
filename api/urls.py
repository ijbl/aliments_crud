from django.urls import path
from api.views import ListCreateAlimentView, RetrieveUpdateDeleteAlimentView

urlpatterns = [
    path("aliments/", ListCreateAlimentView.as_view(), name='aliments'),
    path("aliments/<int:id>", RetrieveUpdateDeleteAlimentView.as_view(), name='aliments_detail'),
]