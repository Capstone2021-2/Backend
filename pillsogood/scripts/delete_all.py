from scripts import delete_ages, delete_age_nutrients, delete_nutrients, delete_nutrition_facts, delete_supplements, delete_organs, delete_main_nutrients, delete_brands, delete_good_for_organ

def run():
    delete_main_nutrients.run()
    delete_nutrition_facts.run()
    delete_age_nutrients.run()
    delete_good_for_organ.run()
    delete_brands.run()
    delete_ages.run()
    delete_organs.run()
    delete_nutrients.run()
    delete_supplements.run()