from urllib.parse import urlparse, urljoin
import requests
import re
from url_tree_handler import find_node_by_url

def crawl(url, cookies, url_tree, domain=""):
    child_urls = list()
    print()
    print("---------------------Root URL:---------------------")
    print(url)
    print("---------------------------------------------------")
    print()

    try:
        response = requests.get(url, cookies=cookies, timeout=10)
    except requests.exceptions.TooManyRedirects:
        print(f"URL {url} got into redirect loop, continuing to the next...")
        return child_urls


    links = re.findall(r'(?:href|src)="(.*?)"', response.text)

    links = list(set(links))

    for link in links:
        split_url = link.split("?", 1)
        child_url = split_url[0]

        parsed = urlparse(child_url)

        if parsed.scheme not in ("http", "https", ""):
            continue 

        if not parsed.scheme:
            child_url = urljoin(url, child_url)

        child_url = child_url.rstrip("/")

        query_params = split_url[1].split("&") if len(split_url) > 1 else []

        existing_node = find_node_by_url(url=child_url, node=url_tree)

        if(existing_node is not None):
            existing_node['params'].extend(query_params)
            existing_node['params'] = list(set(existing_node['params']))
            continue

        if not (check_domain(url=child_url, domain=domain)):
            continue

        print()

        print(f"------Child URL:------")
        print(child_url)
        print(f"----------------------")

        if(len(query_params) > 1):
            print("------Params------")
            for param in query_params:
                print(param)
            print("------------------")

        print()

        url_exists = False

        for existing_child in child_urls:
            if(existing_child['url'] == child_url):
                existing_child['params'].extend(query_params)
                existing_child['params'] = list(set(existing_child['params']))
                url_exists = True
                break
        if(url_exists):
            continue

        child_urls.append({"url":child_url, "params":query_params})


    return child_urls

def crawl_one(target_url, cookies, url_tree, domain=""):
    target_url["childs"] = crawl(target_url["url"], cookies, url_tree=url_tree, domain=domain)

def crawl_all(node, cookies, url_tree, domain='', visited=None):

    if visited is None:
        visited = set()

    if(node['url'] in visited):
        return
    
    visited.add(node['url'].rstrip("/"))

    if("childs" in node):
        for child_node in node["childs"]:
            crawl_all(child_node, cookies, url_tree=url_tree, domain=domain, visited=visited)
    else:
        crawl_one(node, cookies, url_tree=url_tree, domain=domain)

def check_domain(url, domain):
    new_url_domain = urlparse(url).hostname

    return new_url_domain == domain or new_url_domain.endswith(f'.{domain}') or domain == ''

