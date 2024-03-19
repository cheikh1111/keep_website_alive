from bs4 import BeautifulSoup
import requests
import random
import time
import os

uas_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "user_agents.txt"))
websites = {
    "https://vote-app-6owd.onrender.com/": "https://api.render.com/deploy/srv-cns9ainjbltc739obg60?key=gOB8ywpivu8",
    "https://vote-app-1.onrender.com": "https://api.render.com/deploy/srv-cnsrfhnjbltc73d5af8g?key=9pMU2rivPEw",
    "https://vote-app-2.onrender.com": "https://api.render.com/deploy/srv-cnsrgrf79t8c73a84lh0?key=NRcYguwn4jQ",
    "https://vote-app-3.onrender.com": "https://api.render.com/deploy/srv-cnsrkcgcmk4c73eqgha0?key=q0FCJqvS5Cw",
}


def save_uas(lst):
    with open(uas_path, "a") as f:
        for ua in lst:
            f.write(ua)
            f.write("\n")


def getUaslist():
    lst = [
        "Firefox",
        "Internet+Explorer",
        "Opera",
        "Safari",
        "Chrome",
        "Edge",
        "Android+Webkit+Browser",
    ]
    for browser in lst:
        url = "http://www.useragentstring.com/pages/useragentstring.php?name=" + browser
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
        else:
            soup = False
        if soup:
            user_agents = []
            lst = soup.find("div", {"id": "liste"})
            links = lst.findAll("a")
            for link in links:
                user_agents.append(link.text)
            save_uas(user_agents)
        else:
            print(f"No user agents parsed for {browser}")


def load_uas():
    with open(uas_path, "r") as f:
        return f.readlines()


if not os.path.exists(uas_path):
    print("Scraping user agent list")
    getUaslist()

uas_list = load_uas()


def send_request():
    # Replace with your target URL
    headers = {"User-Agent": random.choice(uas_list).strip()}
    for website in websites:
        try:
            res = requests.get(website, headers=headers)
            if res.status_code == 200:
                print("Request successful")
            else:
                print(f"Request failed with status code {res.status_code}")
                print(f"Triggering the auto deploy: ")
                res = requests.get(websites[website])
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    while True:
        send_request()
        time.sleep(500)
