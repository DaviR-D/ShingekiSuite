import argparse
import fuzzer
import crawler

url_tree = dict()

def main():
    methods = [print, fuzzing, crawling, print_url_tree, print_params]

    option = 99
    parser = argparse.ArgumentParser(description="ShingekiSuite")
    parser.add_argument("-u", "--url", help="Target URL")
    args = parser.parse_args()
    url_tree["url"] = args.url

    while option != "0":
        print_menu()

        option = input("Choice: ")


        methods[int(option)]()
            

def print_menu():

    print("1) Fuzz")
    print("2) Crawl")
    print("3) Show available URLs")
    print("4) Print params")
    print("0) Exit")

def fuzzing():
    target_url = search_tree(input("Target URL: "), url_tree)
    wordlist_path = input("Wordlist: ")
    fuzzer.fuzz(target_url["url"], wordlist_path)

def crawling():
    target_url = search_tree(input("Target URL: "), url_tree)
    target_url["childs"] = crawler.crawl(target_url["url"])

def print_url_tree(node=url_tree, number="1", level=1):
    spaces = ""
    for l in range(0, level):
        spaces += " "

    print(f"{spaces}{number}. {node["url"]}")

    if("childs" in node):
        for n, i in zip(node["childs"], range(0, len(node["childs"]))):
            print_url_tree(n, f"{number}.{i+1}", level+1)

def print_params():
    target_url = search_tree(input("Target URL: "), url_tree)
    for param in target_url["params"]:
        print(param)

def search_tree(number, node):
    split_number = number.split(".")
    split_number.pop(0)
    if(len(split_number) == 0):
        return node
    else:
        next_number = split_number[0]
        return search_tree(".".join(split_number), node["childs"][int(next_number) - 1])
        

if __name__ == "__main__":
    main()