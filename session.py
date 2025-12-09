import json

def export_session(url_tree):
    with open("output/url_tree.json", "w+", encoding="utf-8") as output:
        json.dump(url_tree, output, ensure_ascii=False, indent=2)

    print("Written in output/url_tree.json")

def import_session(url_tree, import_file=None):
    if(not import_file):
        import_file = input("File to import: ")

    with open(import_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    url_tree.clear()
    url_tree.update(data)