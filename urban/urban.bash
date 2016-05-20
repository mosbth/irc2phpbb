#!/usr/bin/env bash

#
# Set it up
#
TODAY=$( date +"%Y%m%d" )
URBAN_DICTIONARY="urban.dictionary"
URBAN_TODAY="urban.$TODAY"
URBAN_LAST_ID="urban.last"
URBAN_RESULT="urban.result"
IRC_INCOMING="../incoming"



#
# Return the next word to use from the dictionary, update row number of 
# current word.
#
function nextWord
{
    local row=$( < "$URBAN_LAST_ID" )
    local max=$( wc -l < "$URBAN_DICTIONARY" )
    (( row++ ))

    if [ "$row" -gt "$max" ]; then
        row=1
    fi

    echo "$row" > "$URBAN_LAST_ID"
    echo "$( sed "${row}q;d" "$URBAN_DICTIONARY" )"
}



#
# Get JSON for word
#
function getUrbanJsonForToday
{
    wget --quiet -O "$URBAN_TODAY" "http://api.urbandictionary.com/v0/define?term=$1"
}



#
# Parse JSON string as ordinary string
#
function parseJSONString
{
    local string=$( echo "$1" | sed 's/\\r\\n/ /g' | sed '/^$/d' )
    eval "set -- $string"
    echo "$@"
}



#
# Printable version of todays word
#
function printWordOfToday
{
    local word=$( jq '.list[0].word' "$URBAN_TODAY" )
    local definition=$( jq '.list[0].definition' "$URBAN_TODAY" )
    local example=$( jq '.list[0].example' "$URBAN_TODAY" )

    word=$( parseJSONString "$word" )
    definition=$( parseJSONString "$definition" )
    example=$( parseJSONString "$example" )

    echo "Veckans Glosövning i Internet Slang: $word"
    echo "$definition" 
    echo "$example"
}



#
# Do it
#
if [ ! -f "$URBAN_LAST_ID" ]; then
    echo "0" > "$URBAN_LAST_ID"
fi

if [ ! -f "$URBAN_TODAY" ]; then
    getUrbanJsonForToday "$( nextWord )"
fi

printWordOfToday > "$URBAN_RESULT"
cp "$URBAN_RESULT" "$IRC_INCOMING"
