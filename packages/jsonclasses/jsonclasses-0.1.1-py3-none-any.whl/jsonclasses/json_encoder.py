from json.encoder import JSONEncoder as OldAndGrayJSONEncoder
from .json_object import JSONObject

class JSONEncoder(OldAndGrayJSONEncoder):
  def default(self, o):
    if isinstance(o, JSONObject):
      return o.to_json()
    else:
      return super().default(o)
