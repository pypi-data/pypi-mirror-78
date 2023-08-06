from bunny_lab.names import get_random_name

HTML_HEADER = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Bunny lab results</title>

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
"""

HTML_FOOTER = """
</body>
</html>
"""


class BunnyLab:

    def __init__(self):
        self.results = {}

    def register_user(self):
        name = get_random_name()
        while (name in self.results.keys()):
            name = get_random_name()

        self.results[name] = 0
        return name

    def unregister_user(self, name):
        print("deregistered", name)
        self.results.pop(name)

    def bunnies_saved(self, user, number):
        self.results[user] += number
        return self.results[user]

    def bunny_saved(self, user):
        self.results[user] += 1
        return self.results[user]

    def print_results(self, full_html=True):
        result = ""
        if full_html:
            result += HTML_HEADER

        result += "<table>\n"
        result += "<th> Player name </th> <th> Saved bunnies </th>"
        key_list = list(self.results.keys())
        keys_sorted = sorted(key_list, key=lambda k: self.results[k], reverse=True)
        for k in keys_sorted:
            result += f"<tr><td>{k}</td><td>{self.results[k]}</td></tr>"
        result += "</table>"

        if full_html:
            result += HTML_FOOTER

        return result

