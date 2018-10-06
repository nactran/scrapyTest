import json
urls = []
def main():
    for i in range(1,7):
        with open("items"+str(i)+"00.json",'r') as load_f:
            load_dict = json.load(load_f)
            for item in load_dict:
                if item not in urls:
                    urls.append(item)
    urls.sort(key = lambda k:k["url"])
    for item in urls:
        print(item)
    print(len(urls))
    with open("record.json","w") as f:
        json.dump(urls,f,ensure_ascii=False)

if __name__ == '__main__':
    main()
