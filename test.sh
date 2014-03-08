redis-cli flushdb
redis-cli SET url:1 google.com
redis-cli SET url:2 apreel.com
redis-cli SET url:3 amazon.com
redis-cli SET url:4 gajdulewicz.com
redis-cli SET url:5 gazeta.pl
redis-cli SET stats:count 5
siege -t 30s -f test_urls.txt -q -b