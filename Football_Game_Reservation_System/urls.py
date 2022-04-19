"""Football_Game_Reservation_System URL Configuration

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


from django.contrib import admin
from django.urls import path, include
from Reservation_App.views import (
    register,
    MainPageView,
    CreateSportPitchesView,
    CreateSportMatchesView,
    CityView,
    MatchDetails,
    DeleteListOfPlayer,
    DeleteMatch
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MainPageView.as_view(), name="index"),
    path("register/", register, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("city/<str:city>/pitchcreate", CreateSportPitchesView.as_view()),
    path("city/<str:city>/games", CreateSportMatchesView.as_view()),
    path("city/<str:city>", CityView.as_view(), name="cityview"),
    path("city/<str:city>/<int:sportmatches_id>", MatchDetails.as_view(), name="matchDetails"),
    path('removeplayerfromgame/<int:list_of_players_id>', DeleteListOfPlayer.as_view(), name="delete-from-list"),
    path('cancelmatch/<int:match_id>', DeleteMatch.as_view(), name="delete-match"),
]
