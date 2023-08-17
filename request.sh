#!/bin/bash

export HOST=192.168.59.119

while sleep 0.1;

do curl --location --request POST $HOST:30001/get_sentiments \
--header 'Content-Type: application/json' \
--data-raw '{
    "tweets": ["I love @JT", "#OMG this is making me barf."]
}'

done
