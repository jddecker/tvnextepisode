"""Gets the date of the next episode of a TV show"""

import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
from datetime import datetime as dt
from datetime import timedelta as td


def main():
    # Printing statement at the top
    print('Find out when the next episode of a TV show.')
    print('Information provided by TVmaze.com <https://tvmaze.com>', end='\n\n')

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
        print('next episode is {}/{}/{}'.format(ep_date.month,
                                                ep_date.day, ep_date.year), end='')

        # Figuring out am/pm
        if ep_time:
            am_pm = 'am'
            if ep_time.hour > 12:
                ep_time = ep_time - td(hours=12)
                am_pm = 'pm'
            print(' @ {}:{:02d} {}'.format(ep_time.hour, ep_time.minute, am_pm))
        else:
            print('')  # Adding a newline if no time


def tvmazequery(show_name):
    """Query show on TV Maze's API

    Args: show_name (str): Name of the TV show

    Returns:
        A dict mapping keys from the returned json. For example:

        {
            'name': 'What We Do in the Shadows',
            'premiered': 2019,
            'ep_date': '2020-06-10'
            'ep_time': '22:00'
        }
    """

    # Getting show query with the API
    api = 'https://api.tvmaze.com/singlesearch/shows'
    params = {'q': show_name, 'embed': 'nextepisode'}
    request = Request(url=api + '?' + urlencode(params))

    try:
        response = urlopen(request)
    except URLError as e:
        sys.exit("Server couldn't complete request. Error: " + str(e.reason))
    except URLError as e:
        sys.exit('Failed to reach the server. Error: ' + str(e.reason))
    else:
        show = json.loads(response.read().decode('utf-8'))

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
        if ep_time != '':
            ep_time = dt.strptime(ep_time, '%H:%M')

    # Returning results as a dictionary
    return {'name': name, 'premiered': premiered, 'ep_date': ep_date, 'ep_time': ep_time}


if __name__ == '__main__':
    main()
