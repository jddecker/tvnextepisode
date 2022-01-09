<#
    .SYNOPSIS
        Find out when the next episode of a TV show
    .DESCRIPTION
        Querying TVmaze's API to get when the next episode of a show will be released

        TVmaze website: https://tvmaze.com
        TVmaze API: https://api.tvmaze.com
    .PARAMETER Show
        The name of the show to query
    .INPUTS
        None. Cannot pipe objects to tvnextepisode.ps1.
    .OUTPUTS
        Formatted string with the show results, show premiered date, and if there is a next episode scheduled and when
    .EXAMPLE
        PS> .\tvnextepisode.ps1 -Show "what we do in the shadows"
    .LINK
        https://github.com/jddecker/tvnextepisode
#>

param (
    [Parameter(Mandatory)][string] $Show  # What show to query
)

# Query
$search = @{
    q = $Show;
    embed = "nextepisode"
}

try {
    $response = Invoke-RestMethod -Uri "https://api.tvmaze.com/singlesearch/shows" -Method "Get" -Body $search
} catch {
    $_.Exception  # Output error
    exit 1
}

$name = "$($response.name) ($(Get-Date $response.premiered -Format 'yyyy'))"
# If no next episode air stamp then no new episode
if ($null -eq $response._embedded.nextepisode.airstamp) {
    "No new episodes of $name at this time"
} else {
    # Getting timezone name
    if ((Get-Date).IsDaylightSavingTime()) {
        $tzname = (Get-Timezone).DaylightName
    } else {
        $tzname = (Get-Timezone).StandardName
    }
    "The next episode of $name is $(Get-Date $response._embedded.nextepisode.airstamp -Format 'dddd MM/dd/yyyy @ h:mm tt K') ($($tzname))"
}

"Results from TVmaze <https://tvmaze.com>"
