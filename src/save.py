import csv

def save_to_file(articles):
    file = open("techcrunch.csv", mode="w")
    writer = csv.writer (file)
    writer.writerow (["title", "Date", "link"])

    #print(articles)

    for article in articles:
        writer.writerow(list(article.values()))
        #print (article.values())

    return
