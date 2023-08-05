from typing import List, Dict, Union
from datetime import date, datetime
from .validators import *

class Types:

  validator: ChainedValidator

  def __init__(self, validator: ChainedValidator = ChainedValidator()):
    self.validator = validator

  @property
  def invalid(self):
    return Types(self.validator.append(Validator()))

  @property
  def str(self):
    return Types(self.validator.append(StrValidator()))

  def match(self, pattern):
    return Types(self.validator.append(MatchValidator(pattern)))

  def one_of(self, str_list):
    return Types(self.validator.append(OneOfValidator(str_list)))

  @property
  def int(self):
    return Types(self.validator.append(IntValidator()))

  @property
  def float(self):
    return Types(self.validator.append(FloatValidator()))

  def min(self, value: float):
    return Types(self.validator.append(MinValidator(value)))

  def max(self, value: float):
    return Types(self.validator.append(MaxValidator(value)))

  def range(self, min_value: float, max_value: float):
    return Types(self.validator.append(RangeValidator(min_value, max_value)))

  @property
  def bool(self):
    return Types(self.validator.append(BoolValidator()))

  @property
  def date(self):
    return Types(self.validator.append(DateValidator()))

  @property
  def datetime(self):
    return Types(self.validator.append(DatetimeValidator()))

  # @property
  # def list_of(self, types: Types):
  #   return Types(self.validator.append(ListOfValidator(types)))

  @property
  def required(self):
    return Types(self.validator.append(RequiredValidator()))

  # transformers

  def default(self, value):
    return Types(self.validator.append(DefaultValidator(value)))

  def truncate(self, max_length):
    return Types(self.validator.append(TruncateValidator(max_length)))

types = Types()
