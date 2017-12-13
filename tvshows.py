"""TV show updater"""

import requests


def main():
    """Run when the program starts"""
    query = input('Show search: ')
    parameters = {'q': query}
    response = requests.get('http://api.tvmaze.com/search/shows', params=parameters)
    shows = response.json()
    result_num = 0
    for show in shows:
        show = show['show']
        result_num += 1
        spacing = ' '
        spacing *= 3 - len(str(result_num))
        show_name = show['name']
        if show['network'] is None or show['network']['name'] is None:
            network_name = 'unknown network'
        else:
            network_name = show['network']['name']
        if show['premiered'] is None:
            premiered_year = 'year unknown'
        else:
            premiered_year = show['premiered'][:4]
        print(str(result_num) + '.' + spacing + show_name + ' (' + network_name + ', ' +
              str(premiered_year) + ')')

if __name__ == '__main__':
    main()
