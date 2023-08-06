from typing import Union
from ..exceptions import ValidationException
from .validator import Validator

class MinlengthValidator(Validator):

  def __init__(self, minlength: int):
    self.minlength = minlength

  def validate(self, value, key_path, root, all_fields):
    if value is not None and len(value) < self.minlength:
      raise ValidationException(
        { key_path: f'Length of value \'{value}\' at \'{key_path}\' should not be less than {self.minlength}.' },
        root
      )
