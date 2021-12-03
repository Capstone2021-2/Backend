from scripts import delete_good_for_life_styles
from scripts import delete_body_types, delete_life_styles
from scripts import delete_ages, delete_age_nutrients
from scripts import delete_nutrients, delete_nutrition_facts
from scripts import delete_supplements, delete_organs, delete_cautions
from scripts import delete_main_nutrients, delete_brands, delete_good_for_organ
from scripts import delete_good_for_age, delet_good_for_

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
    delete_brands.run()
    delete_body_types.run()
    delete_life_styles.run()
    delete_good_for_life_styles.run()
    delete_cautions.run()
    delete_good_for_age.run()