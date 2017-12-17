"""TV show updater"""

import requests

def get_show_list(shows):
    """Gather shows data into a dictionary from json data"""
    result_num = 0
    results = {}
    for show in shows:
        show = show['show']
        result_num += 1
        show_name = show['name']
        if show['network'] is not None:
            network_name = show['network'].get('name')
        elif show['webChannel'] is not None:
            network_name = show['webChannel'].get('name')
        else:
            network_name = None
        if show['premiered'] is None:
            premiered_year = None
        else:
            premiered_year = show['premiered'][:4]
        result_tuple = (show_name, network_name, premiered_year)
        results[result_num] = result_tuple
    return results

def print_shows(results):
    """Print the results of the shows"""
    for num in results:
        if len(str(num)) == 1:
            number = ' ' + str(num)
        else:
            number = str(num)
        name = results[num][0]
        desc = []
        if results[num][1] is not None:
            desc.append(results[num][1])
        if results[num][2] is not None:
            desc.append(results[num][2])
        desc_text = ', '.join(desc)
        print(number + '. ' + name + ' (' + desc_text + ')')

def main():
    """Run when the program starts"""
    query = input('Show search: ')
    parameters = {'q': query}
    api = 'http://api.tvmaze.com/search/shows'
    response = requests.get(api, params=parameters)
    shows = response.json()
    results = get_show_list(shows)
    print_shows(results)

if __name__ == '__main__':
    main()
