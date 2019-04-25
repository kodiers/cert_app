from model_mommy.recipe import Recipe, foreign_key, related

from certifications.models import Vendor, Certification, Exam


vendor_recipe = Recipe(Vendor, title='Test', description='Test')
certification_recipe = Recipe(Certification, title='Test', description='Test', number='test-1',
                              vendor=foreign_key(vendor_recipe))
exam_recipe = Recipe(Exam, title='Test', description='Test', number='test-1')
exam_with_certification = exam_recipe.extend(certification=related(certification_recipe))
