# coding=utf-8
import json
import logging

__author__ = 'ThucNC'

import configparser
from typing import List, Union

import requests

from ptoolbox.beestar.beestar import Beestar
from ptoolbox.iqsha.iqsha import IQSha
from ptoolbox.dsa.dsa_problem import DsaProblem
from ptoolbox.hackerrank.hackerrank import HackerRank, prepare_testcases
from ptoolbox.helpers.clog import CLog
from ptoolbox.helpers.misc import make_slug
from ptoolbox.models.general_models import Problem, TestCase
from ptoolbox.models.question import Question, QuestionOption, QuestionType

_logger = logging.getLogger(__name__)


class UCode:
    def __init__(self, base_url, token):
        self.s = requests.session()
        self.api_base_url = base_url
        self.token = token
        self._headers = {
            'access-token': self.token
        }

    def get_api_url(self, path):
        return self.api_base_url + path

    def create_problem(self, lesson_id, problem: Union[Question, Problem, str],
                       score=10, xp=100, lang='vi', statement_format="markdown", question_type='code',
                       is_server_judge=0):
        """

        :param lesson_id:
        :param problem:
        :param score:
        :param xp:
        :param lang:
        :param statement_format:
        :param question_type: multiple_choice, short_answer, code, turtle, sport
        :return:
        """
        if isinstance(problem, str):
            problem: Problem = DsaProblem.load(problem, load_testcase=True)

        if isinstance(problem, Problem):
            data = {
                "name": problem.name,
                "type": question_type,
                "statement": problem.statement,
                "statement_format": statement_format,
                "input_desc": problem.input_format,
                "output_desc": problem.output_format,
                "constraints": problem.constraints,
                "compiler": "python",
                "statement_language": lang,
                "score": score,
                "solution": problem.solution,
                "status": "published",
                "visibility": "public",
                "ucoin": xp,
                'is_server_judge': is_server_judge
            }
        elif isinstance(problem, Question):
            question: Question = problem
            data = {
                "name": question.src_name,
                "type": question.type.value or type,
                "statement": question.statement,
                "statement_format": statement_format,
                "statement_language": lang,
                "score": score,
                "status": "published",
                "visibility": "public",
                "ucoin": xp,
                "constraints": "base_question" if question.base_question else
                                               ("sub_question" if question.sub_question else "")
            }

            new_option_format = False
            if not isinstance(question.options, list):
                new_option_format = True
            else:
                for i, option in enumerate(question.options):
                    if not isinstance(option, QuestionOption):
                        # CLog.error("Option not valid:")
                        # print(question.to_json())
                        new_option_format = True
                        break
                    if not option.content:
                        new_option_format = True
                        break
                    data[f"option{i + 1}"] = option.content
                    if option.is_correct:
                        data['answer'] = f"{i + 1}"

            question_json = json.loads(question.to_json())
            if question.solution:
                data['solution'] = question.solution
            elif question.solutions:
                data['solutions'] = json.dumps(question_json['solutions'])

            if question.hint:
                data['hint'] = json.dumps(question_json["hint"])

            if question.statement_media:
                data['statement_media'] = json.dumps(question_json["statement_media"])

            if question.option_display:
                data['option_display'] = json.dumps(question_json["option_display"])

            if question.source:
                data['source'] = json.dumps(question_json["source"])

            if new_option_format:
                data['options'] = json.dumps(question_json["options"])

            if question.answer is not None:
                data['answers'] = question.answer
            if question.type == QuestionType.SHORT_ANSWER:
                print("data:", data)
        else:
            raise Exception(f"Unsupported problem type {type(problem)}")

        if lesson_id:
            url = self.get_api_url(f"/lesson-item/{lesson_id}/question")
        else:
            url = self.get_api_url(f"/problems")
            data['slug'] = make_slug(problem.name)

        response = self.s.post(url, json=data, headers=self._headers)

        print(response.status_code)
        # print(response.text)
        res = response.json()
        # print(res)
        if res['success']:
            question_id = res['data']['id']
            print("question_id:", question_id)
        else:
            raise Exception("Cannot create question:" + json.dumps(res))

        if isinstance(problem, Problem):
            # upload testcase
            for i, testcase in enumerate(problem.testcases):
                self.upload_testcase(question_id, testcase, is_sample=True)

        if isinstance(problem, Problem):
            if problem.translations:
                for tran_lang, tran_problem in problem.translations.items():
                    CLog.info(f"Creating translation {tran_lang} for question #{question_id}...")
                    data = {
                        "name": tran_problem.name,
                        "type": "code",
                        "root_question_id": question_id,
                        "statement": tran_problem.statement,
                        "statement_language": tran_lang,
                        "input_desc": tran_problem.input_format,
                        "output_desc": tran_problem.output_format,
                        "constraints": tran_problem.constraints,

                    }
                    response = self.s.post(url, json=data, headers=self._headers)
                    res = response.json()
                    if res['success']:
                        tran_question_id = res['data']['id']
                        print("translated question_id:", tran_question_id)
                    else:
                        raise Exception("Cannot create question:" + json.dumps(res))

        return question_id

    def create_problems(self, lesson_id, problems: List[Problem], score=10, xp=100, lang="vi"):
        question_ids = []
        for problem in problems:
            q_id = self.create_problem(self, lesson_id=lesson_id,
                                       problem=problem,
                                       score=score, xp=xp, lang=lang)
            question_ids.append(q_id)

        return question_ids

    def upload_testcase(self, problem_id, testcase: TestCase, is_sample=True, score=10):
        url = self.get_api_url(f"/question/{problem_id}/testcase")
        data = {
            "name": testcase.name,
            "explanation": testcase.explanation,
            "input": testcase.input,
            "output": testcase.output,
            "score": score,
            "is_sample": bool(is_sample)
        }

        response = self.s.post(url, json=data, headers=self._headers)
        print(response.status_code)
        res = response.json()
        print(res)
        if res['success']:
            testcase_id = res['data']['id']
            print("testcase_id:", testcase_id)
        else:
            CLog.error("Cannot create testcase:" + json.dumps(res))

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('UCODE'):
            CLog.error(f'Section `UCODE` should exist in {credential_file} file')
            return None, None
        if not config.has_option('UCODE', 'api_url') or not config.has_option('UCODE', 'token'):
            CLog.error(f'api_url and/or token are missing in {credential_file} file')
            return None, None

        api_url = config.get('UCODE', 'api_url')
        token = config.get('UCODE', 'token')

        return api_url, token

    def create_chapter(self, course_id, chapter_name, slug=None, parent_id=None, status="draft", _type="chapter"):
        if not slug:
            slug = make_slug(chapter_name)

        data = {
            "parent_id": parent_id if parent_id else 0,
            "item_type": _type,
            "name": chapter_name,
            "is_preview": False,
            # "content_type": "video",
            "is_free": True,
            "slug": slug,
            "status": status
        }

        url = self.get_api_url(f"/curriculum/{course_id}/course-items")

        response = self.s.post(url, json=data, headers=self._headers)

        print(response.status_code)
        res = response.json()
        print(res)
        if res['success']:
            return res['data']['id']
        else:
            raise Exception("Cannot create chapter:" + json.dumps(res))

    def create_lesson_item(self, course_id, chapter_id, lesson_name, slug=None,
                           desciption="", content="",
                           type="video", video_url="",
                           status="draft"):
        if not slug:
            slug = make_slug(lesson_name)

        data = {
            "parent_id": chapter_id,
            "item_type": "lesson_item",
            "name": lesson_name,
            "is_preview": False,
            "content_type": type,
            "is_free": True,
            "slug": slug,
            "status": status
        }

        url = self.get_api_url(f"/curriculum/{course_id}/course-items")

        response = self.s.post(url, json=data, headers=self._headers)
        print(response.status_code)
        res = response.json()
        # print(res)
        if not res['success']:
            raise Exception("Cannot create course item for lesson:" + json.dumps(res))

        course_item_id = res['data']['id']
        print("course_item_id:", course_item_id)
        lesson_item_id = res['data']['lesson_item_id']
        print("lesson_item_id:", lesson_item_id)
        # if type == "video":
        if video_url or content or desciption:
            url = self.get_api_url(f"/lesson-item/{lesson_item_id}")
            data = {
                "description": desciption,
                "video_url": video_url,
                "content": content,
                "content_format": "markdown",
                "slug": slug,
                "is_free": True,
                "is_preview": False,
                "visibility": "public"
            }

            response = self.s.put(url, json=data, headers=self._headers)
            print(response.status_code)
            res = response.json()
            print(res)
            if not res['success']:
                raise Exception("Cannot lesson item:" + json.dumps(res))
        return lesson_item_id

    def create_lesson_item_from_beestar_file(self, course_id, chapter_id, beestar_file):
        beestar = Beestar()
        title, quiz = beestar.read_quiz_from_file(beestar_file)
        title = title \
            .replace("Beestar", "") \
            .replace("Exercise Results: ", "") \
            .replace(",", " -") \
            .replace("ex. ", "p") \
            .strip()

        if not title or not quiz:
            CLog.error(f"Cannot read quiz from file {beestar_file}")
            return

        lesson_id = self.create_lesson_item(course_id=course_id, chapter_id=chapter_id, lesson_name=title, type="quiz")
        CLog.info(f"Lesson #{lesson_id} created!")

        for question in quiz:
            self.create_problem(lesson_id=lesson_id, problem=question, lang='en', statement_format='html')
        return lesson_id


def create_chapters_mc1():
    ucode = UCode("https://dev-api.ucode.vn/api", "72821b59462c5fdb552a049c1caed85c")

    course_id = 7
    for w in range(1, 13):
        chapter_name = "Thử thách %02d" % w
        chapter_id = ucode.create_chapter(course_id=course_id, chapter_name=chapter_name)


def iqsha(year, ucode_course_id):
    iqsha = IQSha()
    course, n, ignores = iqsha.read_courses_from_full_catalog_file(
        full_catalog_file="/home/thuc/projects/ucode/content_crawler/data/iqsha/catalog_with_questions.json",
        year=year
    )

    # ucode = UCode("https://dev-api.ucode.vn/api", "538ac87edf833079fe3818993e519641")
    ucode = UCode("https://api.ucode.vn/api", "28514c33b635c2206b3f121fbe016a6a")
    course_id = ucode_course_id

    print(f"Total question: {n}, ignored: {ignores}")

    for i, chap in enumerate(course):
        chap_name = chap["name"]
        print(chap_name)
        chapter_id = ucode.create_chapter(course_id, chap_name, slug=f"chap{i+1}", status="published")
        for j, subchap in enumerate(chap['sub_chapters']):
            subchap_id = ucode.create_chapter(course_id, subchap['name'], slug=f"p{i+1}.{j+1}", parent_id=chapter_id,
                                              status="published", _type="lesson")
            for lesson in subchap['lessons']:
                lesson_id = ucode.create_lesson_item(course_id=course_id, chapter_id=subchap_id,
                                                     lesson_name=lesson['name'], type="quiz", status="published")
                for question in lesson['questions']:
                    ucode.create_problem(lesson_id, problem=question, xp=25,  lang='vi', statement_format='html')
                    # if question.type == QuestionType.FILL_IN:
                    #     print(question.to_json())
                        # return
                    # print(question.options)
                    # if question.type == QuestionType.FILL_IN:
                        # print(question.to_json())
                        # print("after:", question.answer)
                        # pass


if __name__ == "__main__":
    ucode_courses = {
        2: 42,
        3: 43,
        4: 44,
        5: 45,
        6: 46,
        7: 47,
        8: 48,
        9: 49,
        10: 50,
        11: 51
    }
    # ucode_courses = {
    #     2: 46
    # }
    for y, course_id in ucode_courses.items():
        iqsha(y, course_id)

    # create_chapters_mc1()

    # ucode = UCode("https://dev-api.ucode.vn/api", "72821b59462c5fdb552a049c1caed85c")
    # # problem_folder = "../../problems/domino_for_young"
    # problem_folder = "/home/thuc/projects/ucode/courses/course-py101/lesson2/c1_input/p13_chao_ban"
    # ucode_lesson_id = 172
    #
    # problem: Problem = DsaProblem.load(problem_folder, load_testcase=True)
    # #
    # # print(problem)
    # #
    # print(len(problem.testcases))
    # for testcase in problem.testcases:
    #     print(testcase)

    # ucode.create_problem(lesson_id=172, problem=problem_folder)

    # beestar = Beestar()
    #
    # files = beestar.read_quizzes_files_from_folder(
    #     "/home/thuc/projects/ucode/content_crawler/data/beestar/*grade-4-math*_ans.html"
    # )
    # course_id = 17
    # # chappter_id = 413  # GT Math 2
    # # chappter_id = 630  # GT Math 5
    # chappter_id = 735
    # # chappter_id = 619  # problems
    #
    # ucode = UCode("https://dev-api.ucode.vn/api", "df12e0548fbba3e6f48f9df2b78c3df2")
    # # for file in files:
    # #     ucode.create_lesson_item_from_beestar_file(course_id=course_id, chapter_id=chappter_id, beestar_file=file)
    # file = "../../problems/bs/_bs_ans.html"
    # ucode.create_lesson_item_from_beestar_file(course_id=course_id, chapter_id=chappter_id, beestar_file=file)

    # problem_folder = "/home/thuc/projects/ucode/problemtools/problems/cs/Arcade_TheCore/p001_Intro_Gates__addTwoDigits"
    # problem = DsaProblem.load(problem_folder, load_testcase=True)
    #
    # hr = HackerRank()
    # hr.login('thucngch', '15041985')
    # # prepare_testcases("/home/thuc/projects/ucode/problemtools/problems/cs/Arcade_TheCore/p001_Intro_Gates__addTwoDigits")
    # hr.upload_testcases(163975, "/home/thuc/projects/ucode/problemtools/problems/cs/Arcade_TheCore/p001_Intro_Gates__addTwoDigits/testcases_hackerrank.zip")
    # # hr_prob = hr.create_problem(problem)
    # # print(json.dumps(hr_prob))
    #
    # "https://www.hackerrank.com/rest/administration/contests/46715/challenge?slug=add-two-digits&track_id=0&chapter_id=0&weight=100"
    #
    #
    # ucode = UCode("https://dev-api.ucode.vn/api", "df12e0548fbba3e6f48f9df2b78c3df2")
    # # print(problem)
    # # print(problem.name)
    # # print(len(problem.testcases))
    # #
    # # ucode.create_problem(lesson_id=None, problem=problem, question_type='code', lang="en")





