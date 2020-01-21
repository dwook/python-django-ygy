from django.shortcuts import render


def menus_list_view(request, restaurants_id, groups_id):
    return render(
        request,
        "menus/menus_list.html",
        {"restaurants_id": restaurants_id, "groups_id": groups_id},
    )

