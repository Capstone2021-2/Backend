from scripts import add_body_types
from scripts import add_brands
from scripts import add_age_nutrients, add_ages, add_nutrients, add_nutrition_facts, add_supplements
from scripts import add_organs, add_main_nutrients, add_good_for_organ

def run():
    add_ages.run()
    add_age_nutrients.run()
    add_nutrients.run()
    add_supplements.run()
    add_nutrition_facts.run()
    add_good_for_organ.run()
    add_organs.run()
    add_main_nutrients.run()
    add_brands.run()
    add_body_types.run()