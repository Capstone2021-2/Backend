from pillsogood.scripts import delete_good_for_organ
from scripts import delete_ages, delete_age_nutrients, delete_nutrients, delete_nutrition_facts, delete_supplements

def run():
    delete_ages.run()
    delete_age_nutrients.run()
    delete_nutrition_facts.run()
    delete_supplements.run()
    delete_nutrients.run()
    delete_good_for_organ.run()