import argparse
import logging
import sys
from datetime import datetime, timezone

from . import command, procfile, procret, __version__


logger = logging.getLogger(__package__)


def add_query_parser(parent):
    parser = parent.add_parser('query')
    parser.add_argument(
        '-f', '--procfile-list',
        default='stat,cmdline',
        type=lambda s: s.split(','),
        help=f'''
            PID proc files to read. By default: %(default)s.
            Available: {','.join(procfile.registry.keys())}.
        ''',
    )
    parser.add_argument(
        '-d', '--delimiter',
        help='Join query result using given delimiter',
    )
    parser.add_argument(
        '-i', '--indent',
        type=int,
        help='Format result JSON using given indent number',
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='''
            JSONPath expression, for example this query returns
            PIDs for process subtree including the given root's:

            $..children[?(@.stat.pid == 2610)]..pid
        '''
    )
    parser.set_defaults(output_file=sys.stdout)


def add_record_parser(parent):
    parser = parent.add_parser('record')
    parser.add_argument(
        '-f', '--procfile-list',
        default='stat,cmdline',
        type=lambda s: s.split(','),
        help=f'''
            PID proc files to read. By default: %(default)s.
            Available: {','.join(procfile.registry.keys())}.
        ''',
    )
    parser.add_argument(
        '-e', '--environment',
        action='append',
        type=lambda s: s.split('=', 1),
        help='Commands to evaluate in the shell and template the query, like VAR=date.',
    )
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default='10',
        help='Interval in second between each recording, %(default)s by default.',
    )
    parser.add_argument(
        '-r', '--recnum',
        type=int,
        help='''
            Number of recordings to take at --interval seconds apart.
            If not specified, recordings will be taken indefinitely.
        ''',
    )
    parser.add_argument(
        '-v', '--reevalnum',
        type=int,
        help='''
            Number of recordings after which environment must be re-evaluate.
            It's useful when you expect it to change in while recordings are
            taken.
        ''',
    )
    parser.add_argument(
        '-d', '--database-file',
        required=True,
        help='Path to the recording database file',
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='''
            JSONPath expression, for example this query returns
            a node including its subtree for given PID:

            $..children[?(@.stat.pid == 2610)]
        '''
    )


def add_plot_parser(parent):
    parser = parent.add_parser('plot')
    parser.add_argument(
        '-d', '--database-file',
        required=True,
        help='Path to the database file to read from.',
    )
    parser.add_argument(
        '-f', '--plot-file',
        default='plot.svg',
        help='Path to the output SVG file, plot.svg by default.',
    )
    parser.add_argument(
        '-q', '--query-name',
        default='cpu',
        help=f'Built-in query name. Available: {",".join(procret.registry.keys())}.',
    )
    parser.add_argument(
        '-a', '--after',
        type=lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc),
        help='Include only points after given UTC date, like 2000-01-01T00:00:00.',
    )
    parser.add_argument(
        '-b', '--before',
        type=lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc),
        help='Include only points before given UTC date, like 2000-01-01T00:00:00.',
    )
    parser.add_argument(
        '-p', '--pid-list',
        type=lambda s: list(map(int, s.split(','))),
        help='Include only given PIDs.',
    )
    parser.add_argument(
        '-e', '--epsilon',
        type=float,
        help='Reduce points using Ramer-Douglas-Peucker algorithm and given ε.',
    )
    parser.add_argument(
        '-w', '--moving-average-window',
        type=int,
        help='Smooth the lines using moving average.',
    )
    parser.add_argument(
        '--style',
        help='Plot using given pygal.style, like LightGreenStyle.',
    )
    parser.add_argument(
        '--title',
        help='Override plot title.',
    )
    parser.add_argument(
        '--custom-query-file',
        help='''
            Use custom SQL query in given file.
            The result-set must have 3 columns: ts, pid, value. See procpath.procsql.
        ''',
    )


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=__version__)

    parent = parser.add_subparsers(dest='command')
    [fn(parent) for fn in (add_query_parser, add_record_parser, add_plot_parser)]

    return parser


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(levelname)-7s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    parser = build_parser()
    kwargs = vars(parser.parse_args())
    # "required" keyword argument to add_subparsers() was added in py37
    if not kwargs.get('command'):
        parser.error('the following arguments are required: command')

    try:
        getattr(command, kwargs.pop('command'))(**kwargs)
    except KeyboardInterrupt:
        pass
    except command.CommandError as ex:
        logger.error(ex)
