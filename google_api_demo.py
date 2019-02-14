#Not using rest API because it's only free up to 100 searches per day

import requests
import re
test_query = "https://www.google.com/search?q=recipe+beef+onion+pizza+dough&btnI"
"Referer: http://www.google.com/"

headers = {"Referer": "http://www.google.com/"}
r = requests.get(test_query, headers=headers)

print(r.text)
