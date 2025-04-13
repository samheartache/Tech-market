from django.core.management import call_command

import os

fixture_path = input('Enter fixture path: ')
fx_model = input('Input model to be fixtured: ')

os.makedirs(os.path.dirname(fixture_path), exist_ok=True)


def load_data(fx_path, fx_model):
    with open(fx_path, "w", encoding="utf-8") as f:
        call_command("dumpdata", fx_model, indent=2, format="json", stdout=f)


load_data(fixture_path, fx_model)
