# Python Version: 3.x
# -*- coding: utf-8 -*-
import argparse
import pathlib
import sys
import traceback
from logging import DEBUG, INFO, StreamHandler, basicConfig, getLogger
from typing import List, Optional

import onlinejudge_command.__0_workaround_for_conflict  # pylint: disable=unused-import
import onlinejudge_command.__about__ as version
import onlinejudge_command.log_formatter as log_formatter
import onlinejudge_command.update_checking as update_checking
import onlinejudge_command.utils as utils
from onlinejudge_command.subcommand.download import download
from onlinejudge_command.subcommand.generate_input import generate_input
from onlinejudge_command.subcommand.generate_output import generate_output
from onlinejudge_command.subcommand.login import login
from onlinejudge_command.subcommand.submit import submit
from onlinejudge_command.subcommand.test import test
from onlinejudge_command.subcommand.test_reactive import test_reactive

import onlinejudge.__about__ as api_version

logger = getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Tools for online judge services')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-c', '--cookie', type=pathlib.Path, default=utils.default_cookie_path, help='path to cookie. (default: {})'.format(utils.default_cookie_path))
    parser.add_argument('--version', action='store_true', help='print the online-judge-tools version number')
    subparsers = parser.add_subparsers(dest='subcommand', help='for details, see "{} COMMAND --help"'.format(sys.argv[0]))

    # download
    subparser = subparsers.add_parser('download', aliases=['d', 'dl'], help='download sample cases', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
supported services:
  Anarchy Golf
  Aizu Online Judge (including the Arena)
  AtCoder
  Codeforces
  yukicoder
  CS Academy
  HackerRank
  PKU JudgeOnline
  Kattis
  Toph (Problem Archive)
  CodeChef
  Facebook Hacker Cup
  Google Code Jam
  Library Checker (https://judge.yosupo.jp/)

supported services with --system:
  Aizu Online Judge
  yukicoder
  Library Checker (https://judge.yosupo.jp/)

format string for --format:
  %i                    index: 1, 2, 3, ...
  %e                    extension: "in" or "out"
  %n                    name: e.g. "Sample Input 1", "system_test3.txt", ...
  %b                    os.path.basename(name)
  %d                    os.path.dirname(name)
  %%                    '%' itself
''')
    subparser.add_argument('url')
    subparser.add_argument('-f', '--format', help='a format string to specify paths of cases (default: "sample-%%i.%%e" if not --system)')  # default must be None for --system
    subparser.add_argument('-d', '--directory', type=pathlib.Path, help='a directory name for test cases (default: test/)')  # default must be None for guessing in submit command
    subparser.add_argument('-n', '--dry-run', action='store_true', help='don\'t write to files')
    subparser.add_argument('-a', '--system', action='store_true', help='download system testcases')
    subparser.add_argument('-s', '--silent', action='store_true')
    subparser.add_argument('--yukicoder-token', type=str)
    subparser.add_argument('--json', action='store_true')

    # login
    subparser = subparsers.add_parser('login', aliases=['l'], help='login to a service', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
supported services:
  AtCoder
  Codeforces
  yukicoder
  HackerRank
  Toph
''')
    subparser.add_argument('url')
    subparser.add_argument('-u', '--username')
    subparser.add_argument('-p', '--password')
    subparser.add_argument('--check', action='store_true', help='check whether you are logged in or not')
    subparser.add_argument('--use-browser', choices=('always', 'auto', 'never'), default='auto', help='specify whether it uses a GUI web browser to login or not  (default: auto)')

    # submit
    subparser = subparsers.add_parser('submit', aliases=['s'], help='submit your solution', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
supported services:
  AtCoder
  Codeforces
  yukicoder
  HackerRank
  Toph (Problem Archive)

''')
    subparser.add_argument('url', nargs='?', help='the URL of the problem to submit. if not given, guessed from history of download command.')
    subparser.add_argument('file', type=pathlib.Path)
    subparser.add_argument('-l', '--language', help='narrow down language choices if ambiguous')
    subparser.add_argument('--no-guess', action='store_false', dest='guess')
    subparser.add_argument('-g', '--guess', action='store_true', help='guess the language for your file (default)')
    subparser.add_argument('--no-guess-latest', action='store_false', dest='guess_cxx_latest')
    subparser.add_argument('--guess-cxx-latest', action='store_true', help='use the lasest version for C++ (default)')
    subparser.add_argument('--guess-cxx-compiler', choices=('gcc', 'clang', 'all'), default='gcc', help='use the specified C++ compiler if both of GCC and Clang are available (default: gcc)')
    subparser.add_argument('--guess-python-version', choices=('2', '3', 'auto', 'all'), default='auto', help='default: auto')
    subparser.add_argument('--guess-python-interpreter', choices=('cpython', 'pypy', 'all'), default='cpython', help='use the specified Python interpreter if both of CPython and PyPy are available (default: cpython)')
    subparser.add_argument('--format-dos2unix', action='store_true', help='replace CRLF with LF for given file')
    subparser.add_argument('--format-rstrip', action='store_true', help='remove trailing newlines from given file')
    subparser.add_argument('-G', '--golf', action='store_true', help='now equivalent to --format-dos2unix --format-rstrip')
    subparser.add_argument('--no-open', action='store_false', dest='open')
    subparser.add_argument('--open', action='store_true', default=True, help='open the result page after submission (default)')
    subparser.add_argument('-w', '--wait', metavar='SECOND', type=float, default=3, help='sleep before submitting')
    subparser.add_argument('-y', '--yes', action='store_true', help='don\'t confirm')

    # test
    subparser = subparsers.add_parser('test', aliases=['t'], help='test your code', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
format string for --format:
  %s                    name
  %e                    extension: "in" or "out"
  (both %s and %e are required.)

tips:
  You can do similar things with shell: e.g. `for f in test/*.in ; do echo $f ; diff <(./a.out < $f) ${f/.in/.out} ; done`
''')
    subparser.add_argument('-c', '--command', default='./a.out', help='your solution to be tested. (default: "./a.out")')
    subparser.add_argument('-f', '--format', default='%s.%e', help='a format string to recognize the relationship of test cases. (default: "%%s.%%e")')
    subparser.add_argument('-d', '--directory', type=pathlib.Path, default=pathlib.Path('test'), help='a directory name for test cases (default: test/)')
    subparser.add_argument('-m', '--display-mode', choices=['simple', 'side-by-side'], default='simple', help='mode to display an output with the correct answer (default: simple)')
    subparser.add_argument('-S', '--side-by-side', dest='display_mode', action='store_const', const='side-by-side', help='display an output and the correct answer with side by side mode (equivalent to --display-mode side-by-side)')
    subparser.add_argument('--no-rstrip', action='store_false', dest='rstrip')
    subparser.add_argument('--rstrip', action='store_true', help='rstrip output before compare (default)')
    subparser.add_argument('-s', '--silent', action='store_true', help='don\'t report output and correct answer even if not AC  (for --mode all)')
    subparser.add_argument('-e', '--error', type=float, help='check as floating point number: correct if its absolute or relative error doesn\'t exceed it')
    subparser.add_argument('-t', '--tle', type=float, help='set the time limit (in second) (default: inf)')
    subparser.add_argument('--mle', type=float, help='set the memory limit (in megabyte) (default: inf)')
    subparser.add_argument('-i', '--print-input', action='store_true', help='print input cases if not AC')
    subparser.add_argument('-j', '--jobs', metavar='N', type=int, help='specifies the number of jobs to run simultaneously  (default: no parallelization)')
    subparser.add_argument('--print-memory', action='store_true', help='print the amount of memory which your program used, even if it is small enough')
    subparser.add_argument('--gnu-time', help='used to measure memory consumption (default: "time")', default='time')
    subparser.add_argument('--no-ignore-backup', action='store_false', dest='ignore_backup')
    subparser.add_argument('--ignore-backup', action='store_true', help='ignore backup files and hidden files (i.e. files like "*~", "\\#*\\#" and ".*") (default)')
    subparser.add_argument('--json', action='store_true')
    subparser.add_argument('--judge-command', dest='judge', default=None, help='specify judge command instead of default diff judge. See https://online-judge-tools.readthedocs.io/en/master/introduction.en.html#test-for-special-forms-of-problem for details')
    subparser.add_argument('test', nargs='*', type=pathlib.Path, help='paths of test cases. (if empty: globbed from --format)')

    # generate output
    subparser = subparsers.add_parser('generate-output', aliases=['g/o'], help='generate output files from input and reference implementation', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
format string for --format:
  %s                    name
  %e                    extension: "in" or "out"
  (both %s and %e are required.)

tips:
  You can do similar things with shell: e.g. `for f in test/*.in ; do ./a.out < $f > ${f/.in/.out} ; done`
''')
    subparser.add_argument('-c', '--command', default='./a.out', help='your solution to be tested. (default: "./a.out")')
    subparser.add_argument('-f', '--format', default='%s.%e', help='a format string to recognize the relationship of test cases. (default: "%%s.%%e")')
    subparser.add_argument('-d', '--directory', type=pathlib.Path, default=pathlib.Path('test'), help='a directory name for test cases (default: test/)')
    subparser.add_argument('-t', '--tle', type=float, help='set the time limit (in second) (default: inf)')
    subparser.add_argument('-j', '--jobs', type=int, help='run tests in parallel')
    subparser.add_argument('test', nargs='*', type=pathlib.Path, help='paths of input cases. (if empty: globbed from --format)')
    subparser.add_argument('--no-ignore-backup', action='store_false', dest='ignore_backup')
    subparser.add_argument('--ignore-backup', action='store_true', help='ignore backup files and hidden files (i.e. files like "*~", "\\#*\\#" and ".*") (default)')

    # generate input
    subparser = subparsers.add_parser('generate-input', aliases=['g/i'], help='generate input files from given generator', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
format string for --format:
  %s                    name
  %e                    extension: "in" or "out"
  (both %d and %e are required.)

tips:
  You can do similar things with shell: e.g. `for i in {000..099} ; do ./generate.py > test/random-$i.in ; done`
''')
    subparser.add_argument('-f', '--format', default='%s.%e', help='a format string to recognize the relationship of test cases. (default: "%%s.%%e")')
    subparser.add_argument('-d', '--directory', type=pathlib.Path, default=pathlib.Path('test'), help='a directory name for test cases (default: test/)')
    subparser.add_argument('-t', '--tle', type=float, help='set the time limit (in second) (default: inf)')
    subparser.add_argument('-j', '--jobs', type=int, help='run tests in parallel')
    subparser.add_argument('--width', type=int, default=3, help='specify the width of indices of cases. (default: 3)')
    subparser.add_argument('--name', help='specify the base name of cases. (default: "random")')
    subparser.add_argument('-c', '--command', help='specify your solution to generate output')
    subparser.add_argument('--hack', help='specify your solution to be compared the reference solution given by --command')
    subparser.add_argument('generator', type=str, help='your program to generate test cases')
    subparser.add_argument('count', nargs='?', type=int, help='the number of cases to generate (default: 100)')

    # test reactive
    subparser = subparsers.add_parser('test-reactive', aliases=['t/r'], help='test for reactive problem', formatter_class=argparse.RawTextHelpFormatter, epilog='''\
''')
    subparser.add_argument('-c', '--command', default='./a.out', help='your solution to be tested. (default: "./a.out")')
    subparser.add_argument('judge', help='judge program using standard I/O')

    return parser


def run_program(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.version:
        print('online-judge-tools {} (+ online-judge-api-client {})'.format(version.__version__, api_version.__version__))
        sys.exit(0)
    logger.debug('args: %s', str(args))

    # print the version to use for user-supporting
    logger.info('online-judge-tools %s (+ online-judge-api-client %s)', version.__version__, api_version.__version__)

    if args.subcommand in ['download', 'd', 'dl']:
        download(args)
    elif args.subcommand in ['login', 'l']:
        login(args)
    elif args.subcommand in ['submit', 's']:
        submit(args)
    elif args.subcommand in ['test', 't']:
        test(args)
    elif args.subcommand in ['test-reactive', 't/r']:
        test_reactive(args)
    elif args.subcommand in ['generate-output', 'g/o']:
        generate_output(args)
    elif args.subcommand in ['generate-input', 'g/i']:
        generate_input(args)
    else:
        parser.print_help(file=sys.stderr)
        sys.exit(1)


def main(args: Optional[List[str]] = None) -> None:
    parser = get_parser()
    parsed = parser.parse_args(args=args)

    # configure the logger
    level = INFO
    if parsed.verbose:
        level = DEBUG
    handler = StreamHandler()
    handler.setFormatter(log_formatter.LogFormatter())
    basicConfig(level=level, handlers=[handler])

    # check update
    is_updated = update_checking.run()

    try:
        run_program(parsed, parser=parser)
    except NotImplementedError as e:
        logger.debug('\n' + traceback.format_exc())
        logger.error('NotImplementedError')
        logger.info('The operation you specified is not supported yet. Pull requests are welcome.')
        logger.info('see: https://github.com/online-judge-tools/oj')
        if not is_updated:
            logger.info('hint: try updating the version of online-judge-tools')
        sys.exit(1)
    except Exception as e:
        logger.debug('\n' + traceback.format_exc())
        logger.exception(str(e))
        if not is_updated:
            logger.info('hint: try updating the version of online-judge-tools')
        sys.exit(1)


if __name__ == '__main__':
    main()
