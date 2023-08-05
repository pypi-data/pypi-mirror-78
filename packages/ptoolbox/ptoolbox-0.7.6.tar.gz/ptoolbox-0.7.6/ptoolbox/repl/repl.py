import copy
import json
import traceback
from datetime import datetime

from dateutil import tz, parser

from draftjs_exporter.html import HTML
from draftjs_exporter_markdown import BLOCK_MAP, ENGINE, ENTITY_DECORATORS, STYLE_MAP

import requests

from ptoolbox.dsa.dsa_problem import DsaProblem
from ptoolbox.models.general_models import MatchingType, Classroom, ProgrammingLanguage, ProblemStatus, TestCase, \
    JudgeMode, Problem


class ReplIt:
    def __init__(self, cookies):
        self.s = requests.session()
        self._headers = {
            'origin': 'https://repl.it',
            'referer': 'https://repl.it/login',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': cookies
        }
        self.cookies = cookies

    def get_classroom(self, classroom_id, get_assignments=True, get_students=False, get_submissions=False,
                      get_all_problems=True):
        url = 'https://repl.it/data/classrooms/{}'.format(classroom_id)
        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)
        raw = r.json()

        classroom = Classroom()
        classroom.src_id = raw['id']
        classroom.name = raw['name']
        if raw['language_key'] == 'python3':
            classroom.language = ProgrammingLanguage.python3

        problems = []
        if get_assignments:
            url = 'https://repl.it/data/classrooms/{}/assignments'.format(classroom_id)
            r = self.s.get(url, headers=headers)
            assignments = r.json()
            for a in assignments:
                for p in ['classroom_id', 'time_deleted', 'time_updated', 'time_due', 'time_created', 'github_id']:
                    a.pop(p, None)
                # time_published = null: draft
                # time_published > now: scheduled
                # time_published <= now: published
                if not a['time_published']:
                    a['status'] = ProblemStatus.draft
                else:
                    now = datetime.now()
                    # from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    published_date = parser.parse(a['time_published'])
                    # published_date = published_date.replace(tzinfo=from_zone)
                    local = published_date.astimezone(to_zone).replace(tzinfo=None)
                    if local < now:
                        a['status'] = ProblemStatus.published
                    else:
                        a['status'] = ProblemStatus.scheduled

            classroom.assignments = sorted(assignments, key=lambda x: x['name'])
            if get_all_problems:
                # classroom
                problems = self.get_problems([asm['id'] for asm in assignments])

        if get_students:
            url = 'https://repl.it/data/classrooms/{}/students'.format(classroom_id)
            # r = self.s.get(url, headers=headers)
            # students = r.json()
            # TODO
        if get_submissions:
            url = 'https://repl.it/data/classrooms/{}/submissions'.format(classroom_id)
            # r = self.s.get(url, headers=headers)
            # students = r.json()
            # TODO

        return classroom, problems

    def get_problems(self, problem_ids):
        """
        :param problem_ids: list of problem ids
        :return:
        """
        problems = []
        for id in problem_ids:
            problems.append(self.get_problem(id))
        return problems

    def get_problem(self, problem_id):
        url = 'https://repl.it/data/assignments/{}'.format(problem_id)
        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        print(r.text)

        raw = r.json()
        problem = self.parse_problem(raw)
        return problem

    def get_testcases(self, problem_id):
        url = 'https://repl.it/data/assignments/{}/tests/'.format(problem_id)
        r = self.s.get(url, headers=self._headers)
        raw = r.json()
        print(raw)

        testcases = []
        for t in raw:
            testcase = self.parse_testcase(t)
            testcases.append(testcase)

        return testcases

    def get_solution(self, problem_id):
        url = 'https://repl.it/data/teacher/model_solutions/{}'.format(problem_id)
        r = self.s.get(url, headers=self._headers)
        raw = r.json()
        if 'editor_text' in raw:
            sol = raw['editor_text']
        else:
            sol = ''
        return sol

    def parse_problem(self, raw):
        exporter = HTML({
            'block_map': BLOCK_MAP,
            'style_map': STYLE_MAP,
            'entity_decorators': ENTITY_DECORATORS,
            'engine': ENGINE,
        })

        if not raw['instructions']:
            markdown = ''
        else:
            try:
                markdown = exporter.render(json.loads(raw['instructions']))
            except Exception:
                markdown = ""
                traceback.print_exc()

        problem = Problem()
        problem.statement = markdown

        if raw['feedback_mode'] == "input_output":
            problem.judge_mode = JudgeMode.oj
        elif raw['feedback_mode'] == "manual":
            problem.judge_mode = JudgeMode.manual
        else:
            problem.judge_mode = JudgeMode.unit_test

        problem.src_id = raw['id']
        problem.name = raw['name']
        problem.template = raw['editor_template']

        # print(markdown)

        problem.testcases = self.get_testcases(problem.src_id)
        # print(problem.testcases)

        if problem.testcases:
            problem.testcases_sample = problem.testcases[:1]

        problem.solution = self.get_solution(problem.src_id)
        return problem

    def parse_testcase(self, t):
        if t['matching_type'] == 'flexible':
            mt = MatchingType.flexible
        elif t['matching_type'] == 'strict':
            mt = MatchingType.strict
        else:
            mt = MatchingType.regexp
        testcase = TestCase(t['input'], t['output'], matchingtype=mt)
        testcase.src_id = t['id']
        return testcase


if __name__ == "__main__":
    cookies = \
        "_ga=GA1.2.1677725907.1574165625; ajs_group_id=null; " \
        "ajs_anonymous_id=%22ffa18d4a-381b-4ef8-91c8-8b8512a84015%22; " \
        "ajs_user_id=816683; " \
        "ajs_group_id=null; " \
        "ajs_anonymous_id=%22ffa18d4a-381b-4ef8-91c8-8b8512a84015%22; " \
        "_gid=GA1.2.1064340347.1586530886; " \
        "__cfduid=d71e0129e3276acbcf8a4c30508fa44591586598686; " \
        "connect.sid=s%3ABIXcPR3N1fqg6-Q95N431rGktezZS9tL.o6GU8PWzP4eLBvC%2Bgo5rczm4dVSwJwFhK%2FNaChC1Qns; " \
        "_gat=1; ajs_user_id=816683"
    repl = ReplIt(cookies)
    classroom, problems = repl.get_classroom(classroom_id=199129, get_assignments=True, get_all_problems=True)
    for problem in problems:
        DsaProblem.save(problem, "../../problems/lesson01")
    # print(classroom)
    # for assignment in classroom.assignments:
    #     print(assignment)

    # problem = repl.get_problem(5064610)
    # DsaProblem.save(problem, "../../problems/p1")


    # problem = repl.get_problem(2079412)
    # problem = repl.get_problem(2079413)
    # problem = repl.get_problem(2079416)
    # problem = repl.get_problem(2079417)

    # i = 1
    # for t in problem.testcases:
    #     print('#{}: '.format(i), t)
    #     i += 1

    # classroom = repl.get_classroom("85432")
    # print(classroom)
    # pprint.pprint(classroom.assignments)

    # test_create_problem()