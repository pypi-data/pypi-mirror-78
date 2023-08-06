# This module overrides some sentitive data from weblate context

def override_version(request):
    return {"version": "Weblate",
            "weblate_link": "Weblate",
            "weblate_version_link": "Weblate",}
