from django.contrib import admin

from .models import HydroponicGrower, Plant, PlantInfo, SeedTray


@admin.register(SeedTray)
class SeedTrayAdmin(admin.ModelAdmin):
    list_display = ("name", "x_size", "y_size", "user")
    search_fields = ("name", "user__username")
    list_filter = ("user",)


@admin.register(HydroponicGrower)
class HydroponicGrowerAdmin(admin.ModelAdmin):
    list_display = ("name", "x_size", "y_size", "orientation", "user")
    search_fields = ("name", "user__username")
    list_filter = (
        "orientation",
        "user",
    )


@admin.register(PlantInfo)
class PlantInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")
    list_filter = ("user",)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "plant_info",
        "n_seeds_used",
        "current_stage",
        "datetime_germination_to_growing",
        "datetime_growing_to_cropped",
        "user",
    )
    search_fields = ("plant_info__name", "current_stage", "user__username")
    list_filter = (
        "current_stage",
        "user",
    )
    raw_id_fields = ("plant_info", "seed_tray", "hydroponic_grower")

    # Optionally, to include fields for editing positions
    fields = (
        "plant_info",
        "n_seeds_used",
        "current_stage",
        "datetime_germination_to_growing",
        "datetime_growing_to_cropped",
        "position_x",
        "position_y",
        "seed_tray",
        "hydroponic_grower",
        "user",
    )

    # This function ensures that the admin queryset is limited to the user's own plants
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    # This function ensures that the user field is automatically populated with the current user when creating a plant
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # pk is None when the object is created
            obj.user = request.user
        super().save_model(request, obj, form, change)

    # Optionally, override get_form to customize the admin form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Customize the form as needed
        return form
