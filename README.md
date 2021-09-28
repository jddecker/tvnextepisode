# TV Show next episode

A quick Python and PowerShell and to query [TV Maze](https://tvmaze.com) API and find the next airtime for a TV show.

## Python Usage

You can just run the script or you can put an argument after it.

For example:

```
$ python3 tvnextepisode.py
```

OR with the `-s` flag:

```
$ python3 tvnextepisode.py -s "what we do in the shadows"
```

OR with the `--show` flag:

```
$ python3 tvnextepisode.py --show "what we do in the shadows"
```

## PowerShell Usage

You can add the show to the commandline with the `Show` variable:

```
.\tvnextepisode.ps1 -Show "what we do in the shadows"
```

Or you can run the script and it'll prompt for the show:

```
.\tvnextepisode.ps1
```
