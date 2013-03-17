App.net Word Cloud
=====

A simple last-24-hours word cloud of the most common words on App.net. Records the most common words, hashtags, links and mentions and provides a website for viewing these. Resets at midnight UTC.

Currently running on [Google App Engine](http://www.adnwc.net), using [web.py](http://webpy.org) (also on [Github](http://github.com/webpy/webpy)) to serve pages.

Raw JSON for each of the common items is available at `/wc`, `/hashtags`, `/links` and `/mentions`. The service is currently in __beta__ and the JSON _will_ change - there will be  at the least the addition of a date object indicating what day the results are recorded for.

Future additions
================

Currently there are plans to add the following:

- True language support; currently there is a basic hack in place to filter out most non-English posts by restricting user locales to `en_XX` locales only. This is somewhat effective but far from perfect. There are freely available libraries that allow one to determine the language of text - this needs testing and implementing. Implementing language support could result in a few new features:
    - Language specific common words
    - Statistical analysis - most common language, usage over time, etc.
- Additional metadata in the JSON responses. Currently it's just an array of `[item,count]` pairs. Additional metadata for this could include:
    - date that the items were recorded for
    - time of the latest update
    - post id of the last post to use a given item
- Recording of daily results. There is a shell method in place to handle this; results should be saved daily (or more often) for a permanent record. This could allow statistical analysis over time, as well as failure recovery (i.e. if the backend instance goes down, we can recover the days items from the last saved point)


License
=======

    Copyright 2013 Adam Speakman

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
