# log2token
Parse logfiles for interesting Tokens with their Timeline into JSON or Tabulated formats etc

# Searching for Tokens
Given a token name, the match positive or negative logged values:
token(s)=NUM (or -NUM) 

Eg. Use the program to search for tokens like state=3 or temp=-15.

## Types of Token Search
- Comma-separated tokens, eg state,temp etc
- OR separator, eg state|temp etc
- Regular expressions, eg m\d{4} (i.e. m[4-digits]) etc


# Date & Timestamps
While searching, track the Date/Time so that the token (or parameters of interest) can be plotted on a generic timeline using any standard tools or scripts.

## Date Time Format
Standard Date/Time format is currently supported
YYYY-MM-DDTHH:MM:SS.MS

## Example Output:
```
________________ Token: <Token> _________________
date                 time                 value
2023/01/23           06:59:49.26655       1386
2023/01/23           06:59:52.26657       1473
2023/01/23           06:59:55.39158       -1546
```

# Support Output Formats:
JSON, Pretty Print, Table
