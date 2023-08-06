import itertools
import json
import string
import time

import jsonpyth

from . import proctree, procfile, procrec, procret, utility


__all__ = 'CommandError', 'query', 'record'


class CommandError(Exception):
    """Generic command error."""


def query(procfile_list, output_file, delimiter=None, indent=None, query=None):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)
    result = tree.get_root()

    if query:
        try:
            result = jsonpyth.jsonpath(result, query, always_return_list=True)
        except jsonpyth.JsonPathSyntaxError as ex:
            raise CommandError(str(ex)) from ex

    if delimiter:
        result = delimiter.join(map(str, result))
    else:
        result = json.dumps(result, indent=indent, sort_keys=True, ensure_ascii=False)

    output_file.write(result)
    output_file.write('\n')


def record(
    procfile_list,
    database_file,
    interval,
    environment=None,
    query=None,
    recnum=None,
    reevalnum=None,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)

    count = 1
    query_tpl = string.Template(query)
    with procrec.SqliteStorage(database_file, procfile_list, utility.get_meta()) as store:
        while True:
            if (
                query_tpl.template
                and environment
                and (count == 1 or reevalnum and (count + 1) % reevalnum == 0)
            ):
                query = query_tpl.safe_substitute(utility.evaluate(environment))

            start = time.time()
            result = tree.get_root()
            if query:
                try:
                    result = jsonpyth.jsonpath(result, query, always_return_list=True)
                except jsonpyth.JsonPathSyntaxError as ex:
                    raise CommandError(str(ex)) from ex

            store.record(start, proctree.flatten(result, procfile_list))

            count += 1
            if recnum and count > recnum:
                break

            latency = time.time() - start
            time.sleep(max(0, interval - latency))


def plot(
    database_file,
    plot_file,
    query_name,
    after=None,
    before=None,
    pid_list=None,
    epsilon=None,
    moving_average_window=None,
    style=None,
    title=None,
    custom_query_file=None,
):
    if custom_query_file:
        with open(custom_query_file, 'r') as f:
            query = procret.Query(f.read(), title or 'Custom query')
    elif title:
        query = procret.registry[query_name]._replace(title=title)
    else:
        query = procret.registry[query_name]

    timeseries = procret.query(database_file, query, after, before, pid_list)
    pid_series = {}
    for pid, series in itertools.groupby(timeseries, lambda r: r['pid']):
        pid_series[pid] = [(r['ts'], r['value']) for r in series]
        if epsilon:
            pid_series[pid] = utility.decimate(pid_series[pid], epsilon)
        if moving_average_window:
            x, y = zip(*pid_series[pid])
            pid_series[pid] = list(zip(
                utility.moving_average(x, moving_average_window),
                utility.moving_average(y, moving_average_window),
            ))

    utility.plot(pid_series, plot_file, query.title, style)
