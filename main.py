from session import *
from visual import *
from crawler import *
from fuzzer import *
import argparse



url_tree = dict()
fuzzing_wordlist = ""
cookies = dict()

def add_args():
    parser = argparse.ArgumentParser(description="ShingekiSuite")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-is", "--import-session", help="Import previous session")
    parser.add_argument("-fw", "--fuzzer-wordlist", help="Set fixed fuzzing wordlist")
    parser.add_argument("-c", "--cookie", help="Cookie (key=value)", action="append")
    args = parser.parse_args()

    return args

def load_args():
    global fuzzing_wordlist
    global url_tree

    args = add_args()

    for cookie in args.cookie or []:
        key, value = cookie.split('=', 1)
        cookies[key] = value

    url_tree["url"] = args.url

    fuzzing_wordlist = args.fuzzer_wordlist

    if(args.import_session):
        import_session(url_tree=url_tree, import_file=args.import_session)

def handle_option(option):
    global url_tree
    global fuzzing_wordlist
    global cookies

    handle = {
    0: lambda: print(),
    1: lambda: fuzzing(search_tree(input("Target URL: "), url_tree), fuzzing_wordlist, cookies),
    2: lambda: crawl_one(search_tree(input("Target URL: "), url_tree), cookies),
    3: lambda: print_url_tree(current_node=url_tree),
    4: lambda: print_params(search_tree(input("Target URL: "), url_tree)),
    5: lambda: print_url_tree(current_node=url_tree, include_params=True),
    6: lambda: crawl_all(node=url_tree, cookies=cookies),
    7: lambda: export_session(url_tree=url_tree),
    8: lambda: import_session(url_tree),
}
    
    handle[int(option)]()


def main():
    load_args()

    option = 99

    while option != "0":
        print_menu()

        option = input("Choice: ")

        print()

        handle_option(option)


def search_tree(number, node):
    index_array = number.split(".")
    index_array.pop(0)
    
    if(len(index_array) == 0):
        return node
    
    else:
        next_index = int(index_array[0]) - 1
        next_node = node["childs"][next_index]

        return search_tree(".".join(index_array), next_node)
        
if __name__ == "__main__":
    main()