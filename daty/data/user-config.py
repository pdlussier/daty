# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

# Website
family = 'wikidata'

# The language code of the site we're working on.
mylang = 'wikidata'

# YOUR USERNAME
usernames['wikidata']['wikidata'] = u'your_user'

# PASSWORD
# You have to generate a bot username and password at this link:
# https://www.wikidata.org/wiki/Special:BotPasswords
# After creating them put them in 'user-password.py' file
password_file = 'user-password.py'

































# Logs section
log = ['interwiki']
logfilename = None
logfilesize = 1024
logfilecount = 5
verbose_output = 0
log_pywiki_repo_version = False
debug_log = []
user_script_paths = []

# Interwiki settings
interwiki_backlink = True
interwiki_shownew = True
interwiki_graph = False
interwiki_min_subjects = 100
interwiki_graph_formats = ['png']
interwiki_graph_url = None
without_interwiki = False
interwiki_contents_on_disk = False

# Disambiguation settings
sort_ignore_case = False

# Commons setting
upload_to_commons = False

# Gosh too long

# ############# SETTINGS TO AVOID SERVER OVERLOAD ##############

# Slow down the robot such that it never requests a second page within
# 'minthrottle' seconds. This can be lengthened if the server is slow,
# but never more than 'maxthrottle' seconds. However - if you are running
# more than one bot in parallel the times are lengthened.
#
# By default, the get_throttle is turned off, and 'maxlag' is used to
# control the rate of server access. Set minthrottle to non-zero to use a
# throttle on read access.
minthrottle = 0
maxthrottle = 60

# Slow down the robot such that it never makes a second page edit within
# 'put_throttle' seconds.
put_throttle = 10

# Sometimes you want to know when a delay is inserted. If a delay is larger
# than 'noisysleep' seconds, it is logged on the screen.
noisysleep = 3.0

# Defer bot edits during periods of database server lag. For details, see
# https://www.mediawiki.org/wiki/Maxlag_parameter
# You can set this variable to a number of seconds, or to None (or 0) to
# disable this behavior. Higher values are more aggressive in seeking
# access to the wiki.
# Non-Wikimedia wikis may or may not support this feature; for families
# that do not use it, it is recommended to set minthrottle (above) to
# at least 1 second.
maxlag = 5

# Maximum of pages which can be retrieved at one time from wiki server.
# -1 indicates limit by api restriction
step = -1

# Maximum number of times to retry an API request before quitting.
max_retries = 15
# Minimum time to wait before resubmitting a failed API request.
retry_wait = 5

# ############# TABLE CONVERSION BOT SETTINGS ##############

# Will split long paragraphs for better reading the source.
# Only table2wiki.py use it by now.
splitLongParagraphs = False
# sometimes HTML-tables are indented for better reading.
# That can do very ugly results.
deIndentTables = True

# ############# WEBLINK CHECKER SETTINGS ##############

# How many external links should weblinkchecker.py check at the same time?
# If you have a fast connection, you might want to increase this number so
# that slow servers won't slow you down.
max_external_links = 50

report_dead_links_on_talk = False

# Don't alert on links days_dead old or younger
weblink_dead_days = 7

# ############# DATABASE SETTINGS ##############
# Setting to connect the database or replica of the database of the wiki.
# db_name_format can be used to manipulate the dbName of site.
#
# Example for a pywikibot running on wmflabs:
# db_hostname = 'enwiki.analytics.db.svc.eqiad.wmflabs'
# db_name_format = '{0}_p'
# db_connect_file = user_home_path('replica.my.cnf')
db_hostname = 'localhost'
db_username = ''
db_password = ''
db_name_format = '{0}'
db_connect_file = user_home_path('.my.cnf')
# local port for mysql server
# ssh -L 4711:enwiki.analytics.db.svc.eqiad.wmflabs:3306 \
#     user@login.tools.wmflabs.org
db_port = 3306

# ############# SEARCH ENGINE SETTINGS ##############
# Live search web service appid settings.
#
# Yahoo! Search Web Services are not operational.
# See https://phabricator.wikimedia.org/T106085
yahoo_appid = ''

# To use Windows Live Search web service you must get an AppID from
# http://www.bing.com/dev/en-us/dev-center
msn_appid = ''

# ############# FLICKR RIPPER SETTINGS ##############

# Using the Flickr api
flickr = {
    'api_key': '',  # Provide your key!
    'api_secret': '',  # Api secret of your key (optional)
    'review': False,  # Do we use automatically make our uploads reviewed?
    'reviewer': '',  # If so, under what reviewer name?
}

# ############# COPYRIGHT SETTINGS ##############

# Enable/disable search engine in copyright.py script
copyright_google = True
copyright_yahoo = True
copyright_msn = False

# Perform a deep check, loading URLs to search if 'Wikipedia' is present.
# This may be useful to increase the number of correct results. If you haven't
# a fast connection, you might want to keep them disabled.
copyright_check_in_source_google = False
copyright_check_in_source_yahoo = False
copyright_check_in_source_msn = False

# Web pages may contain a Wikipedia text without the word 'Wikipedia' but with
# the typical '[edit]' tag as a result of a copy & paste procedure. You want
# no report for this kind of URLs, even if they are copyright violations.
# However, when enabled, these URLs are logged in a file.
copyright_check_in_source_section_names = False

# Limit number of queries for page.
copyright_max_query_for_page = 25

# Skip a specified number of queries
copyright_skip_query = 0

# Number of attempts on connection error.
copyright_connection_tries = 10

# Behavior if an exceeded error occur.
#
# Possibilities:
#
#    0 = None
#    1 = Disable search engine
#    2 = Sleep (default)
#    3 = Stop
copyright_exceeded_in_queries = 2
copyright_exceeded_in_queries_sleep_hours = 6

# Append last modified date of URL to script result
copyright_show_date = True

# Append length of URL to script result
copyright_show_length = True

# By default the script tries to identify and skip text that contains a large
# comma separated list or only numbers. But sometimes that might be the
# only part unmodified of a slightly edited and not otherwise reported
# copyright violation. You can disable this feature to try to increase the
# number of results.
copyright_economize_query = True

# ############# HTTP SETTINGS ##############
# Use a persistent http connection. An http connection has to be established
# only once per site object, making stuff a whole lot faster. Do NOT EVER
# use this if you share Site objects across threads without proper locking.
#
# DISABLED FUNCTION. Setting this variable will not have any effect.
persistent_http = False

# Default socket timeout in seconds.
# DO NOT set to None to disable timeouts. Otherwise this may freeze your
# script.
# You may assign either a tuple of two int or float values for connection and
# read timeout, or a single value for both in a tuple (since requests 2.4.0).
socket_timeout = (6.05, 45)


# ############# COSMETIC CHANGES SETTINGS ##############
# The bot can make some additional changes to each page it edits, e.g. fix
# whitespace or positioning of interwiki and category links.

# This is an experimental feature; handle with care and consider re-checking
# each bot edit if enabling this!
cosmetic_changes = False

# If cosmetic changes are switched on, and you also have several accounts at
# projects where you're not familiar with the local conventions, you probably
# only want the bot to do cosmetic changes on your "home" wiki which you
# specified in config.mylang and config.family.
# If you want the bot to also do cosmetic changes when editing a page on a
# foreign wiki, set cosmetic_changes_mylang_only to False, but be careful!
cosmetic_changes_mylang_only = True

# The dictionary cosmetic_changes_enable should contain a tuple of languages
# for each site where you wish to enable in addition to your own langlanguage
# (if cosmetic_changes_mylang_only is set)
# Please set your dictionary by adding such lines to your user-config.py:
# cosmetic_changes_enable['wikipedia'] = ('de', 'en', 'fr')
cosmetic_changes_enable = {}

# The dictionary cosmetic_changes_disable should contain a tuple of languages
# for each site where you wish to disable cosmetic changes. You may use it with
# cosmetic_changes_mylang_only is False, but you can also disable your own
# language. This also overrides the settings in the cosmetic_changes_enable
# dictionary. Please set your dict by adding such lines to your user-config.py:
# cosmetic_changes_disable['wikipedia'] = ('de', 'en', 'fr')
cosmetic_changes_disable = {}

# cosmetic_changes_deny_script is a list of scripts for which cosmetic changes
# are disabled. You may add additional scripts by appending script names in
# your user-config.py ("+=" operator is strictly recommended):
# cosmetic_changes_deny_script += ['your_script_name_1', 'your_script_name_2']
# Appending the script name also works:
# cosmetic_changes_deny_script.append('your_script_name')
cosmetic_changes_deny_script = ['category_redirect', 'cosmetic_changes',
                                'newitem', 'touch']

# ############# REPLICATION BOT SETTINGS ################
# You can add replicate_replace to your user-config.py.
#
# Use has the following format:
#
# replicate_replace = {
#            'wikipedia:li': {'Hoofdpagina': 'Veurblaad'}
# }
#
# to replace all occurrences of 'Hoofdpagina' with 'Veurblaad' when writing to
# liwiki. Note that this does not take the origin wiki into account.
replicate_replace = {}

# ############# FURTHER SETTINGS ##############

# Proxy configuration

# TODO: proxy support
proxy = None

# Simulate settings

# Defines what additional actions the bots are NOT allowed to do (e.g. 'edit')
# on the wiki server. Allows simulation runs of bots to be carried out without
# changing any page on the server side. Use this setting to add more actions
# in user-config.py for wikis with extra write actions.
actions_to_block = []

# Set simulate to True or use -simulate option to block all actions given
# above.
simulate = False

# How many pages should be put to a queue in asynchronous mode.
# If maxsize is <= 0, the queue size is infinite.
# Increasing this value will increase memory space but could speed up
# processing. As higher this value this effect will decrease.
max_queue_size = 64

# Define the line separator. Pages retrieved via API have "\n" whereas
# pages fetched from screen (mostly) have "\r\n". Interwiki and category
# separator settings in family files should use multiplied of this.
# LS is a shortcut alias.
line_separator = LS = '\n'

# Settings to enable mwparserfromhell
# <https://mwparserfromhell.readthedocs.org/en/latest/>
# Currently used in textlib.extract_templates_and_params
# This is more accurate than our current regex, but only works
# if the user has already installed the library.
use_mwparserfromhell = True

# Pickle protocol version to use for storing dumps.
# This config variable is not used for loading dumps.
# Version 2 is common to both Python 2 and 3, and should
# be used when dumps are accessed by both versions.
# Version 4 is only available for Python 3.4
pickle_protocol = 2

