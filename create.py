import json
import datetime
from datetime import datetime
newsy = [
  {
    "created": "2020-02-24 16:40:00",
    "text": "Kurde pijak.",
    "title": "Zazdroszcżę chłopu",
    "link": 123
  },
  {
    "created": "2020-02-25 16:40:00",
    "text": "A new star appeared in the sky.",
    "title": "The birth of the star",
    "link": 234
  },
  {
    "created": "2020-02-26 16:40:00",
    "text": "Małpa w lesie.",
    "title": "O żesz!",
    "link": 345
  },

]

with open("news.json", "w") as json_file:
    json.dump(newsy, json_file)


