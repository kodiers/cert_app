from django.contrib.auth.models import User

from model_mommy.recipe import Recipe


user_recipe = Recipe(User, email='test@test.com', username='test', first_name='Test', last_name='Test')

