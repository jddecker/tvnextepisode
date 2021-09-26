<#
Querying TVMaze's API to get when the next episode of a show will air
#>

param (
    [Parameter(Mandatory)][string]$Show  # What show to query
)

Write-Output "Find out when the next episode of a TV show."
Write-Output "Information provided by TVmaze.com <https://tvmaze.com>`n"

# Setting up search variables
$search = @{
    q = $Show;
    embed = "nextepisode"
}

$response = Invoke-RestMethod -Uri "https://api.tvmaze.com/singlesearch/shows" -Method "Get" -Body $search

# If no next episode air stamp then no new episode
if ($null -eq $response._embedded.nextepisode.airstamp) {
    Write-Output "No new episodes of $($response.name) at this time"
} else {
    Write-Output "The next episode of $($response.name) ($(Get-Date $response.premiered -Format 'yyyy')) is $(Get-Date $response._embedded.nextepisode.airstamp -Format 'MM/dd/yyyy @ h:mm tt')"
}
