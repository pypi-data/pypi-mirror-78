import io
import os
import re
import sys
import math
import json
import time
import signal
import sqlite3
import datetime
import unittest
import tempfile
import multiprocessing
from unittest import mock
from contextlib import closing

from . import cli, command, procfile, procrec, procret, proctree, utility

try:
    import apsw
except ImportError:
    apsw = None


class TestUtility(unittest.TestCase):

    def test_evaluate(self):
        actual = utility.evaluate([
            ('A', 'date -I'),
            ('B', 'echo 42')
        ])
        self.assertEqual({'A': datetime.date.today().isoformat(), 'B': '42'}, actual)

    def test_get_meta(self):
        self.assertEqual(
            {'platform_node', 'platform_platform', 'page_size', 'clock_ticks'},
            utility.get_meta().keys(),
        )

    def test_get_line_distance(self):
        self.assertEqual(10, utility.get_line_distance((0, 0), (10, 0), (10, 0)))
        self.assertEqual(10, utility.get_line_distance((0, 0), (10, 0), (10, 10)))

        actual = utility.get_line_distance((90, 51), (34, 15), (-11, -51))
        self.assertAlmostEqual(25.9886, actual, delta=0.00001)

    def test_decimate(self):
        self.assertEqual([(1, 1)], utility.decimate([(1, 1)], 0))
        self.assertEqual([(1, 1), (1, 1)], utility.decimate([(1, 1), (1, 1)], 0))
        self.assertEqual([(1, 1), (1, 1)], utility.decimate([(1, 1), (1, 1), (1, 1)], 0))

        actual = utility.decimate([(1, 1), (2, 1.1), (3, 1)], 0.05)
        self.assertEqual([(1, 1), (2, 1.1), (3, 1)], actual)
        actual = utility.decimate([(1, 1), (2, 1.1), (3, 1)], 0.15)
        self.assertEqual([(1, 1), (3, 1)], actual)

        points = [(x / 10, math.log2(x)) for x in range(1, 100)]
        actual = utility.decimate(points, 0.3)
        expected = [
            (0.1, 0.0),
            (0.7, 2.807354922057604),
            (2.1, 4.392317422778761),
            (5.0, 5.643856189774724),
            (9.9, 6.6293566200796095),
        ]
        self.assertEqual(expected, actual)

    def test_moving_average(self):
        r = range(10)
        self.assertEqual(list(r), list(utility.moving_average(r, n=1)))

        expected = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]
        self.assertEqual(expected, list(utility.moving_average(r, n=2)))

        expected = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        self.assertEqual(expected, list(utility.moving_average(r, n=5)))

        expected = [4.5]
        self.assertEqual(expected, list(utility.moving_average(r, n=10)))

    def test_plot(self):
        pid_series = {
            309: [(0, 0), (10, 10), (15, 5)],
            2610: [(0, 0), (10, 10), (25, 10)],
        }
        with tempfile.NamedTemporaryFile() as f:
            utility.plot(pid_series, f.name, 'Visions', style=None)
            svg_bytes = f.read()

        self.assertIn(b'<svg', svg_bytes)
        self.assertIn(b'Visions', svg_bytes)
        self.assertIn(b'309', svg_bytes)
        self.assertIn(b'2610', svg_bytes)
        self.assertGreater(len(svg_bytes), 18000)

        with tempfile.NamedTemporaryFile() as f:
            utility.plot(pid_series, f.name, 'Visions', style='LightGreenStyle')
            svg_green_bytes = f.read()

        self.assertIn(b'<svg', svg_bytes)
        self.assertIn(b'Visions', svg_bytes)
        self.assertIn(b'309', svg_bytes)
        self.assertIn(b'2610', svg_bytes)
        self.assertGreater(len(svg_bytes), 18000)
        self.assertNotEqual(svg_bytes, svg_green_bytes)


class TestProctreeTree(unittest.TestCase):

    testee = None

    def setUp(self):
        self.testee = proctree.Tree(procfile.registry)

        node_list = get_chromium_node_list()
        proc_list = [{k: v for k, v in p.items() if k != 'children'} for p in node_list]
        proc_map = {proc['stat']['pid']: proc for proc in proc_list}
        proc_map[1] = {'stat': {'ppid': 0}}
        self.testee._read_process_dict = proc_map.__getitem__
        self.testee.get_pid_list = lambda: list(proc_map.keys()) + [os.getpid()]

    def test_get_pid_list(self):
        actual = proctree.Tree.get_pid_list()
        self.assertTrue(all(isinstance(v, int) for v in actual))
        self.assertEqual(actual, sorted(actual))

    def test_get_nodemap(self):
        expected = {p['stat']['pid']: p for p in get_chromium_node_list()}
        expected[1] = {'stat': {'ppid': 0}, 'children': [get_chromium_node_list()[0]]}
        actual = self.testee.get_nodemap()
        self.assertEqual(expected, actual)

    def test_get_root(self):
        expected = {'stat': {'ppid': 0}, 'children': [get_chromium_node_list()[0]]}
        actual = self.testee.get_root()
        self.assertEqual(expected, actual)

    def test_read_process_dict(self):
        testee = proctree.Tree(procfile.registry)
        actual = testee._read_process_dict(os.getpid())
        self.assertIn('stat', actual)
        self.assertIn('rss', actual['stat'])
        self.assertIn('cmdline', actual)
        self.assertIn('io', actual)
        self.assertIn('rchar', actual['io'])

        testee = proctree.Tree({'cmdline': procfile.registry['cmdline']})
        actual = testee._read_process_dict(os.getpid())
        self.assertEqual(['cmdline'], list(actual.keys()))

    def test_read_process_dict_permission_error(self):
        testee = proctree.Tree({'io': procfile.registry['io']})

        with self.assertLogs('procpath', 'WARNING') as ctx:
            actual = testee._read_process_dict(1)
        self.assertEqual(1, len(ctx.records))
        self.assertIn('Permission denied', ctx.records[0].message)

        self.assertEqual({'io': procfile.read_io.empty}, actual)  # @UndefinedVariable

    def test_get_root_do_not_skip_self(self):
        testee = proctree.Tree(procfile.registry, skip_self=False)
        proc_map = {
            1: {'stat': {'ppid': 0}},
            os.getpid(): {'stat': {'ppid': 1}}
        }
        testee._read_process_dict = proc_map.__getitem__
        testee.get_pid_list = lambda: list(proc_map.keys())

        expected = {'stat': {'ppid': 0}, 'children': [{'stat': {'ppid': 1}}]}
        self.assertEqual(expected, testee.get_root())

    def test_get_root_required_stat(self):
        testee = proctree.Tree({'io': procfile.registry['io']})
        with self.assertRaises(RuntimeError) as ctx:
            testee.get_root()
        self.assertEqual('stat file reader is required', str(ctx.exception))


class TestProctree(unittest.TestCase):

    def test_flatten(self):
        actual = proctree.flatten(get_chromium_node_list(), ['stat'])

        # trim for brevity
        for d in actual:
            for k in list(d.keys()):
                if k not in ('stat_pid', 'stat_rss', 'stat_state'):
                    d.pop(k)

        expected = [
            {'stat_pid': 18467, 'stat_rss': 53306, 'stat_state': 'S'},
            {'stat_pid': 18482, 'stat_rss': 13765, 'stat_state': 'S'},
            {'stat_pid': 18503, 'stat_rss': 27219, 'stat_state': 'S'},
            {'stat_pid': 18508, 'stat_rss': 20059, 'stat_state': 'S'},
            {'stat_pid': 18484, 'stat_rss': 3651, 'stat_state': 'S'},
            {'stat_pid': 18517, 'stat_rss': 4368, 'stat_state': 'S'},
            {'stat_pid': 18529, 'stat_rss': 19849, 'stat_state': 'S'},
            {'stat_pid': 18531, 'stat_rss': 26117, 'stat_state': 'S'},
            {'stat_pid': 18555, 'stat_rss': 63235, 'stat_state': 'S'},
            {'stat_pid': 18569, 'stat_rss': 18979, 'stat_state': 'S'},
            {'stat_pid': 18571, 'stat_rss': 8825, 'stat_state': 'S'},
            {'stat_pid': 18593, 'stat_rss': 22280, 'stat_state': 'S'},
            {'stat_pid': 18757, 'stat_rss': 12882, 'stat_state': 'S'},
            {'stat_pid': 18769, 'stat_rss': 54376, 'stat_state': 'S'},
            {'stat_pid': 18770, 'stat_rss': 31106, 'stat_state': 'S'},
            {'stat_pid': 18942, 'stat_rss': 27106, 'stat_state': 'S'},
        ]
        self.assertEqual(expected, actual)

    def test_flatten_single_value(self):
        actual = proctree.flatten(get_chromium_node_list(), ['cmdline'])

        renderer = {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...'}
        expected = [
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=gpu-process ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=broker'},
            renderer, renderer, renderer, renderer,
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...'},
            renderer, renderer, renderer, renderer, renderer,
        ]
        self.assertEqual(expected, actual)

    def test_attr_dict(self):
        ad = proctree.AttrDict({'a': 'b'})
        self.assertEqual('b', ad.a)


class TestProcrecSqliteStorage(unittest.TestCase):

    testeee = None

    def setUp(self):
        self.testee = procrec.SqliteStorage(':memory:', ['stat', 'cmdline'], {})

    def test_create_schema_all(self):
        testee = procrec.SqliteStorage(':memory:', ['stat', 'cmdline', 'io'], utility.get_meta())
        testee.create_schema()

        cursor = testee._conn.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite%'
        ''')
        self.assertEqual([('record',), ('meta',)], cursor.fetchall())

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'record'
        ''')
        expected = '''
            CREATE TABLE record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        REAL NOT NULL,
                cmdline TEXT,
                io_rchar INTEGER,
                io_wchar INTEGER,
                io_syscr INTEGER,
                io_syscw INTEGER,
                io_read_bytes INTEGER,
                io_write_bytes INTEGER,
                io_cancelled_write_bytes INTEGER,
                stat_pid INTEGER,
                stat_comm TEXT,
                stat_state TEXT,
                stat_ppid INTEGER,
                stat_pgrp INTEGER,
                stat_session INTEGER,
                stat_tty_nr INTEGER,
                stat_tpgid INTEGER,
                stat_flags INTEGER,
                stat_minflt INTEGER,
                stat_cminflt INTEGER,
                stat_majflt INTEGER,
                stat_cmajflt INTEGER,
                stat_utime INTEGER,
                stat_stime INTEGER,
                stat_cutime INTEGER,
                stat_cstime INTEGER,
                stat_priority INTEGER,
                stat_nice INTEGER,
                stat_num_threads INTEGER,
                stat_itrealvalue INTEGER,
                stat_starttime INTEGER,
                stat_vsize INTEGER,
                stat_rss INTEGER
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'meta'
        ''')
        expected = '''
            CREATE TABLE meta (
                key   TEXT PRIMARY KEY NOT NULL,
                value TEXT NOT NULL
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

        cursor = testee._conn.execute('SELECT * FROM meta')
        actual = dict(list(cursor))
        actual['page_size'] = int(actual['page_size'])
        actual['clock_ticks'] = int(actual['clock_ticks'])
        self.assertEqual(utility.get_meta(), actual)

    def test_create_schema_one(self):
        testee = procrec.SqliteStorage(':memory:', ['cmdline'], {})
        testee.create_schema()

        cursor = testee._conn.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite%'
        ''')
        self.assertEqual([('record',), ('meta',)], cursor.fetchall())

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'record'
        ''')
        expected = '''
            CREATE TABLE record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        REAL NOT NULL,
                cmdline   TEXT
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

    def test_record(self):
        ts = 1594483603.109486
        data = proctree.flatten(get_chromium_node_list(), self.testee._procfile_list)
        with self.testee:
            self.testee.record(ts, data)

            self.testee._conn.row_factory = sqlite3.Row
            cursor = self.testee._conn.execute('SELECT * FROM record')
            expected = [dict(d, record_id=i + 1, ts=ts) for i, d in enumerate(data)]
            self.assertEqual(expected, list(map(dict, cursor)))

        with self.assertRaises(sqlite3.ProgrammingError) as ctx:
            self.testee._conn.execute('SELECT * FROM record')
        self.assertEqual('Cannot operate on a closed database.', str(ctx.exception))

    def test_record_empty(self):
        ts = 1594483603.109486
        with self.testee:
            self.testee.record(ts, [])
            cursor = self.testee._conn.execute('SELECT * FROM record')
            self.assertEqual([], cursor.fetchall())


class TestProcret(unittest.TestCase):

    database_file = None

    @classmethod
    def setUpClass(cls):
        cls.database_file = tempfile.NamedTemporaryFile()
        cls.database_file.__enter__()

        storage = procrec.SqliteStorage(
            cls.database_file.name, ['stat', 'cmdline'], utility.get_meta()
        )
        data = proctree.flatten(get_chromium_node_list(), storage._procfile_list)
        with storage:
            for ts in range(1567504800, 1567504800 + 7200, 60):
                storage.record(ts, data)

    @classmethod
    def tearDownClass(cls):
        cls.database_file.close()

    def test_rss(self):
        rows = procret.query(self.database_file.name, procret.registry['rss'])
        self.assertEqual(1920, len(rows))
        self.assertEqual({'ts': 1567504800.0, 'pid': 18467, 'value': 208.2265625}, rows[0])

    def test_rss_filter_ts(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            after=datetime.datetime(2019, 9, 3, 10, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 11, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(976, len(rows))
        self.assertEqual({'ts': 1567506600.0, 'pid': 18467, 'value': 208.2265625}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            after=datetime.datetime(2019, 9, 3, 12, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 13, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual([], rows)

    def test_rss_filter_pid(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            pid_list=[18508, 18555, 18757],
        )
        self.assertEqual(360, len(rows))
        self.assertEqual({'pid': 18508, 'ts': 1567504800.0, 'value': 78.35546875}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            pid_list=[666],
        )
        self.assertEqual([], rows)

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_cpu(self):
        rows = procret.query(self.database_file.name, procret.registry['cpu'])
        self.assertEqual(1904, len(rows))
        self.assertEqual({'pid': 18467, 'ts': 1567504860.0, 'value': 0.0}, rows[0])

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_cpu_filter_ts(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            after=datetime.datetime(2019, 9, 3, 10, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 11, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(976, len(rows))
        self.assertEqual({'pid': 18467, 'ts': 1567506600.0, 'value': 0.0}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            after=datetime.datetime(2019, 9, 3, 12, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 13, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual([], rows)

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_cpu_filter_pid(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            pid_list=[18508, 18555, 18757],
        )
        self.assertEqual({'pid': 18508, 'ts': 1567504860.0, 'value': 0.0}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            pid_list=[666],
        )
        self.assertEqual([], rows)


class TestCli(unittest.TestCase):

    def test_build_parser_record(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'record',
            '-f', 'stat,cmdline',
            '-e', 'N=\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'',
            '-i', '10',
            '-r', '100',
            '-v', '25',
            '-d', 'db.sqlite',
            '$..children[?(@.stat.pid == $N)]',
        ]))
        expected = {
            'command': 'record',
            'procfile_list': ['stat', 'cmdline'],
            'environment': [['N', '\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'']],
            'interval': 10.0,
            'recnum': 100,
            'reevalnum': 25,
            'database_file': 'db.sqlite',
            'query': '$..children[?(@.stat.pid == $N)]',
        }
        self.assertEqual(expected, actual)

    def test_build_parser_query(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f', 'stat',
            '-d', ',',
            '$..children[?(@.stat.pid == 666)]..pid',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': ',',
            'indent': None,
            'query': '$..children[?(@.stat.pid == 666)]..pid',
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f', 'stat',
            '-i', '2',
            '$..children[?(@.stat.pid == 666)]..pid',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': None,
            'indent': 2,
            'query': '$..children[?(@.stat.pid == 666)]..pid',
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

    def test_build_parser_plot(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args(['plot', '-d', 'db.sqite']))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'plot.svg',
            'query_name': 'cpu',
            'after': None,
            'before': None,
            'pid_list': None,
            'epsilon': None,
            'moving_average_window': None,
            'style': None,
            'title': None,
            'custom_query_file': None,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'plot',
            '-d', 'db.sqite',
            '-f', 'rss.svg',
            '--query-name', 'rss',
            '-p', '1,2,3',
            '--epsilon', '26.1089',
            '-w', '10',
            '--style', 'LightGreenStyle',
            '--title', 'Visions',
        ]))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'rss.svg',
            'query_name': 'rss',
            'after': None,
            'before': None,
            'pid_list': [1, 2, 3],
            'epsilon': 26.1089,
            'moving_average_window': 10,
            'style': 'LightGreenStyle',
            'title': 'Visions',
            'custom_query_file': None,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'plot',
            '-d', 'db.sqite',
            '--title', 'Custom',
            '--after', '2000-01-01T00:00:00',
            '--before', '2020-01-01T00:00:00',
            '--custom-query-file', 'query.sql',
        ]))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'plot.svg',
            'query_name': 'cpu',
            'after': datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'before': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'pid_list': None,
            'epsilon': None,
            'moving_average_window': None,
            'style': None,
            'title': 'Custom',
            'custom_query_file': 'query.sql'
        }
        self.assertEqual(expected, actual)


class TestProcfile(unittest.TestCase):

    def test_read_stat(self):
        content = (
            b'32222 (python3.7) R 29884 337 337 0 -1 4194304 3765 0 1 0 19 3 0 '
            b'0 20 0 2 0 89851404 150605824 5255 18446744073709551615 4194304 '
            b'8590100 140727866261328 0 0 0 4 553652224 2 0 0 0 17 2 0 0 1 0 0 '
            b'10689968 11363916 15265792 140727866270452 140727866270792 '
            b'140727866270792 140727866273727 0\n'
        )
        expected = {
            'pid': 32222,
            'comm': 'python3.7',
            'state': 'R',
            'ppid': 29884,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194304,
            'minflt': 3765,
            'cminflt': 0,
            'majflt': 1,
            'cmajflt': 0,
            'utime': 19,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 2,
            'itrealvalue': 0,
            'starttime': 89851404,
            'vsize': 150605824,
            'rss': 5255
        }
        actual = procfile.read_stat(content)
        self.assertEqual(expected, actual)

    def test_read_cmdline(self):
        content = b'python3.7\x00-Wa\x00-u\x00'
        expected = 'python3.7 -Wa -u'
        actual = procfile.read_cmdline(content)
        self.assertEqual(expected, actual)

    def test_read_io(self):
        content = (
            b'rchar: 2274068\nwchar: 15681\nsyscr: 377\nsyscw: 10\nread_bytes: '
            b'0\nwrite_bytes: 20480\ncancelled_write_bytes: 0\n'
        )
        expected = {
            'rchar': 2274068,
            'wchar': 15681,
            'syscr': 377,
            'syscw': 10,
            'read_bytes': 0,
            'write_bytes': 20480,
            'cancelled_write_bytes': 0
        }
        actual = procfile.read_io(content)
        self.assertEqual(expected, actual)


class TestQueryCommand(unittest.TestCase):

    def test_query_query_node_list_json_output(self):
        output_file = io.StringIO()
        command.query(
            procfile_list=['stat'],
            output_file=output_file,
            indent=2,
            query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))

    def test_query_no_query_root_output(self):
        output_file = io.StringIO()
        command.query(
            procfile_list=['stat'],
            output_file=output_file,
        )
        root = json.loads(output_file.getvalue())
        self.assertEqual(1, root['stat']['pid'])

    def test_query_delimited(self):
        output_file = io.StringIO()
        command.query(
            procfile_list=['stat'],
            output_file=output_file,
            delimiter=',',
            query='$..children[?(@.stat.pid == {})]..pid'.format(os.getppid()),
        )
        pids = output_file.getvalue().split(',')
        self.assertGreaterEqual(len(pids), 1)
        self.assertEqual(os.getppid(), int(pids[0]))

    def test_query_syntax_error(self):
        with self.assertRaises(command.CommandError):
            command.query(procfile_list=['stat'], output_file=io.StringIO(), query='$!#')


class TestRecordCommand(unittest.TestCase):

    def test_record_query(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            command.record(
                procfile_list=['stat'],
                database_file=f.name,
                interval=1,
                recnum=1,
                query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            )
            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        actual = rows[0]
        self.assertEqual(1, actual.pop('record_id'))
        self.assertAlmostEqual(start, actual.pop('ts'), delta=0.1)

        self.assertEqual(os.getppid(), actual['stat_pid'])
        self.assertEqual(
            list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in actual.keys()],
        )

    def test_record_all(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            command.record(
                procfile_list=['stat', 'cmdline'],
                database_file=f.name,
                interval=1,
                recnum=1,
            )
            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        root = rows[0]
        self.assertEqual(1, root.pop('record_id'))
        self.assertAlmostEqual(start, root.pop('ts'), delta=0.1)

        self.assertEqual(1, root['stat_pid'])
        self.assertEqual(
            ['cmdline'] + list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in root.keys()],
        )

    @classmethod
    def record_forever(cls, database_file, pid):
        try:
            command.record(
                procfile_list=['stat'],
                database_file=database_file,
                interval=0.1,
                query=f'$..children[?(@.stat.pid == {pid})]',
            )
        except KeyboardInterrupt:
            pass

    def test_record_forever(self):
        with tempfile.NamedTemporaryFile() as f:
            p = multiprocessing.Process(target=self.record_forever, args=(f.name, os.getppid()))
            start = time.time()
            p.start()

            time.sleep(0.6)
            os.kill(p.pid, signal.SIGINT)
            p.join()

            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))

        self.assertGreaterEqual(sum(1 for r in rows if r['stat_pid'] == os.getppid()), 5)
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_n_times(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            command.record(
                procfile_list=['stat'],
                database_file=f.name,
                interval=0.01,
                recnum=4,
                query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            )
            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))

        self.assertEqual(4, sum(1 for r in rows if r['stat_pid'] == os.getppid()))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_environment(self):
        with tempfile.NamedTemporaryFile() as f:
            with tempfile.NamedTemporaryFile() as f_log:
                start = time.time()
                command.record(
                    procfile_list=['stat'],
                    database_file=f.name,
                    interval=0.01,
                    recnum=4,
                    reevalnum=2,
                    environment=[['P', 'echo {} | tee -a {}'.format(os.getppid(), f_log.name)]],
                    query='$..children[?(@.stat.pid == $P)]',
                )
                self.assertEqual(''.join(['{}\n'.format(os.getppid())] * 2).encode(), f_log.read())

                with closing(sqlite3.connect(f.name)) as conn:
                    conn.row_factory = sqlite3.Row

                    cursor = conn.execute('SELECT * FROM record')
                    rows = list(map(dict, cursor))

        self.assertEqual(4, sum(1 for r in rows if r['stat_pid'] == os.getppid()))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_syntax_error(self):
        with self.assertRaises(command.CommandError):
            command.record(
                procfile_list=['stat'], database_file=':memory:', interval=1, query='$!#'
            )


class TestPlotCommand(unittest.TestCase):

    database_file = None

    @classmethod
    def setUpClass(cls):
        cls.database_file = tempfile.NamedTemporaryFile()
        cls.database_file.__enter__()

        storage = procrec.SqliteStorage(cls.database_file.name, ['stat'], utility.get_meta())
        data = proctree.flatten(get_chromium_node_list(), storage._procfile_list)
        with storage:
            for ts in range(1567504800, 1567504800 + 4):
                storage.record(ts, data)

    @classmethod
    def tearDownClass(cls):
        cls.database_file.close()

    def test_plot(self):
        with tempfile.NamedTemporaryFile() as plot:
            command.plot(self.database_file.name, plot.name, query_name='rss')

            svg_bytes = plot.read()
            self.assertIn(b'<svg', svg_bytes)
            self.assertIn(b'Resident Set Size, MiB', svg_bytes)
            self.assertGreater(len(svg_bytes), 15_000)

    @mock.patch('procpath.command.utility.plot')
    def test_plot_title_override(self, plot):
        command.plot(
            self.database_file.name,
            '/fake',
            query_name='rss',
            pid_list=[18467],
            title='The Strain',
        )
        plot.assert_called_once_with(
            {18467: [
                (1567504800.0, 208.2265625),
                (1567504801.0, 208.2265625),
                (1567504802.0, 208.2265625),
                (1567504803.0, 208.2265625),
            ]},
            '/fake',
            'The Strain',
            None,
        )

    @mock.patch('procpath.command.utility.plot')
    def test_plot_custom_query_file(self, plot):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'''
                SELECT 1 ts, 2 pid, 3 value
                UNION
                SELECT 2 ts, 2 pid, 4 value
            ''')
            f.seek(0)

            command.plot(
                self.database_file.name,
                '/fake',
                query_name='rss',
                custom_query_file=f.name,
            )
            plot.assert_called_once_with({2: [(1, 3), (2, 4)]}, '/fake', 'Custom query', None)

    @mock.patch('procpath.command.utility.plot')
    def test_plot_rdp_epsilon(self, plot):
        command.plot(
            self.database_file.name,
            '/fake',
            query_name='rss',
            pid_list=[18467],
            epsilon=0.1,
        )
        plot.assert_called_once_with(
            {18467: [
                (1567504800.0, 208.2265625),
                (1567504803.0, 208.2265625)
            ]},
            '/fake',
            'Resident Set Size, MiB',
            None,
        )

    @mock.patch('procpath.command.utility.plot')
    def test_plot_moving_average_window(self, plot):
        command.plot(
            self.database_file.name,
            '/fake',
            query_name='rss',
            pid_list=[18467],
            moving_average_window=2,
        )
        plot.assert_called_once_with(
            {18467: [
                (1567504800.5, 208.2265625),
                (1567504801.5, 208.2265625),
                (1567504802.5, 208.2265625)
            ]},
            '/fake',
            'Resident Set Size, MiB',
            None,
        )


def get_chromium_node_list():
    """
    Get procpath search sample of Chromium browser process tree.

    ::

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
              ├─ chromium-browser --type=utility ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              └─ chromium-browser --type=renderer ...

    """

    pid_18467 = {
        'stat': {
            'pid': 18467,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 1,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194560,
            'minflt': 51931,
            'cminflt': 24741,
            'majflt': 721,
            'cmajflt': 13,
            'utime': 455,
            'stime': 123,
            'cutime': 16,
            'cstime': 17,
            'priority': 20,
            'nice': 0,
            'num_threads': 40,
            'itrealvalue': 0,
            'starttime': 62870630,
            'vsize': 2981761024,
            'rss': 53306,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser ...',
    }
    pid_18482 = {
        'stat': {
            'pid': 18482,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194560,
            'minflt': 3572,
            'cminflt': 0,
            'majflt': 49,
            'cmajflt': 0,
            'utime': 3,
            'stime': 2,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870663,
            'vsize': 460001280,
            'rss': 13765,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote',
    }
    pid_18484 = {
        'stat': {
            'pid': 18484,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18482,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194624,
            'minflt': 278,
            'cminflt': 4862,
            'majflt': 0,
            'cmajflt': 15,
            'utime': 0,
            'stime': 1,
            'cutime': 27,
            'cstime': 4,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870674,
            'vsize': 460001280,
            'rss': 3651,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote',
    }
    pid_18529 = {
        'stat': {
            'pid': 18529,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 3285,
            'cminflt': 0,
            'majflt': 78,
            'cmajflt': 0,
            'utime': 16,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870743,
            'vsize': 5411180544,
            'rss': 19849,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18531 = {
        'stat': {
            'pid': 18531,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 18231,
            'cminflt': 0,
            'majflt': 183,
            'cmajflt': 0,
            'utime': 118,
            'stime': 18,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870744,
            'vsize': 16164175872,
            'rss': 26117,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18555 = {
        'stat': {
            'pid': 18555,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 62472,
            'cminflt': 0,
            'majflt': 136,
            'cmajflt': 0,
            'utime': 1166,
            'stime': 59,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 14,
            'itrealvalue': 0,
            'starttime': 62870769,
            'vsize': 14124892160,
            'rss': 63235,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18569 = {
        'stat': {
            'pid': 18569,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 2695,
            'cminflt': 0,
            'majflt': 8,
            'cmajflt': 0,
            'utime': 7,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 11,
            'itrealvalue': 0,
            'starttime': 62870779,
            'vsize': 5407739904,
            'rss': 18979,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18571 = {
        'stat': {
            'pid': 18571,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 930,
            'cminflt': 0,
            'majflt': 20,
            'cmajflt': 0,
            'utime': 6,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 5,
            'itrealvalue': 0,
            'starttime': 62870781,
            'vsize': 5057503232,
            'rss': 8825,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...',
    }
    pid_18593 = {
        'stat': {
            'pid': 18593,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 12212,
            'cminflt': 0,
            'majflt': 2,
            'cmajflt': 0,
            'utime': 171,
            'stime': 11,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870786,
            'vsize': 5419442176,
            'rss': 22280,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18757 = {
        'stat': {
            'pid': 18757,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 1624,
            'cminflt': 0,
            'majflt': 0,
            'cmajflt': 0,
            'utime': 2,
            'stime': 0,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 11,
            'itrealvalue': 0,
            'starttime': 62871186,
            'vsize': 5389012992,
            'rss': 12882
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...'
    }
    pid_18769 = {
        'stat': {
            'pid': 18769,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 78483,
            'cminflt': 0,
            'majflt': 3,
            'cmajflt': 0,
            'utime': 906,
            'stime': 34,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871227,
            'vsize': 5497511936,
            'rss': 54376,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18770 = {
        'stat': {
            'pid': 18770,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 24759,
            'cminflt': 0,
            'majflt': 2,
            'cmajflt': 0,
            'utime': 260,
            'stime': 15,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871228,
            'vsize': 5438599168,
            'rss': 31106,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18942 = {
        'stat': {
            'pid': 18942,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 12989,
            'cminflt': 0,
            'majflt': 16,
            'cmajflt': 0,
            'utime': 77,
            'stime': 5,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871410,
            'vsize': 5436309504,
            'rss': 27106,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18503 = {
        'stat': {
            'pid': 18503,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194304,
            'minflt': 14361,
            'cminflt': 0,
            'majflt': 46,
            'cmajflt': 0,
            'utime': 112,
            'stime': 21,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 6,
            'itrealvalue': 0,
            'starttime': 62870711,
            'vsize': 877408256,
            'rss': 27219,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=gpu-process ...',
    }
    pid_18517 = {
        'stat': {
            'pid': 18517,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18503,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194368,
            'minflt': 86,
            'cminflt': 0,
            'majflt': 0,
            'cmajflt': 0,
            'utime': 0,
            'stime': 0,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870723,
            'vsize': 524230656,
            'rss': 4368,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=broker',
    }
    pid_18508 = {
        'stat': {
            'pid': 18508,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936128,
            'minflt': 9993,
            'cminflt': 0,
            'majflt': 55,
            'cmajflt': 0,
            'utime': 151,
            'stime': 47,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870714,
            'vsize': 1302757376,
            'rss': 20059,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...',
    }

    return [
        {
            **pid_18467,
            'children': [
                {
                    **pid_18482,
                    'children': [
                        {
                            **pid_18484,
                            'children': [
                                pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                                pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
                            ]
                        }
                    ]
                },
                {
                    **pid_18503,
                    'children': [pid_18517]
                },
                pid_18508
            ]
        },
        {
            **pid_18482,
            'children': [
                {
                    **pid_18484,
                    'children': [
                        pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                        pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
                    ]
                }
            ]
        },
        {
            **pid_18503,
            'children': [pid_18517]
        },
        pid_18508,
        {
            **pid_18484,
            'children': [
                pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
            ]
        },
        pid_18517,
        pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
        pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
    ]
