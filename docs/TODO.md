1. Get the web server execution to use the venv.  Custom apache
   configuration, or bouncing it through a shell script ?
1. Figure out a way to have a single request.Session so that we can set
a User-Agent of the form:

		EDCD-[A-Za-z]+-[.0-9]+
    without having to remember it on every request.

1. Implement use of Access Token against all available endpoints.
	1. Auth /decode
	1. Auth /me
	1. CAPI profile - DONE
	1. CAPI market - DONE
	1. CAPI shipyard - DONE
	1. CAPI journal - DONE
		1. CAPI journal current - DONE
		1. CAPI journal historic - DONE
	1. CAPI Community Goals - /communitygoals
		1. Need to query this when a CG is active to see the
		   output format and contents.

			```{ 
                activeCommunityGoals: (array of objects)
                [
                                { 
                                id: string
                                title: string
                                expiry: string
                                market_name: string
                                starsystem_name: string
                                activityType: string
                                target_commodity_list: string
                                target_qty: string
                                qty: string
                                objective: string
                                news: string
                                bulletin: string
                                commander_progress: { 
                                                currentQty: int
                                                numContributors: int
                                                commanderContributionQty: int or null
                                                commanderPercentile: int
                                                commanderSubscribed: bool
                                                unixTimeStamp: int
                                                complete: bool
                                                }
                                }
                ] 
}```
	1. See also: https://gist.github.com/corenting/b6ac5cf8f446f54856e08b6e287fe835
1. CL arg to try an expired Access Token anyway, in order to check the
   server response is as expected.
1. Find out what the expiry time is on a Refresh Token, and what exactly
   happens if you try to use it.
1. Implement automatically firing the whole Authorization mechanism if
   both Access Token and Refresh Token are expired.  This may well
   entail first merging the oauth2-pkce.py script into the
   org.miggy.edcapi namespace.
1. Implement non-PKCE authorization flow and document it.
1. Make sure the user script(s) are as quiet as possible during normal
   operation.
1. Update loop-test.sh to use fd-ed-capi.py
	1. Need to ensure return codes match up
1. In-code python documenting comments.
1. Consider a CAPI 'status board'.  Perform each of the following on a
   schedule and signal when we did and what the state was:
	1. Was auth.frontierstore.net reachable, and did it respond
	   properly?
	1. Can't do auth from scratch, as it requires user interaction.
	1. Use of Refresh Token for new Access Token
	1. Each CAPI endpoint
