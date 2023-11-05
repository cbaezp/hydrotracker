from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [
    # SeedTray
    path("seedtrays/", views.seed_tray_list, name="seed_tray_list"),
    path("seedtrays/add/", views.seed_tray_create, name="seed_tray_create"),
    path("seedtrays/<int:pk>/edit/", views.seed_tray_edit, name="seed_tray_edit"),
    path(
        "seedtray/<int:pk>/confirm_delete/",
        views.seed_tray_confirm_delete,
        name="seed_tray_confirm_delete",
    ),
    # urls.py
    path("seedtrays/<int:pk>/", views.seed_tray_detail, name="seed_tray_detail"),
    path("hydroponic/", views.hydroponic_grower_list, name="hydroponic_grower_list"),
    path(
        "hydroponic/add/",
        views.hydroponic_grower_create,
        name="hydroponic_grower_create",
    ),
    path(
        "hydroponic/<int:pk>/edit/",
        views.hydroponic_grower_edit,
        name="hydroponic_grower_edit",
    ),
    path(
        "hydroponic/<int:pk>/delete/",
        views.hydroponic_grower_confirm_delete,
        name="hydroponic_grower_confirm_delete",
    ),
    path("plantinfo/", views.plant_info_list, name="plant_info_list"),
    path("plantinfo/add/", views.plant_info_create, name="plant_info_create"),
    path("plantinfo/<int:pk>/edit/", views.plant_info_edit, name="plant_info_edit"),
    path(
        "plantinfo/<int:pk>/confirm_delete/",
        views.plant_info_confirm_delete,
        name="plant_info_confirm_delete",
    ),
    path(
        "plant/add/<int:tray_id>/<int:pos_x>/<int:pos_y>/",
        views.plant_add,
        name="plant_add",
    ),
    path("plant/edit/<int:plant_id>/", views.plant_edit, name="plant_edit"),
    path(
        "plant/delete/confirm/<int:pk>/",
        views.plant_delete_confirm,
        name="plant_delete_confirm",
    ),
]
