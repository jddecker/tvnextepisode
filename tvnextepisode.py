"""Gets the date of the next episode of a TV show"""

from datetime import datetime as dt
from datetime import timedelta as td
import sys

import requests


def main():
    # Getting query info for which show to look up
    if sys.argv[1:]:
        query = ' '.join(sys.argv[1:])
    else:
        query = input('When is the next episode for: ')

    # Querying TV Maze API and setting variables
    results = tvmazequery(query)
    name = results['name']
    premiered = results['premiered']
    ep_date = results['ep_date']
    ep_time = results['ep_time']

    # Printing premiered year
    print(name, end=' ')
    if premiered:
        print('(' + str(premiered.year) + ')', end=' ')

    # Printing episode date and time info
    if ep_date is None:
        print('has no scheduled next episode')
    else:
        print('next episode is {}/{}/{}'.format(ep_date.month, ep_date.day, ep_date.year), end='')

        # Figuring out am/pm
        if ep_time:
            am_pm = 'am'
            if ep_time.hour > 12:
                ep_time = ep_time - td(hours=12)
                am_pm = 'pm'
            print(' @ {}:{:02d} {}'.format(ep_time.hour, ep_time.minute, am_pm))
    
    # Printing TV Maze disclaimer
    print("(Info provided by TVmaze.com)")


def tvmazequery(show_name):
    """Query show on TV Maze's API and return the name, premiered year, and the next episode date and time as a dictionary"""
    api = 'http://api.tvmaze.com/singlesearch/shows'
    parameters = {'q': show_name, 'embed': 'nextepisode'}
    response = requests.get(api, params=parameters)
    if response.status_code != 200:
        sys.exit("Can't find show or TV Maze is down")
    show = response.json()

    # Getting variables from converted json data
    name = show['name']
    premiered = show.get('premiered')
    ep_date = show.get('_embedded', {}).get('nextepisode', {}).get('airdate')
    ep_time = show.get('_embedded', {}).get('nextepisode', {}).get('airtime')

    # Getting show premiered date if exists
    if premiered:
        premiered = dt.strptime(premiered, '%Y-%m-%d')
    
    # Getting show next episode date and time if exists
    if ep_date:
        ep_date = dt.strptime(ep_date, '%Y-%m-%d')
        if ep_time != "":
            ep_time = dt.strptime(ep_time, '%H:%M')
    
    # Returning results as a dictionary
    return {'name': name, 'premiered': premiered, 'ep_date': ep_date, 'ep_time': ep_time}

if __name__ == '__main__':
    main()
