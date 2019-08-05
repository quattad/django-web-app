from mixer.backend.django import mixer
import pytest

"""
Mixer: Allows you to specify model to test without needing to specify all other attributes of model.
e.g. product = mixer.blend('<app_name>.<model_name>', '<property_to_fix>')

@pytest.mark.django_db decorator to ensure that test class has access to database
"""