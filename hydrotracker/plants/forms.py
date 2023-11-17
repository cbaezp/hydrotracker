from django import forms

from .models import HydroponicGrower, Plant, PlantInfo, SeedTray


class SeedTrayForm(forms.ModelForm):
    class Meta:
        model = SeedTray
        fields = ["name", "x_size", "y_size"]


class HydroponicGrowerForm(forms.ModelForm):
    class Meta:
        model = HydroponicGrower
        fields = ["name", "x_size", "y_size"]


class PlantInfoForm(forms.ModelForm):
    class Meta:
        model = PlantInfo
        fields = ["name", "notes"]


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["plant_info", "n_seeds_used"]
        widgets = {
            "plant_info": forms.Select(attrs={"class": "form-control"}),
            "n_seeds_used": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PlantForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["plant_info"].queryset = PlantInfo.objects.filter(user=user)


class HydroponicPlantUpdateForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["current_stage"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(HydroponicPlantUpdateForm, self).__init__(*args, **kwargs)
        self.fields["current_stage"].choices = [
            (choice[0], choice[1]) for choice in self.instance.STAGE_CHOICES if choice[0] in ["growing", "cropped"]
        ]

    def save(self, commit=True):
        plant = super(HydroponicPlantUpdateForm, self).save(commit=False)
        # Custom save logic here if needed
        if commit:
            plant.save()
        return plant
