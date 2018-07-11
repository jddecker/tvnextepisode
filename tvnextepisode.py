"""Gets the date of the next episode of a TV show"""

from datetime import datetime as dt
import sys

import requests


def main():
    # Getting info from TV Maze API and making sure there is a 200 response
    if sys.argv[1:]:
        query = ' '.join(sys.argv[1:])
    else:
        query = input('When is the next episode for: ')
    api = 'http://api.tvmaze.com/singlesearch/shows'
    parameters = {'q': query, 'embed': 'nextepisode'}
    response = requests.get(api, params=parameters)
    if response.status_code != 200:
        sys.exit("Can't find show or TV Maze is down")
    show = response.json()

    # Getting variables from converted json data
    name = show['name']
    premiered = None
    ep_date = None
    ep_time = None
    if show['premiered'] is not None:
        premiered = dt.strptime(show['premiered'], '%Y-%m-%d')
    if '_embedded' in show:
        if 'nextepisode' in show['_embedded']:
            ep_date = dt.strptime(
                show['_embedded']['nextepisode']['airdate'], '%Y-%m-%d')
            if show['_embedded']['nextepisode']['airtime'] != "":
                ep_time = dt.strptime(
                    show['_embedded']['nextepisode']['airtime'], '%H:%M')

    # Print information to the terminal
    print(name, end=' ')
    if premiered is not None:
        print('(' + str(premiered.year) + ')', end=' ')
    if ep_date is None:
        print('has no scheduled next episode')
    else:
        month = ep_date.month
        day = ep_date.day
        year = ep_date.year
        print('next episode is {}/{}/{}'.format(month, day, year), end='')
        if ep_time is not None:
            hour = ep_time.hour
            minute = ep_time.minute
            am_pm = 'am'
            if hour > 12:
                hour -= 12
                am_pm = 'pm'
            print(' @ {}:{:02d}{}'.format(hour, minute, am_pm))


if __name__ == '__main__':
    main()
