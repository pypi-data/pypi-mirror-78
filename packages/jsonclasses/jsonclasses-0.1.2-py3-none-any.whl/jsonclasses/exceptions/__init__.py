from typing import List, Dict, Any

class ValidationException(Exception):

  keypath_messages: Dict[str, str] = {}
  root: Any

  def __init__(self, keypath_messages: Dict[str, str], root: Any):
    self.keypath_messages = keypath_messages
    self.message = self.formatted_keypath_messages()
    self.root = root
    super().__init__(self.message)

  def formatted_keypath_messages(self):
    retval = 'Json classes validation failed:\n'
    for k, v in self.keypath_messages.items():
      retval += f'  \'{k}\': {v}\n'
    return retval
