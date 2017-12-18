"""Gets the date of the next episode"""

import datetime
import sys

import requests


def main():
    """
    Run on startup. Input a TV show name and returns if the show has a next episode and
    when it will air
    """

    query = input('When is the next episode for: ')
    api = 'http://api.tvmaze.com/singlesearch/shows'
    parameters = {'q': query, 'embed': 'nextepisode'}
    response = requests.get(api, params=parameters)
    if response.status_code != 200:
        sys.exit("Can't find show or TV Maze API is down")
    show = response.json()

    name = show['name']
    if show['premiered'] is not None:
        premiered = datetime.datetime.strptime(show['premiered'], '%Y-%m-%d')
    else:
        premiered = None

    if '_embedded' in show:
        if 'nextepisode' in show['_embedded']:
            nextepisode_date = datetime.datetime.strptime(
                show['_embedded']['nextepisode']['airdate'], '%Y-%m-%d')
            if show['_embedded']['nextepisode']['airtime'] == "":
                nextepisode_time = None
            else:
                nextepisode_time = datetime.datetime.strptime(
                    show['_embedded']['nextepisode']['airtime'], '%H:%M')
        else:
            nextepisode_date = None
            nextepisode_time = None
    else:
        nextepisode_date = None
        nextepisode_time = None

    print(name, end=' ')
    if premiered is not None:
        print('(' + str(premiered.year) + ')', end=' ')

    if nextepisode_date is None:
        print('has no scheduled next episode')
    else:
        print('next episode is', end=' ')
        print(str(nextepisode_date.month) + '/' +
              str(nextepisode_date.day) + '/' + str(nextepisode_date.year), end='')

        if nextepisode_time is not None:
            print(' @ {:02d}:{:02d}'.format(
                nextepisode_time.hour, nextepisode_time.minute))


if __name__ == '__main__':
    main()
