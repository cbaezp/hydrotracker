from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import HydroponicGrowerForm, PlantForm, PlantInfoForm, SeedTrayForm
from .models import HydroponicGrower, Plant, PlantInfo, SeedTray


def test_view(request):
    return render(request, "dashboard/test.html")


@login_required
def seed_tray_list(request):
    seed_trays = SeedTray.objects.filter(user=request.user)
    return render(
        request, "dashboard/seed_tray/seed_tray_list.html", {"seed_trays": seed_trays}
    )


@login_required
def seed_tray_create(request):
    if request.method == "POST":
        form = SeedTrayForm(request.POST)
        if form.is_valid():
            seed_tray = form.save(commit=False)
            seed_tray.user = request.user
            seed_tray.save()
            messages.success(request, "Seed tray was successfully created!")
            return redirect("tracker:seed_tray_list")
    else:
        form = SeedTrayForm()
    return render(request, "dashboard/seed_tray/seed_tray_form.html", {"form": form})


@login_required
def seed_tray_edit(request, pk):
    seed_tray = get_object_or_404(SeedTray, pk=pk, user=request.user)
    if Plant.objects.filter(seed_tray=seed_tray).exists():
        messages.error(request, "Tray cannot be edited because it has plants. Empty your tray to edit.")
        return redirect("tracker:seed_tray_list")

    if request.method == "POST":
        form = SeedTrayForm(request.POST, instance=seed_tray)
        if form.is_valid():
            form.save()
            messages.success(request, "Seed tray was successfully updated!")
            return redirect("tracker:seed_tray_list")
    else:
        form = SeedTrayForm(instance=seed_tray)
    return render(request, "dashboard/seed_tray/seed_tray_form.html", {"form": form})


@login_required
def seed_tray_confirm_delete(request, pk):
    seed_tray = get_object_or_404(SeedTray, pk=pk, user=request.user)
    if request.method == "POST":
        seed_tray.delete()
        messages.success(request, "Seed tray was successfully deleted!")
        return redirect("tracker:seed_tray_list")
    return render(
        request,
        "dashboard/seed_tray/seed_tray_confirm_delete.html",
        {"seed_tray": seed_tray},
    )


# Hydroponic
@login_required
def hydroponic_grower_list(request):
    hydroponic_growers = HydroponicGrower.objects.filter(user=request.user)
    return render(
        request,
        "dashboard/hydroponic/hydroponic_grower_list.html",
        {"hydroponic_growers": hydroponic_growers},
    )


@login_required
def hydroponic_grower_create(request):
    if request.method == "POST":
        form = HydroponicGrowerForm(request.POST)
        if form.is_valid():
            hydroponic_grower = form.save(commit=False)
            hydroponic_grower.user = request.user
            hydroponic_grower.save()
            messages.success(request, "Hydroponic grower was successfully created!")
            return redirect("tracker:hydroponic_grower_list")
    else:
        form = HydroponicGrowerForm()
    return render(
        request, "dashboard/hydroponic/hydroponic_grower_form.html", {"form": form}
    )


@login_required
def hydroponic_grower_edit(request, pk):
    hydroponic_grower = get_object_or_404(HydroponicGrower, pk=pk, user=request.user)
    if Plant.objects.filter(hydroponic_grower=hydroponic_grower).exists():
        messages.error(
            request, "Hydroponic grower cannot be edited because it has plants."
        )
        return redirect("tracker:hydroponic_grower_list")

    if request.method == "POST":
        form = HydroponicGrowerForm(request.POST, instance=hydroponic_grower)
        if form.is_valid():
            form.save()
            messages.success(request, "Hydroponic grower was successfully updated!")
            return redirect("tracker:hydroponic_grower_list")
    else:
        form = HydroponicGrowerForm(instance=hydroponic_grower)
    return render(
        request, "dashboard/hydroponic/hydroponic_grower_form.html", {"form": form}
    )


@login_required
def hydroponic_grower_confirm_delete(request, pk):
    hydroponic_grower = get_object_or_404(HydroponicGrower, pk=pk, user=request.user)
    if request.method == "POST":
        hydroponic_grower.delete()
        messages.success(request, "Hydroponic grower was successfully deleted!")
        return redirect("tracker:hydroponic_grower_list")
    return render(
        request,
        "dashboard/hydroponic/hydroponic_grower_confirm_delete.html",
        {"hydroponic_grower": hydroponic_grower},
    )


# Plant Type
@login_required
def plant_info_list(request):
    plant_infos = PlantInfo.objects.filter(user=request.user)
    return render(
        request,
        "dashboard/plant_info/plant_info_list.html",
        {"plant_infos": plant_infos},
    )


@login_required
def plant_info_create(request):
    if request.method == "POST":
        form = PlantInfoForm(request.POST)
        if form.is_valid():
            plant_info = form.save(commit=False)
            plant_info.user = request.user
            plant_info.save()
            messages.success(request, "Plant info was successfully created!")
            return redirect("tracker:plant_info_list")
    else:
        form = PlantInfoForm()
    return render(request, "dashboard/plant_info/plant_info_form.html", {"form": form})


@login_required
def plant_info_edit(request, pk):
    plant_info = get_object_or_404(PlantInfo, pk=pk, user=request.user)
    if request.method == "POST":
        form = PlantInfoForm(request.POST, instance=plant_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Plant info was successfully updated!")
            return redirect("tracker:plant_info_list")
    else:
        form = PlantInfoForm(instance=plant_info)
    return render(request, "dashboard/plant_info/plant_info_form.html", {"form": form})


@login_required
def plant_info_confirm_delete(request, pk):
    plant_info = get_object_or_404(PlantInfo, pk=pk, user=request.user)
    if request.method == "POST":
        plant_info.delete()
        messages.success(request, "Plant info was successfully deleted!")
        return redirect("tracker:plant_info_list")
    return render(
        request,
        "dashboard/plant_info/plant_info_confirm_delete.html",
        {"plant_info": plant_info},
    )


# SeedTray Details


@login_required
def seed_tray_detail(request, pk):
    seed_tray = get_object_or_404(SeedTray, pk=pk, user=request.user)
    plants = Plant.objects.filter(seed_tray=seed_tray).select_related("plant_info")

    # Mapping plants to their positions, adjusting for zero indexing.
    positions = {
        (plant.position_x - 1, plant.position_y - 1): plant for plant in plants
    }

    # Create a grid representation of the tray
    grid = [[None for _ in range(seed_tray.x_size)] for _ in range(seed_tray.y_size)]
    for plant in plants:
        x = plant.position_x - 1  # Convert to 0-based index
        y = plant.position_y - 1  # Convert to 0-based index
        if 0 <= x < seed_tray.x_size and 0 <= y < seed_tray.y_size:
            grid[y][x] = plant

    return render(
        request,
        "dashboard/seed_tray/seed_tray_detail.html",
        {
            "seed_tray": seed_tray,
            "grid": grid,
        },
    )


@login_required
def plant_add(request, tray_id, pos_x, pos_y):
    seed_tray = get_object_or_404(SeedTray, pk=tray_id, user=request.user)

    # Convert the 1-based indices from the template to 0-based indices for internal use
    pos_x = int(pos_x) - 1
    pos_y = int(pos_y) - 1

    if request.method == "POST":
        form = PlantForm(request.POST, user=request.user)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.current_stage = "germination"
            plant.position_x = pos_x + 1  # Convert back to 1-based index for saving
            plant.position_y = pos_y + 1  # Convert back to 1-based index for saving
            plant.seed_tray = seed_tray
            plant.hydroponic_grower = None
            plant.save()
            return redirect("tracker:seed_tray_detail", pk=tray_id)
    else:
        form = PlantForm(
            initial={
                "seed_tray": seed_tray,
            },
            user=request.user,
        )

    return render(
        request,
        "dashboard/seed_tray/plant_add.html",
        {"form": form, "seed_tray": seed_tray},
    )


@login_required
def plant_edit(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id, user=request.user)
    seed_tray = plant.seed_tray
    if request.method == "POST":
        form = PlantForm(request.POST, instance=plant, user=request.user)
        if form.is_valid():
            # Update plant position if provided
            new_position_x = request.POST.get("position_x")
            new_position_y = request.POST.get("position_y")
            if new_position_x and new_position_y:
                plant.position_x = new_position_x
                plant.position_y = new_position_y
            plant.save()
            return redirect("tracker:seed_tray_detail", pk=seed_tray.pk)
    else:
        form = PlantForm(instance=plant, user=request.user)

    # Create a small representation of the tray
    grid = create_tray_representation(seed_tray, plant)

    return render(
        request,
        "dashboard/seed_tray/plant_edit.html",
        {
            "form": form,
            "seed_tray": seed_tray,
            "grid": grid,
            "plant": plant,
        },
    )


def create_tray_representation(seed_tray, current_plant):
    plants = (
        Plant.objects.filter(seed_tray=seed_tray)
        .exclude(pk=current_plant.pk)
        .select_related("plant_info")
    )

    # Create a dictionary of positions with plants
    positions = {(plant.position_x, plant.position_y): plant for plant in plants}

    # Create a grid representation of the tray
    grid = [[None for _ in range(seed_tray.x_size)] for _ in range(seed_tray.y_size)]

    # Fill the grid with plants, skipping the position of current_plant
    for x in range(1, seed_tray.x_size + 1):
        for y in range(1, seed_tray.y_size + 1):
            if (x, y) in positions:
                grid[y - 1][x - 1] = positions[(x, y)]
            elif (x, y) == (current_plant.position_x, current_plant.position_y):
                grid[y - 1][x - 1] = "current_plant"

    return grid


@login_required
def plant_delete_confirm(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    # Capture the ID of the seed tray before deletion
    seed_tray_id = plant.seed_tray_id
    if request.method == "POST":
        plant.delete()
        # Redirect to the seed tray detail view after deletion
        return redirect('tracker:seed_tray_detail', pk=seed_tray_id)
    # If it's a GET request, render the confirmation page
    return render(request, "dashboard/seed_tray/plant_delete_confirm.html", {"plant": plant})
