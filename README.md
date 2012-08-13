flush
====

FLask Url SHortener - an app to play with Flask and some other technologies

Available endpoints:

- /[a-z0-9]+ GET => redirect to the full URL, store request data and update stats
- /shorten POST => shorten the link passed in 'link' POST variable
- /info/[a-z0-9]+ GET => return information about visits to the link specified in URL