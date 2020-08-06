import requests
import json
from bs4 import BeautifulSoup

query_codes = {
    'book_author' : 'förf',
    'book_title'  : 'tit',
    'genre'  : 'AMNE',
    'isbn'   : 'NUMM',
    'yesr'     : 'ÅR'
}

lang_decoder = {
    'pol' : 'Polish',
    'eng' : 'English',
    'swe' : 'Swedish'
}

base_url = 'http://api.libris.kb.se/xsearch'


def user_input_to_tuple(user_in):
    return (list(user_in.keys())[0], list(user_in.values())[0])
    
def fill_in_parameters(query_codes, user_input):
    
    '''
    Here i need to add more options for the query 
    
    '''
    
    return {'query' : '{}:{}'.format(query_codes[user_input[0]], user_input[1]), 
                  'n': 20, 'format' : 'json'}

def get_top_results(loaded_json):
    results = []
    num = 2
    book_titles = []
    failsafe = 20
   
   
    for i in loaded_json['xsearch']['list']:
        if  i['type'] == 'book' and i['title'] not in book_titles:
            try:
                results.append(i)
                book_titles.append(i['title'])
                num += 1
            except:
                continue
                    
    return results

def print_results_to_terminal(results):
    
    print('Top 10 results for query for books by ')
    for i in results:

        try:
            print('\nTitle:{}\nAuthor:{}\nLanguage:{}\n'.format(i['title'],i['creator'],lang_decoder[i['language']]))
        except:
            pass

def big_string(results):
    result_string =  []
    
    for i in results:

        try:
            result_string.append('\nTitle:{}\nAuthor:{}\nLanguage:{}\n'.format(i['title'],i['creator'],lang_decoder[i['language']]))
        except:
            pass
        
    return result_string

def main(user_input):
    
    user_input = user_input_to_tuple(user_input)
    payload = fill_in_parameters(query_codes, user_input)
    r = requests.get(base_url, params=payload)
    json_data = json.loads(r.content)
    results = get_top_results(json_data)
    a_big_string = big_string(results)
    return a_big_string

if __name__ == '__main__':
    main({'book_author' : 'stephen king'})
    