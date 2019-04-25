from model_mommy.recipe import Recipe, foreign_key

from people.tests.recipes import user_recipe
from certifications.tests.recipes import certification_recipe, exam_with_certification

from cert_remainder.models import UserCertification, UserExam


user_certification_recipe = Recipe(UserCertification, user=foreign_key(user_recipe),
                                   certification=foreign_key(certification_recipe))
user_exam_recipe = Recipe(UserExam, user=foreign_key(user_recipe),
                          user_certification=foreign_key(user_certification_recipe),
                          exam=foreign_key(exam_with_certification))
