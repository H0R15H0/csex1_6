import csv

def format_aozora():
    author_ids = []
    with open('./books.csv', 'w') as f:
        books = csv.writer(f)
        with open('./authors.csv', 'w') as f:
            authors = csv.writer(f)
            with open('./aozora.csv') as f:
                reader = csv.reader(f)
                for row in reader:
                    id, title, class_name, published_at, author_id, author = row[0], row[1], row[2], row[3], row[5], row[6]
                    books.writerow([title, class_name, published_at, author_id])
                    if author_id not in author_ids:
                        author_ids.append(author_id)
                        authors.writerow([author_id, author])

if __name__ == "__main__":
    format_aozora()