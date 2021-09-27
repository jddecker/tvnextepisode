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


def tvmazequery(show):
    """Query show on TV Maze's API

    Args: show_name (str): Name of the TV show

    Returns:
        A dict mapping keys from the returned json. For example:

        {
            'name': 'What We Do in the Shadows',
            'premiered': 2019,
            'next_ep': '2020-06-10T02:00:00+00:00'
        }
    """

    # Getting show query with the API
    api = 'https://api.tvmaze.com/singlesearch/shows'
    body = {'q': show, 'embed': 'nextepisode'}
    request = Request(url=api + '?' + urlencode(body))

    # Print error if request can't be made
    try:
        response = urlopen(request)
    except URLError as e:
        sys.exit("Server couldn't complete request. Error: " + str(e.reason))
    except HTTPError as e:
        sys.exit('Failed to reach the server. Error: ' + str(e.reason))
    else:
        # Load results into json object
        results = json.loads(response.read())

    # Getting variables from converted json data
    next_ep_dict = {}
    next_ep_dict['name'] = results['name']
    next_ep_dict['premiered'] = results['premiered']
    # Next episode airstamp doesn't exist if there isn't another episode scheduled
    try:
        next_ep_dict['next_ep'] = results['_embedded']['nextepisode']['airstamp']
    except KeyError:
        next_ep_dict['next_ep'] = None

    # Returning results as a dictionary
    return next_ep_dict


if __name__ == '__main__':
    main()
