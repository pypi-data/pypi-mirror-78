import csv
import json
import os
from datetime import datetime

import click
from tabulate import tabulate

from ptoolbox.airtable.airtable import Airtable
from ptoolbox.beestar.beestar import Beestar
from ptoolbox.codeforces.codeforces import Codeforces
from ptoolbox.codesignal.codesignal import Codesignal
from ptoolbox.dsa import dsa_problem_file
from ptoolbox.dsa.dsa_problem import DsaProblem
from ptoolbox.hackerrank import hackerrank
from ptoolbox.hackerrank.hackerrank import HackerRank
from ptoolbox.helpers.clog import CLog
from ptoolbox.helpers.dsa_helper import read_all_problems
from ptoolbox.kattis.kattis import Kattis
from ptoolbox.logiclike.logiclike import LogicLike
from ptoolbox.ucode.ucode import UCode


@click.group()
def cli():
    """
    Problem Toolbox - Problem CLI tools by Thuc Nguyen (https://github.com/thucnc)
    """
    click.echo("Problem Toolbox - Problem CLI tools by Thuc Nguyen (https://github.com/thucnc)")


@cli.group(name='cs')
def codesignal_group():
    """
    codesignal tools
    """
    click.echo("codesignal problem tools")


@cli.group(name='lgl')
def logiclike_group():
    """
    logic like problem tools
    """
    click.echo("logiclike problem tools")


@cli.group(name='bs')
def beestar_group():
    """
    beestar problem tools
    """
    click.echo("beestar problem tools")


@cli.group(name='ucode')
def ucode_group():
    """
    ucode problem tools
    """
    click.echo("ucode problem tools")


@cli.group(name='dsa')
def dsa_group():
    """
    DSA problem tools
    """
    click.echo("Common DSA tools")


@cli.group(name='cf')
def codeforces_group():
    """
    Codeforces tools
    """
    click.echo("codeforces.com tools")


@cli.group(name='hr')
def hackerrank_group():
    """
    Hackerrank tools
    """
    click.echo("hackerrank.com tools")


@cli.group(name='kt')
def kattis_group():
    """
    Kattis tools
    """
    click.echo("kattis.com tools")


@dsa_group.command(name='create')
@click.option('-d', '--dir', default='.',
              type=click.Path(file_okay=False),
              help='Base folder for the problem')
@click.option('--overwrite/--no-overwrite', default=False, help='Overwrite existing folder, default - No')
@click.argument('problem', metavar='{problem}')
def create_problem(dir, overwrite, problem):
    """
    Create a problem boilerplate

    Syntax:
    ptoolbox dsa create-problem -d {folder} {problem-code} [--overwrite]

    Ex.:
    ptoolbox dsa create-problem -d problems/ prob2 --overwrite

    """
    dsa_problem_file.create_problem(dir, problem, overwrite=overwrite)


@dsa_group.command(name='check')
@click.option('--autofix/--no-auto-fix', default=False, help='Auto fix style, save original file to .bak.md, default - No')
@click.argument('problem_folder', metavar='{problem_folder}')
def check_problem(autofix, problem_folder):
    """
    Check problem folder for proper format

    Syntax:
    ptoolbox dsa check-problem {problem-folder}

    Ex.:
    ptoolbox dsa check-problem ../problems/prob2

    """
    dsa_problem_file.check_problem(problem_folder, autofix)


@codeforces_group.command(name='get')
@click.option('-d', '--dir', default='.',
              type=click.Path(file_okay=False),
              help='Base folder for the problem')
@click.option('-c', '--code', default='',
              help='Problem code, use as problem folder name, leave empty by default for auto generation from name')
@click.argument('url', metavar='{problem_url-or-problem_id}')
def get_codeforces_problem(dir, code, url):
    """
    Get a codeforces problem and save as to a local folder

    Syntax:
    ptoolbox cf get [-d {folder}] [-c {problem-code}] {codeforces-problem-url-or-id}

    Ex.:
    ptoolbox cf get -d problems/ https://codeforces.com/problemset/problem/1257/D
    or:
    ptoolbox cf get -d problems/ -c "Monster Killing" 1257D
    or:
    ptoolbox cf get -d problems/ 1257/D

    """
    cf = Codeforces()
    dsa_problem = cf.get_problem_from_url(url)
    DsaProblem.save(dsa_problem, dir, code, overwrite=False)


@kattis_group.command(name='get')
@click.option('-d', '--dir', default='.',
              type=click.Path(file_okay=False),
              help='Base folder for the problem')
@click.option('-c', '--code', default='',
              help='Problem code, use as problem folder name, leave empty by default for auto generation from name')
@click.argument('slug', metavar='{kattis-problem_slug}')
def get_kattis_problem(dir, code, slug):
    """
    Get a codeforces problem and save as to a local folder

    Syntax:
    ptoolbox cf get [-d {folder}] [-c {problem-code}] {kattis-problem-id}

    Ex.:
    ptoolbox cf get -d problems/ -c "Monster Killing" pieceofcake2
    """
    kt = Kattis()
    dsa_problem = kt.get_problem(slug)
    DsaProblem.save(dsa_problem, dir, code, overwrite=False)


@hackerrank_group.command()
@click.option('--keep-zip-file-only/--keep-intermediate-files', default=True,
              help='Remove intermediate files, default - Yes')
@click.argument('problem_folder', metavar='{problem_folder}')
def prepare_testcases(keep_zip_file_only, problem_folder):
    """
    Convert testcases to hackerrank format, and compress into .zip file, ready for upload

    Syntax:
    ptoolbox hackerrank prepare-testcases  {problem-folder} [--keep-zip-file-only/--keep-intermediate-files]

    Ex.:
    ptoolbox hackerrank prepare-testcases problems/prob2

    """
    hackerrank.prepare_testcases(problem_folder, keep_zip_file_only=keep_zip_file_only)


@hackerrank_group.command(name="create")
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True),
              prompt='Credential file', help='Configuration file that contain hackerrank user name/pass')
@click.option('--with-testcases/--without-testcases', default=True, help='Upload testcases')
@click.option('-w', '--weight', default=100, type=click.INT, help='Weight (score) of each testcase')
@click.option('-s', '--sample', default=1, type=click.INT, help='Number of sample testcases')
@click.argument('problem_folder', metavar='{problem_folder}')
def create_problem(credential, with_testcases, weight, sample, problem_folder):
    """
    Create problem description on hackerrank

    Syntax:
    ptoolbox hackerrank create-problem [--upload-testcases] {dsa_problem_folder}

    Ex.:
    ptoolbox hackerrank create-problem problems/array001_counting_sort3/

    """
    username, password = HackerRank.read_credential(credential)
    if not username or not password:
        CLog.error(f'Username and/or password are missing in {credential} file')
        return

    hr = HackerRank()
    hr.login(username, password)

    problem1 = DsaProblem.load(problem_folder)
    hk_problem = hr.create_problem(problem1)

    if hk_problem and with_testcases:
        _do_upload_testcases(username, password, weight, sample, hk_problem["id"], problem_folder)

    # print(hk_problem)

    if problem1:
        CLog.important(f'Problem `{hk_problem["id"]}` updated, slug: {hk_problem["slug"]}')


@hackerrank_group.command(name="update")
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True),
              prompt='Credential file', help='Configuration file that contain hackerrank user name/pass')
@click.argument('hackerrank_problem_id', metavar='{hackerrank_problem_id}')
@click.argument('problem_folder', metavar='{problem_folder}')
def update_problem(credential, hackerrank_problem_id, problem_folder):
    """
    Update problem description on hackerrank

    Syntax:
    ptoolbox hackerrank update-problem {hackerrank_problem_id} {dsa_problem_folder}

    Ex.:
    ptoolbox hackerrank update-problem 113357 problems/array001_counting_sort3/

    """
    username, password = HackerRank.read_credential(credential)
    if not username or not password:
        CLog.error(f'Username and/or password are missing in {credential} file')
        return

    hr = HackerRank()
    hr.login(username, password)

    problem1 = DsaProblem.load(problem_folder)

    hk_problem = hr.update_problem(hackerrank_problem_id, problem1)

    # print(hk_problem)

    if problem1:
        CLog.important(f'Problem `{hk_problem["id"]}` updated, slug: `{hk_problem["slug"]}`')


def _do_upload_testcases(username, password, weight, sample, hackerrank_problem_id, problem_folder):
    testcase_zip = os.path.join(problem_folder, 'testcases_hackerrank.zip')

    if not os.path.exists(testcase_zip):
        CLog.error(f'`{testcase_zip}` does not exist, '
                   f'please run `ptoolbox hackerrank prepare-testcases {problem_folder}` first')
        return

    hr = HackerRank()
    hr.login(username, password)
    created_testcases = hr.upload_testcases_and_set_score(hackerrank_problem_id, testcase_zip, weight, sample)

    print(created_testcases)

    if created_testcases:
        CLog.important(f'{len(created_testcases)} test cases uploaded to problem `{hackerrank_problem_id}`')


@hackerrank_group.command()
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True),
              prompt='Credential file', help='Configuration file that contain hackerrank user name/pass')
@click.option('-w', '--weight', default=100, type=click.INT, help='Weight (score) of each testcase')
@click.option('-s', '--sample', default=1, type=click.INT, help='Number of sample testcases')
@click.argument('hackerrank_problem_id', metavar='{hackerrank_problem_id}')
@click.argument('problem_folder', metavar='{problem_folder}')
def upload_testcases(credential, weight, sample, hackerrank_problem_id, problem_folder):
    """
    Upload testcases_hackerrank.zip to problem on hackerrank

    Syntax:
    ptoolbox hackerrank upload-testcases -w {weight} -s {sample_count} {hackerrank_problem_id} {dsa_problem_folder}

    Ex.:
    ptoolbox hackerrank upload-testcases -w 100 -s 2 113357 problems/array001_counting_sort3/

    """
    username, password = HackerRank.read_credential(credential)
    if not username or not password:
        CLog.error(f'Username and/or password are missing in {credential} file')
        return

    _do_upload_testcases(username, password, weight, sample, hackerrank_problem_id, problem_folder)


@ucode_group.command(name="create")
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True),
              prompt='Credential file', help='Configuration file that contain hackerrank user name/pass')
@click.option('-l', '--lesson', type=click.INT, help='Lesson id')
@click.option('-s', '--score', default=100, type=click.INT, help='Score of this question')
@click.option('-x', '--xp', default=100, type=click.INT, help='XP of this question')
@click.argument('problem_folder', metavar='{problem_folder}')
def ucode_create_problem(lesson, credential, score, problem_folder, xp):
    """
    Create problem on ucode.vn

    Syntax:
    ptoolbox ucode create-problem [--upload-testcases] -l {lesson_id} -s {score} {dsa_problem_folder}

    """
    api_url, token = UCode.read_credential(credential)
    if not api_url or not token:
        CLog.error(f'Username and/or password are missing in {credential} file')
        return

    ucode = UCode(api_url, token)

    problem = DsaProblem.load(problem_folder, load_testcase=True)
    problem_id = ucode.create_problem(lesson, problem, score=score, xp=xp)

    if problem:
        CLog.important(f'Problem `{problem_id}` created')


@ucode_group.command(name="create-multiple")
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True),
              prompt='Credential file', help='Configuration file that contain hackerrank user name/pass')
@click.option('-l', '--lesson', type=click.INT, help='Lesson id')
@click.option('-s', '--score', default=100, type=click.INT, help='Score of this question')
@click.option('-x', '--xp', default=100, type=click.INT, help='XP of this question')
@click.argument('base_folder', metavar='{base_folder}')
def ucode_create_problems(lesson, credential, score, base_folder, xp):
    """
    Create multiple problems on ucode.vn

    Syntax:
    ptoolbox ucode create-problem [--upload-testcases] -l {lesson_id} -s {score} {dsa_problem_folder}

    """
    api_url, token = UCode.read_credential(credential)
    if not api_url or not token:
        CLog.error(f'Username and/or password are missing in {credential} file')
        return

    ucode = UCode(api_url, token)

    problems = read_all_problems(base_folder, load_testcase=True)

    for problem_tuple in problems:
        problem = problem_tuple[1]
        problem_id = ucode.create_problem(lesson, problem, score=score, xp=xp)
        if problem:
            CLog.important(f'Problem `{problem_id}` created')


@beestar_group.command(name="getall")
@click.option('-u', '--username', type=click.STRING, help='beestar username')
@click.option('-p', '--password', type=click.STRING, help='beestar password')
@click.option('-o', '--output', default='.',
              type=click.Path(file_okay=False, exists=True), help='Output folder')
@click.option('-h', '--history', is_flag=True, help='get past quizzes')
def beestar_get_all(username, password, output, history):
    """
    sample:
    ptoolbox bs getall -u email -p pass -o beestar
    """

    beestar = Beestar()
    beestar.get_all_quizzes(username, password, output, history)


@beestar_group.command(name="upload_quiz_to_ucode")
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True),
              prompt='Credential file', help='Configuration file that contain ucode api/token')
@click.option('-k', '--course', type=click.INT, help='Course id')
@click.option('-s', '--chapter', type=click.INT, help='Chapter id')
@click.argument('filename', metavar='{beestar_quiz_html_file}')
def beestar_quiz_to_ucode(credential, course, chapter, filename):
    """
    sample:
    ptoolbox bs upload_quiz_to_ucode -c credentials.ini -k 17 -s 413 problems/beestar/beestar-grade-3-math-exercise-results-week-17-ex-1-spring-2020_ans.html
    """

    api_url, token = UCode.read_credential(credential)
    if not api_url or not token:
        CLog.error(f'Username and/or password are missing in {credential} file')
        return

    ucode = UCode(api_url, token)
    #
    lesson_id = ucode.create_lesson_item_from_beestar_file(course_id=course, chapter_id=chapter, beestar_file=filename)


@logiclike_group.command(name="get")
@click.option('-u', '--username', type=click.STRING, help='Username')
@click.option('-p', '--password', type=click.STRING, help='Password')
@click.option('-o', '--output', default='.',
              type=click.Path(file_okay=False, exists=True),
              help='output folder')
@click.argument('chapter_id', metavar='{chapter_id}')
def logiclike_get_full_chapter(username, password, chapter_id, output):
    """
    sample: ptoolbox lgl get -u thucngch@gmail.com -p 183126 1505
    """

    logiclike = LogicLike()
    logiclike.login(username, password)
    logiclike.get_chapter_with_solution(chapter_id, output_folder=output)


@logiclike_group.command(name="get-all")
@click.option('-u', '--username', type=click.STRING, help='Username')
@click.option('-p', '--password', type=click.STRING, help='Password')
@click.option('-o', '--output', default='.',
              type=click.Path(file_okay=False, exists=True),
              help='output folder')
@click.argument('chapter_ids', metavar='{chapter_ids}')
def logiclike_get_full_all_chapter(username, password, chapter_ids, output):
    """
    sample: ptoolbox lgl get-all -u {email} -p {pass} 1505,1153
    """

    logiclike = LogicLike()
    logiclike.login(username, password)
    # print(chapter_ids.split(","))
    logiclike.get_all_chapters_with_solution(chapter_ids.split(","), output_folder=output)


@codesignal_group.command(name="tournament-result")
@click.option('-c', '--credential', default='credentials.ini',
              type=click.Path(dir_okay=False, exists=True), help='Configuration file that contain airtable credential')
@click.option('-u', '--user_map', default='user_map.csv',
              type=click.Path(dir_okay=False, exists=True), help='codesignal\'s username - fullname mapping')
@click.argument("tournament", metavar='{tournament id or url}')
def codesignal_get_tournament_result(tournament, credential=None, user_map=None):
    cs = Codesignal()
    tour_info, tour_standing = cs.get_tournament_result(tournament)
    # tournament_id = tour_info['id']
    # tournament_task_ids = tour_info['fields']['taskIds']
    # print("Tournament info", json.dumps(tour_info))
    # print(f"Tournament id: '{tournament_id}'")
    # print(f"Tournament task ids: `{tournament_task_ids}`")
    # print(f"Tournament standing: {len(tour_standing)}", json.dumps(tour_standing))

    print(f"\n\nTournament: https://app.codesignal.com/tournaments/{tour_info['id']}")
    print(f"\nStarted at: {datetime.fromtimestamp(tour_info['fields']['startDate'] // 1000).isoformat()}")

    tour_json = cs.tournament_standing_format(tour_info, tour_standing)
    print(cs.tournament_json_to_ascii_table(tour_json))

    tour_standing = cs.re_judge(tour_standing)
    tour_json = cs.tournament_standing_format(tour_info, tour_standing)
    print(f"\n\nREJUDGE result:\n")
    print(cs.tournament_json_to_ascii_table(tour_json))

    if credential:
        pass
        api_key, base_id, table = Airtable.read_credential(credential)
        if not api_key or not base_id or not table:
            CLog.error(f'AIRTABLE api_key, base_id or table are missing in {credential} file')
        else:
            airtable = Airtable(api_key=api_key, base_id=base_id, table_name=table)
            users = None
            if user_map:
                users = cs.read_user_map(user_map)

            cs.tournament_standing_to_airtable(tour_json, airtable, users)
