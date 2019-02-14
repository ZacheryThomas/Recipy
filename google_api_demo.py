#Not using rest API because it's only free up to 100 searches per day

import requests
import re
test_query = "https://www.google.com/search?q=recipe+beef+onion+pizza+dough"

r = requests.get(test_query)

debug = "http://www.a.com/"

result = re.search("(https?:\/\/(?!(www\..*google\.com\/?)).*?)(\")", r.text)

print(result.group(1))
