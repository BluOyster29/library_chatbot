import requests
import json
import urllib.request
import urllib.parse

query_params = {
    'book_author': 'inauthor',
    'book_title': 'intitle',
    'book_subject': 'subject'
}

def gen_user_query(query, q_params):
    q = ''
    for i in query.keys():
        try:
            q += '{}:{}+'.format(q_params[i], query[i])
        except:
            continue

    return q[:-1]

def process_request(url):

    r = urllib.request.urlopen(url).read()
    data = json.loads(r)

    return data

def config(query):

    params = {
        "q": '{}'.format(query),
        'key': '',
        'maxResults': "10",
        'langRestrict' : 'en'
    }
    url_params = urllib.parse.urlencode(params)
    url = "https://www.googleapis.com/books/v1/volumes?{}".format(url_params)
    

    return url


def clean_data(data):
    book_db = {}
    
    book_titles = []
    for i in data['items']:
        if i['volumeInfo']['title'] not in book_titles:
            try:
                
                book_titles.append((i['volumeInfo']['title'], 
                                    i['volumeInfo']['authors'][0],
                                    i['volumeInfo']['industryIdentifiers'][0]['identifier'],
                                    i['volumeInfo']['description']))

                try:                    
                    book_db[i['volumeInfo']['industryIdentifiers'][0]['identifier']] = {'title' : i['volumeInfo']['title'],
                                                                                    'author' : i['volumeInfo']['authors'][0],
                                                                                    'description' : i['volumeInfo']['description']}
                except:
                    continue
                
            except:
                continue

    return book_titles, book_db


def main(user_input):
    query_params = {
        'book_author': 'inauthor',
        'book_title': 'intitle',
        'book_subject': 'subject'
    }

    query = gen_user_query(user_input, query_params)
    url = config(query)
    print(url)
    r = process_request(url)
    #print(r)
    data, book_db = clean_data(r)

    return data, book_db

def print_data(data):

    for i in data:
        
        try:
            print('\nBook Title: {}\nBook Author: {}\nISBN: {}'.format(i[0], i[1], i[2]))
        except:
            print(i)
            


if __name__ == '__main__':
    request  = {
            'book_title' : 'the hobbit'}
    data, db  = main(request)
    #print_data(data)
    print(db)