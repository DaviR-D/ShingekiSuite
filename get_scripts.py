import requests
import re

def filter_scripts(node):
    if(node['url'].endswith(".js")):
        save_script(node['url'])
    
    if("childs" in node):
        for child_node in node["childs"]:
            filter_scripts(child_node)

def save_script(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error while downloading {url}")
        return

    if response.status_code == 200:
        formatted_url = re.sub(r'[^a-zA-Z0-9_.-]', '-', url)
        print(url)
        with open(f"output/{formatted_url}", "a", encoding="utf-8") as f:
            f.write(f"//{url}\n\n" + response.text)
