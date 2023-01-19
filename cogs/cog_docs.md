# TimeoutCog
command is called as a normal slash command `/timeoutpoll`.

the user is prompted with 4 fields: 
`offender`,
`emoji count`,
`timeout duration` and 
`description`

emoji count will be removed in the next iteration.

## logic:
  - require role specified (in .env) 
  - positive integer and formatting checks (of user input)
          duration formatting. 
  - discord currently supports a maximum of 28 days for timeouts. checks for that included 
  - asyncio accepts only seconds. therefore, we convert the input into seconds 
  - poll_duration is determined by taking the timeout_duration and processing it
    - letters are stripped since users can input m, h and d.
    - they are then converted to a datetime_timedelta object and total_seconds is called
    - 3 categories of time are being checked for:
        - shorter than 120 minutes
        - longer than 120 minutes but shorter than 48h
        - longer than 48h
    - based on the result, the duration is either slashed by 10 or by 5
    - an embed is then constructed with the author, offender, description, timeout and poll duration details   
        - two emoji are added to the poll
        - the bot responds with a call to action and goes to sleep for - the duration calculated
  - after waking up, the bot counts the number of emoji and begins the - checking process:
    - it checks the reaction count and removes 1 of each from it
    - it checks if the emoji_count and majority conditions are satisfied
  based on the timeout amount, a different version of the same thing happens
    - smaller timeouts are named frostbolts
    - medium timeouts are named frost nova
    - big timeouts are named frostfirebolt
- if not satisfied, appropriate errors are retured
