from typing import NamedTuple
from datetime import datetime
from contextlib import closing

try:
    import apsw as sqlite
except ImportError:
    import sqlite3 as sqlite


__all__ = 'registry', 'query', 'Query'

registry = {}


class Query(NamedTuple):
    query: str
    title: str
    min_version: tuple = (1,)


registry['rss'] = Query(
    '''
    SELECT
        ts,
        stat_pid pid,
        stat_rss / 1024.0 / 1024 * (SELECT value FROM meta WHERE key = 'page_size') value
    FROM record
    WHERE
        (NOT :after OR :after <= ts)
        AND (NOT :before OR ts <= :before)
        AND (:pid_list == "" OR instr(:pid_list, stat_pid || ","))
    ORDER BY stat_pid, record_id
    ''',
    'Resident Set Size, MiB',
)

registry['cpu'] = Query(
    '''
    WITH diff AS (
        SELECT
            record_id,
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
        ts,
        stat_pid pid,
        100.0 * tick_diff / (SELECT value FROM meta WHERE key = 'clock_ticks') / ts_diff value
    FROM diff
    WHERE
        tick_diff IS NOT NULL
        AND (NOT :after OR :after <= ts)
        AND (NOT :before OR ts <= :before)
        AND (:pid_list == "" OR instr(:pid_list, stat_pid || ","))
    ORDER BY stat_pid, record_id
    ''',
    'CPU usage, %',
    min_version=(3, 25),
)


def query(
    database: str,
    query: Query,
    after: datetime = None,
    before: datetime = None,
    pid_list: list = None,
):
    conn = sqlite.Connection(database)
    cursor = conn.cursor()

    sqlite_version = cursor.execute('SELECT sqlite_version()').fetchone()[0]
    sqlite_version = tuple(map(int, sqlite_version.split('.')))
    if sqlite_version < query.min_version:
        raise RuntimeError(
            f'This query requires SQLite version >= {query.min_version}, '
            f'installed {sqlite_version}. Install apsw-wheels and try again.'
        )

    row_factory = lambda cur, row: dict(zip([t[0] for t in cur.description], row))
    try:
        conn.row_factory = row_factory
    except AttributeError:
        conn.setrowtrace(row_factory)

    with closing(conn):
        cursor = conn.cursor()
        cursor.execute(query.query, {
            'after': after.timestamp() if after else 0,
            'before': before.timestamp() if before else 0,
            'pid_list': '{},'.format(','.join(map(str, pid_list))) if pid_list else '',
        })
        return cursor.fetchall()
