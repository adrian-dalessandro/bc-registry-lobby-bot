import urllib3
from bs4 import BeautifulSoup
import re

def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None

def poll_registry():
    registry_url = "https://www.lobbyistsregistrar.bc.ca/app/secure/orl/lrs/do/rcntCmLgs?rt=1&pg=1"

    http = urllib3.PoolManager()
    resp = http.request("GET", registry_url)
    soup = BeautifulSoup(resp.data, 'html.parser')
    return parse_registry(soup)

def parse_registry(soup):
    tags = ["Lobbyists who performed the lobbying activity:", "Lobbying Activity date:", "Posted date:", "Lobbying Activity number:"]
    result_list = []
    for registry_elem in soup.find("div", {"class": "panel panel-primary"}).find("ul", {"class": "list-group"}).findAll("li", {"class": "list-group-item"}):
        result = {"organization": None, "officials": [], "lobbying_date": None, "posted_date": None, "lobbyists": None, "lobby_activity_id": None}
        for official in registry_elem.find("ul").findAll("li"):
            official = official.text.replace("\n", "")
            name, title, affiliation = [s.strip() for s in re.split(",|\\|", re.sub(" +", " ", official), maxsplit=2)]
            result["officials"].append({"name": name, "title": title, "affiliation": affiliation})

        lines = re.sub(" +", " ", registry_elem.text).split("\n")
        lines = [l.strip() for l in lines if len(l) > 1]
        result["organization"] = lines[0]
        for key, tag in zip(["lobbyists", "lobbying_date", "posted_date", "lobby_activity_id"], tags):
            index = find_element_in_list(tag, lines)
            if index != None:
                result[key] = lines[index+1]
        result_list.append(result)
    return result_list
