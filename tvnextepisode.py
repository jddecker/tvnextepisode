"""Gets the date of the next episode of a TV show"""

import sys
import json
from argparse import ArgumentParser
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
from datetime import datetime, timezone


def main():
    # Printing statement at the top
    print('Find out when the next episode of a TV show.')
    print('Information provided by TVmaze.com <https://tvmaze.com>', end='\n\n')

    # Getting information from command line
    parser = ArgumentParser()
    parser.add_argument('-s', '--show')
    args = parser.parse_args()

    # Querying TV Maze API
    results = tvmazequery(args.show)
    
    # Checking if there is a new episode
    if results['next_ep'] is None:
        print(f"No new episodes of {results['name']} ({results['premiered'].year}) at this time")
    else:
        # Converting UTC to local time for next episode
        next_ep_local = results['next_ep'].replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(f"The next episode of {results['name']} ({results['premiered'].year}) is {next_ep_local.strftime('%m/%d/%Y @ %I:%M %p %z (%Z)')}")


def tvmazequery(show):
    """Query show on TV Maze's API

    Args: show_name (str): Name of the TV show

    Returns:
        A dict mapping keys from the returned json. For example:

        {
            'name': 'What We Do in the Shadows',
            'premiered': 2019-03-27,
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

    # Converting premiered to a datetime object
    next_ep_dict['premiered'] = datetime.strptime(results['premiered'], '%Y-%m-%d')

    # Next episode airstamp doesn't exist if there isn't another episode scheduled
    try:
        # next_ep as a datetime object
        next_ep_dict['next_ep'] = datetime.strptime(results['_embedded']['nextepisode']['airstamp'], '%Y-%m-%dT%H:%M:%S%z')
    except KeyError:
        next_ep_dict['next_ep'] = None

    # Returning results as a dictionary
    return next_ep_dict


if __name__ == '__main__':
    main()
