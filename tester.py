"""Download show search from TV Maze, convert to JSON and to file"""

import pprint
import sys

import requests


def main():
    """Run when the script starts"""
    query = 'lost'
    parameters = {'q': query}
    response = requests.get('http://api.tvmaze.com/search/shows', params=parameters)
    shows = response.json()

    with open(sys.path[0] + '/' + query + '.json', 'w') as fout:
        pprint.pprint(shows, fout)

if __name__ == '__main__':
    main()
