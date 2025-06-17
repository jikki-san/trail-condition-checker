from bs4 import BeautifulSoup
import requests


def find_trail(trail_name):
    def match_trail_name(tag):
        return tag.name == "tr" and tag.contents[0].text == trail_name
    return match_trail_name


def main():
    trail_name = "Skyline Trail"
    res = requests.get(
        "https://www.nps.gov/mora/planyourvisit/trails-and-backcountry-camp-conditions.htm")
    bs = BeautifulSoup(res.content, features="html.parser")
    row = bs.find("td", string=trail_name)
    row = row.next_sibling.next_sibling
    snow_cover_pct = row.text
    row = row.next_sibling.next_sibling
    trail_conditions = row.text
    row = row.next_sibling.next_sibling
    updated_at = row.text
    print(f"{trail_name}: {snow_cover_pct}% snow cover, {trail_conditions}. Last updated {updated_at}.")


if __name__ == "__main__":
    main()
