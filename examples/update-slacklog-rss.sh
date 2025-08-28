#!/usr/bin/env bash

#
#   Where are the ChangeLogs stored
#
SRC_DIR=./test/changelogs

#
#   Where to store the RSS feeds
#
DST_DIR=./test/rss

#
#   Use one lastBuildDate for every feed for consistency
#
LAST_BUILD_DATE="$(date -Iseconds)"

#
#   A function that knows how to update a single feed.
#
update_rss() {
    slackware=$1
    version=$2
    min_date=$3

    echo -n "Generating RSS for $slackware $version... "

    #
    #   Update the RSS feed
    #
    LANG=C.UTF-8 slacklog2rss \
        --changelog "$SRC_DIR/$slackware-$version.txt" \
        --min-date="$min_date" \
        --out "$DST_DIR/$slackware-$version.rss" \
        --slackware="$slackware $version" \
        --rssLink="http://linuxbox.fi/~vmj/slacklog/$slackware-$version.rss" \
        --description="Recent changes in $slackware $version" \
        --managingEditor="vmj@linuxbox.fi (Mikko Värri)" \
        --webMaster="vmj@linuxbox.fi (Mikko Värri)" \
        --lastBuildDate="$LAST_BUILD_DATE"

    echo "OK"
}

mkdir -p "$DST_DIR"

#
#   Store the last build date for tests
#
echo "$LAST_BUILD_DATE" >"$DST_DIR-timestamp"

#   Update various feeds.

#   For stable releases, the below date is the date of the first
#   patch to the -current branch.  I.e. the slackware 13.0 feed
#   would then contain all the changes made to the -current until
#   it became a release, and all the changes after that.
update_rss slackware   15.0    'Wed Feb  2 22:22:22 UTC 2022'
update_rss slackware64 15.0    'Wed Feb  2 22:22:22 UTC 2022'

#   For current, use some very old date.
update_rss slackware   current 'Thu Jan  1 00:00:00 UTC 1970'
update_rss slackware64 current 'Thu Jan  1 00:00:00 UTC 1970'
