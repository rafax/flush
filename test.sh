redis-cli flushdb
redis-cli SET u:1 google.com
redis-cli SET u:2 apreel.com
redis-cli SET u:3 amazon.com
redis-cli SET u:4 gajdulewicz.com
redis-cli SET u:5 gazeta.pl
redis-cli SET stats:url_count 5
siege -t 30s -f test_urls.txt -q -b