#!/usr/bin/env python
# coding=utf-8
import os
import collections
from datetime import datetime, timedelta
import time
import configparser
import feedparser
import jinja2
import pytz
import typing
import sys

from .extras import normalise_post, fetch_content

config = configparser.ConfigParser()

# Get a list of feed URLs
with open('feeds.txt') as f:
    SUBSCRIPTIONS = list(f)


# Date and time setup. I want only posts from "today" and "yesterday",
# where the day lasts until 2 AM.
TIMEZONE = config.get(section='default', option='timezone', fallback='GMT')

# Get the current time in the home timezone, then step back to include
# the last two days.
home_tz = pytz.timezone(TIMEZONE)
dt = datetime.now(home_tz)
if dt.hour < 2:
    dt -= timedelta(hours=72)
else:
    dt -= timedelta(hours=48)
start = dt.replace(hour=0, minute=0, second=0, microsecond=0)

# Convert this time back into UTC.
utc = pytz.utc
START = start.astimezone(utc)


try:
   Post = typing.NamedTuple('Post', [('time', str), ('blog', str), ('title',str), ('author',str), ('link', str), ('body',str)])

except Exception as exc:
   print(f'Exception Error: {exc}')


def process_entry(entry, blog):
    """
    Coerces an entry from feedparser into a Post tuple.
    Returns None if the entry should be excluded.
    """
    # Get the date of the post.  If it was published more than two days
    # ago, drop the entry.
    try:
        when = entry['updated_parsed']
    except KeyError:
        when = entry['published_parsed']
    when = utc.localize(datetime.fromtimestamp(time.mktime(when)))

    if when < START:
        return

    title = entry['title']
    try:
        author = entry['author']
    except KeyError:
        author = ', '.join(a['name'] for a in entry.get('authors', []))
    link = entry['link']
    try:
        body = entry['content'][0]['value']
    except KeyError:
        body = entry['summary']

    return normalise_post(Post(when, blog, title, author, link, body))    

posts = []
for url in SUBSCRIPTIONS:
    feed = feedparser.parse(url)
    try:
        blog = feed['feed']['title']
    except KeyError:
        raise Exception(f"[{feed.bozo_exception or 'unexpected error.'}] \n{(f'Could not fetch URL(s): {url}')}")
        sys.exit(-1)
        continue
    for entry in feed['entries']:
        post = process_entry(entry, blog)
        if post:
            posts.append(post)
    try:
      fetch_content(url)
    except:
      raise SystemExit
   
# Get the template, and drop in the posts
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f'{dir_path}/templates/template.html', encoding='utf8') as f:
    template = jinja2.Template(f.read())

with open(f'output/index.html', 'w', encoding='utf8') as f:
    f.write(template.render(posts=posts, time=datetime.now()))
