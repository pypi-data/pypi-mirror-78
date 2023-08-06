.. image:: https://badge.fury.io/py/Procpath.svg
  :target: https://pypi.python.org/pypi/Procpath

********
Procpath
********
Procpath is a process tree analysis command-line workbench. Its goal is to
provide natural interface to the tree structure of processes running on a
Linux system for inspection and later analysis.

.. contents::

Installation
============
.. sourcecode::

   pip install --user Procpath

For installing Procpath into a dedicated virtual environment ``pipx`` [12]_
can be used.

.. sourcecode::

   pipx install Procpath

Quickstart
==========
Get comma-separated PIDs of the process subtree (including the parent process
``pid=2610``).

.. sourcecode::

   procpath query -d , '$..children[?(@.stat.pid == 2610)]..pid'

Get JSON document of said process subtree.

.. sourcecode::

   procpath query -i 2 '$..children[?(@.stat.pid == 2610)]'

Get total RSS in MiB of said process subtree (this is an example that
``query`` produces JSON that can be further processed outside of ``procpath``,
and below is a much easier way to calculate aggregates).

.. sourcecode::

   procpath query '$..children[?(@.stat.pid == 2610)]' \
     | jq '[.. | .stat? | objects | .rss] | add / 1024 * 4'

Get total RSS in MiB of said process subtree the easy way.

.. sourcecode::

   procpath record -d out.sqlite -r 1 '$..children[?(@.stat.pid == 2610)]'
   sqlite3 out.sqlite 'SELECT SUM(stat_rss) / 1024.0 * 4 FROM record'

Record process trees of two Docker containers once a second, re-evaluating the
containers' root process PIDs once per 30 recordings. Then visualise RSS of
each process (which is also just an example, that output SQLite database can
be visualised in different ways, including exporting CSV, ``sqlite3 -csv ...``,
and doing it the old way, to using proper UI described in Visualisation
section below).

.. sourcecode::

   procpath record \
     -e C1='docker inspect -f "{{.State.Pid}}" project_db_1' \
     -e C2='docker inspect -f "{{.State.Pid}}" project_app_1' \
     -i 1 -v 30 -d out.sqlite '$..children[?(@.stat.pid in [$C1, $C2])]'
   # press Ctrl + C
   sqlite3 out.sqlite \
     "SELECT stat_pid, group_concat(stat_rss / 1024.0 * 4) \
      FROM record \
      GROUP BY stat_pid" \
     | sed -z 's/\n/\n\n\n/g' | sed 's/|/\n/' | sed 's/,/\n/g' > special_fmt
   gnuplot -p -e \
     "plot for [i=0:*] 'special_fmt' index i with lines title columnheader(1)"

Visualisation
=============
This section describes two methods of visualisation of SQLite databases
produced by ``procpath record``.

Built-in
--------
Procpath comes with built-in SVG visualisation for the most basic temporal
process analysis tasks. Currently this includes RSS and CPU usage.

This example plots all processes' RSS from the recorded database, using
Ramer-Douglas-Peucker algorithm to remove redundant points from the SVG
with ε=0.5, and with moving average window of 10.

.. sourcecode::

   procpath plot -d out.sqlite -f rss.svg -q rss -e 0.5 -w 10

If opened in a browser alone this SVG has some interactivity. SVG is
produced by Pygal [13]_.

.. image:: https://bit.ly/3gUCbFp
   :alt: Procpath RSS SVG

It's possible to filter by time ranges and PIDs. It's also possible to use
custom SQL queries besides built-in ones, and change the style of the
visualisation. See the listing of ``procpath plot --help`` below.

Ad-hoc
------
A GUI-driven ad-hoc visualisation can be done in Plotly Falcon [11]_.
Instead of official raw Electron build, you can use this script to build
AppImage [10]_.

Ad-hoc visualisation in Falcon is straightforward.

1. Choose the SQLite database file
2. Enter the query (see examples in the section below) and run it
3. Switch to *CHART* tab
4. Click *+ TRACE*, select *Line* chart
5. Choose ``X = ts``
6. Choose ``Y`` to the the expression to plot, for instance, ``rss``
7. Switch to *Transforms*, *+ Transform* to add *Split* and choose ``stat_pid``

It should look like this.

.. image:: https://bit.ly/32TqF7Y
   :alt: Plotly Falcon screenshot

SQL query
---------
This section lists SQL queries to back the most basic temporal process
analysis tasks. Same queries with filters are used by ``procpath plot``.

1. RSS in MiB per process.

   .. sourcecode:: sql

      SELECT
        datetime(ts, 'unixepoch', 'localtime') ts,
        stat_pid,
        stat_rss / 1024.0 / 1024 * (SELECT value FROM meta WHERE key = 'page_size') rss
      FROM record

2. CPU usage percent per process.

   .. sourcecode:: sql

      WITH diff AS (
        SELECT
          ts,
          stat_pid,
          stat_utime + stat_stime - LAG(stat_utime + stat_stime) OVER (
            PARTITION BY stat_pid
            ORDER BY ts
          ) tick_diff,
          ts - LAG(ts) OVER (
            PARTITION BY stat_pid
            ORDER BY ts
          ) ts_diff
        FROM record
      )
      SELECT
        datetime(ts, 'unixepoch', 'localtime') ts,
        stat_pid,
        100.0 * tick_diff / (SELECT value FROM meta WHERE key = 'clock_ticks') / ts_diff cpu_load
      FROM diff

   .. note::

      1. Window function support was first added to SQLite with release
         version 3.25.0 (2018-09-15)
      2. The above only accounts for user and system time

Design
======
This section describes the problem and the solution in general. What preceded
Procpath and why it didn't solve the problem.

Problem statement
-----------------
On servers and desktops processes have become treelike long ago. For instance,
this is a process tree of Chromium browser with few opened tabs::

    chromium-browser ...
    ├─ chromium-browser --type=utility ...
    ├─ chromium-browser --type=gpu-process ...
    │  └─ chromium-browser --type=broker
    └─ chromium-browser --type=zygote
       └─ chromium-browser --type=zygote
          ├─ chromium-browser --type=renderer ...
          ├─ chromium-browser --type=renderer ...
          ├─ chromium-browser --type=renderer ...
          ├─ chromium-browser --type=renderer ...
          └─ chromium-browser --type=utility ...

On a server environment it can be substituted with a dozen of task queue worker
process trees, processes of the connection pool of a database, several
web-server process trees or anything-goes in a bunch of Docker containers.

This environment begs some operational questions, point-in-time and temporal.
When I have several trees like above, how do I know the (sub)tree's current
resource profile, like total main memory consumption, CPU time and so on? How
do I track these profiles in time when, for instance, I suspect a memory leak?
How to point other process analysis and introspection tools to these trees?

Existing approaches for outputting a tree's PIDs include applying bash-fu on
``pstree`` output [1]_ or nested ``pgrep`` for shallower cases. ``procps``
(providing ``top`` and ``ps``) is inadequate for any of above from embracing
process hierarchy to collecting temporal metrics. ``psmisc`` (providing
``pstree``) is only good for displaying the hierarchy, and doesn't
cover any programmatic interaction. ``htop`` is great for interactive
inspection of process trees with its filter and search, but for programmatic
interaction is also useless. ``glances`` has the JSON output feature, but it
doesn't have process-level granularity...

For process metrics collection alone (given you know the PIDs), ``sysstat``
(providing ``pidstat``) is likely the only simple solution, which still
requires some ad-hoc scripting [2]_.

Solution
--------
The solution lies in applying the right tool to the job principle.

1. Represent ``procfs`` [4]_ process tree as a tree structure.
2. Expose this structure to queries in a compact tree query language.
3. Flatten and store a query result in a ubiquitous format allowing for
   easy transmission and transformation.

A major non-functional requirement here is ease of installation, preferably in
the form of pure-python package. That's because an ad-hoc investigation may
not allow installing compiler toolchain on the target machine, which discards
``psutil`` and discourages XML as the tree representation format, as it would
require ``lxml`` for XPath.

Representation is relatively simple. Read all ``/proc/N/stat``, build the tree
and serialise it as JSON. The ubiquitous form is even simpler. SQLite!

The step in between is much less obvious. Discarding special graph query
languages and focusing on ones targeting JSON the list goes like this. But
it's unfortunately, taking into account the Python implementations, is not
about choosing the best requirement match, but about choosing the lesser evil.

1. JSONPath [5]_ and its Python port. Informal, regex-based (obscure error
   messages and edge-cases), what-if-XPath-worked-on-JSON prototype. Most
   popular non-regex Python implementation are a sequence of forks, none of
   which supports recursive descent. One grammar-based package would work [6]_,
   but its filter expressions are just Python ``eval``.
2. JSON Pointer [7]_. No recursive descent supported.
3. JMESPath (AWS ``boto`` dependency). No recursive descent supported [8]_.
4. ``jq`` and its Python bindings [9]_. ``jq`` is a programming language
   in disguise of JSON transformation CLI tool. Even though there's lengthy
   documentation, on occasional use ``jq`` feels very counter-intuitive and
   requires lot of googling and trial-and-error.

Pondering and playing with these, item 1 and ``JSONPyth`` [6]_ was the choice.
Filter Python expression syntax can be "jsonified" by the ``AttrDict`` idiom,
and the security concern of ``eval`` is justified by the CLI use cases.

Data model
----------
``procpath query`` outputs the ``pid=1`` process node with all its descendants
into stdout.

.. sourcecode:: json

   {
     "stat": {"pid": 1, "ppid": 0, ...}
     "cmdline": "root node",
     "other_stat_file": ...,
     "children": [
       {
         "cmdline": "cmdline of some process",
         "stat": {"pid": 1, "ppid": 323, ...},
         "other_stat_file": ...
       },
       {
         "cmdline": "cmdline of another process with children",
         "stat": {"pid": 1, "ppid": 324, ...},
         "other_stat_file": ...,
         "children": [...]
       },
       ...
     ]
   }

When JSONPath query is provided to the command, the output is a list of
process nodes. See more examples in the test suite.

When recorded into a SQLite database, schema is inferred from used procfs
files. The root node or the node list is flattened and recorded into the
``record`` table having the DDL like the following.

.. sourcecode:: sql

   CREATE TABLE record (
       record_id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       ts               REAL    NOT NULL,
       cmdline          TEXT,
       stat_pid         INTEGER,
       stat_comm        TEXT,
       ...
   )

Procpath doesn't pre-processes procfs data. For instance, ``rss`` is expressed
in pages, ``utime`` in clock ticks and so on. To properly interpret data in
``record`` table, there's also ``meta`` table containing the following
key-value records.

=====================  ============================
``platform_node``      ``platform.node()``
---------------------  ----------------------------
``platform_platform``  ``platform.platform()``
---------------------  ----------------------------
``page_size``          ``resource.getpagesize()``
                       typically 4096
---------------------  ----------------------------
``clock_ticks``        ``os.sysconf('SC_CLK_TCK')``
                       typically 100
=====================  ============================

Procpath supports ``stat``, ``cmdline`` and ``io`` procfs files. ``stat`` and
``cmdline`` are the default ones. Each procfs file field is described in
``procpath.procfile`` module [3]_.

Command-line interface
======================
.. sourcecode::

   $ procpath query --help
   usage: procpath query [-h] [-f PROCFILE_LIST] [-d DELIMITER] [-i INDENT]
                         [query]

   positional arguments:
     query                 JSONPath expression, for example this query returns
                           PIDs for process subtree including the given root's:
                           $..children[?(@.stat.pid == 2610)]..pid

   optional arguments:
     -h, --help            show this help message and exit
     -f PROCFILE_LIST, --procfile-list PROCFILE_LIST
                           PID proc files to read. By default: stat,cmdline.
                           Available: stat,cmdline,io.
     -d DELIMITER, --delimiter DELIMITER
                           Join query result using given delimiter
     -i INDENT, --indent INDENT
                           Format result JSON using given indent number

.. sourcecode::

   $ procpath record --help
   usage: procpath record [-h] [-f PROCFILE_LIST] [-e ENVIRONMENT]
                          [-i INTERVAL] [-r RECNUM] [-v REEVALNUM] -d
                          DATABASE_FILE
                          [query]

   positional arguments:
     query                 JSONPath expression, for example this query returns a
                           node including its subtree for given PID:
                           $..children[?(@.stat.pid == 2610)]

   optional arguments:
     -h, --help            show this help message and exit
     -f PROCFILE_LIST, --procfile-list PROCFILE_LIST
                           PID proc files to read. By default: stat,cmdline.
                           Available: stat,cmdline,io.
     -e ENVIRONMENT, --environment ENVIRONMENT
                           Commands to evaluate in the shell and template the
                           query, like VAR=date.
     -i INTERVAL, --interval INTERVAL
                           Interval in second between each recording, 10 by
                           default.
     -r RECNUM, --recnum RECNUM
                           Number of recordings to take at --interval seconds
                           apart. If not specified, recordings will be taken
                           indefinitely.
     -v REEVALNUM, --reevalnum REEVALNUM
                           Number of recordings after which environment must be
                           re-evaluate. It's useful when you expect it to change
                           in while recordings are taken.
     -d DATABASE_FILE, --database-file DATABASE_FILE
                           Path to the recording database file

.. sourcecode::

   $ path plot --help
   usage: procpath plot [-h] -d DATABASE_FILE [-f PLOT_FILE] [-q QUERY_NAME]
                        [-a AFTER] [-b BEFORE] [-p PID_LIST] [-e EPSILON]
                        [-w MOVING_AVERAGE_WINDOW] [--style STYLE]
                        [--title TITLE] [--custom-query-file CUSTOM_QUERY_FILE]

   optional arguments:
     -h, --help            show this help message and exit
     -d DATABASE_FILE, --database-file DATABASE_FILE
                           Path to the database file to read from.
     -f PLOT_FILE, --plot-file PLOT_FILE
                           Path to the output SVG file, plot.svg by default.
     -q QUERY_NAME, --query-name QUERY_NAME
                           Built-in query name. Available: rss,cpu.
     -a AFTER, --after AFTER
                           Include only points after given UTC date, like
                           2000-01-01T00:00:00.
     -b BEFORE, --before BEFORE
                           Include only points before given UTC date, like
                           2000-01-01T00:00:00.
     -p PID_LIST, --pid-list PID_LIST
                           Include only given PIDs.
     -e EPSILON, --epsilon EPSILON
                           Reduce points using Ramer-Douglas-Peucker algorithm
                           and given ε.
     -w MOVING_AVERAGE_WINDOW, --moving-average-window MOVING_AVERAGE_WINDOW
                           Smooth the lines using moving average.
     --style STYLE         Plot using given pygal.style, like LightGreenStyle.
     --title TITLE         Override plot title.
     --custom-query-file CUSTOM_QUERY_FILE
                           Use custom SQL query in given file. The result-set
                           must have 3 columns: ts, pid, value. See
                           procpath.procsql.

____

.. [1] https://unix.stackexchange.com/q/67668/124219
.. [2] https://stackoverflow.com/a/59182595/2072035
.. [3] https://heptapod.host/saajns/procpath/-/blob/branch/default/procpath/procfile.py
.. [4] https://en.wikipedia.org/wiki/Procfs
.. [5] https://goessner.net/articles/JsonPath/
.. [6] https://pypi.org/project/JSONPyth/
.. [7] https://tools.ietf.org/html/rfc6901
.. [8] https://github.com/jmespath/jmespath.py/issues/110
.. [9] https://pypi.org/project/jq/
.. [10] https://heptapod.host/saajns/procpath/snippets/4
.. [11] https://github.com/plotly/falcon
.. [12] https://pypi.org/project/pipx/
.. [13] https://pypi.org/project/pygal/
