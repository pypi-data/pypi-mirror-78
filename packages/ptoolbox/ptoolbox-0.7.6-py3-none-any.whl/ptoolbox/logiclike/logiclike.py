# coding=utf-8
import csv
import json
import logging

__author__ = 'ThucNC'

import os

from collections import Counter

import requests
from ptoolbox.helpers.clog import CLog

_logger = logging.getLogger(__name__)


def parse_simplified_questions_from_chapter_deatail(chapter_detail):
    questions = []
    for quiz in chapter_detail['quizzes']:
        if quiz['type'] == "theory":
            question = {
                'chapter_id': chapter_detail['id'],
                'quiz_id': quiz['id'],
                'quiz_type': quiz['type'],
                'question_id': "",
                'question_type': "",
                'title': quiz['detail']['title'],
                'clapanAdviceText': quiz['detail']['text'],
                'solution': ""
            }
            for j in range(12):
                question[f'option{j}'] = ""
            questions.append(question)
        else:
            for i, q in enumerate(quiz['detail']['questions']):
                question = {
                    'chapter_id': chapter_detail['id'],
                    'quiz_id': quiz['id'],
                    'quiz_type': quiz['type'],
                    'question_id': q['id'],
                    'question_type': q['type'],
                    'title': q['title'],
                    'clapanAdviceText': q['clapanAdviceText'] or "",
                    'solution': quiz['detail']['rightAnswers'][i]['publicSolution']
                }

                for j in range(12):
                    option_text = ""
                    if j < len(q['variants']):
                        # print("variants", len(q['variants']), q['variants'])
                        if q['variants'][j]['imageSrc']:
                            option_text = "https://logiclike.com/" + q['variants'][j]['imageSrc']
                        elif q['variants'][j].get('title'):
                            option_text = q['variants'][j]['title']

                    question[f'option{j}'] = option_text

                questions.append(question)
    return questions


class LogicLike:
    def __init__(self):
        self.username = None
        self.csrf_token = None
        self.s = requests.session()
        self._headers = {
            'origin': 'https://logiclike.com',
            'referer': 'https://logiclike.com/auth/login',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
        }

    def login(self, username, password):
        url = 'https://logiclike.com/auth/authenticate.json?no_redirect=1'

        data = {
            "login": username,
            "password": password,
            "desiredRedirectUrl": "",
        }
        r = self.s.post(url, json=data, headers=self._headers)

        print(r.status_code)
        # print(r.headers)
        print(r.text)
        raw = r.json()
        print(raw)

        if raw['authenticated']:
            # print('Login succeeded, csrf token: {}'.format(raw['csrf_token']))
            CLog.important('Login succeeded')
            self.username = username
            # self.csrf_token = raw['csrf_token']
        else:
            raise ValueError("Login failed with user: {}".format(username))

        # res = r.json()origin
        # print(res)

        return True

    def get_chapter_list(self, save_to_file=None, load_from_file=None):
        if load_from_file:
            CLog.info(f"Loading chapter list from file '{load_from_file}'")
            with open(load_from_file, "r") as f:
                return json.load(f)

        url = "https://logiclike.com/user/course/logic.json?no_redirect=1"
        r = self.s.get(url, headers=self._headers)

        print(r.status_code)
        # print(r.headers)
        # print(r.text)
        res = r.json()
        if save_to_file:
            CLog.info(f"Saving chapter list to file '{save_to_file}'")
            with open(save_to_file, "w", encoding='utf8') as f:
                json.dump(res, f, indent=2, ensure_ascii=False)
        else:
            print(json.dumps(res))
        return res

    def get_chapter(self, chapter_id):
        """

        :param chapter:
        :return:
        """
        url = f"https://logiclike.com/chapter/ajax/show.json?id={chapter_id}&no_redirect=1"
        r = self.s.get(url, headers=self._headers)

        print(r.status_code)
        # print(r.headers)
        # print(r.text)
        raw = r.json()
        # print(json.dumps(raw))
        return raw

    def get_quiz(self, chapter_id, quiz, step=1):
        quiz_id = quiz['id']
        CLog.info(f"Getting quiz #{quiz_id} of type '{quiz['type']}' from chapter #{chapter_id}...")

        if quiz['type'] == 'theory':
            url = f"https://logiclike.com/user/course-theory/{quiz_id}.json?chapterId={chapter_id}&no_redirect=1"
            r = self.s.get(url, headers=self._headers)
            print(r.status_code)
            # print(r.headers)
            # print(r.text)
            res = r.json()
            print("Theory")
            # print(json.dumps(res))
            return res
        elif quiz['type'] == 'quiz':
            url = f"https://logiclike.com/quiz2/state.json?id={quiz_id}&step={step}&no_redirect=1"
            data = {
                "chapterId": str(chapter_id)
            }
            r = self.s.post(url, headers=self._headers, json=data)

            print(r.status_code)
            # print(r.headers)
            # print(r.text)
            res = r.json()
            # print(json.dumps(res))
            if res['status'] == "error":
                CLog.warn(f"ERROR getting quiz #{quiz_id} from chapter #{chapter_id} with step {step}: {res['error']}")
                return None
            # CLog.info(f"Question count: {len(res['quiz']['questions'])}")
            for question in res['quiz']['questions']:
                # print(f"Question type {question['type']}: {question['title']}")
                if question['type'] not in [1, 2, 5, 6]:
                    print("Another type, chapter id:", chapter_id)
            if step==1:
                return res

            return res
        else:
            print("Another type, quiz, chapter id:", chapter_id)

    def get_full_chapter_data(self, chapter_list=None, save_to_file=None, load_from_file=None,
                              save_tags_to_file=None, load_tags_from_file=None):
        """

        :param chapter_list:
        :param save_to_file:
        :param load_from_file:
        :param save_tags_to_file:
        :param load_tags_from_file:
        :return: (chapters, tags)
        """
        if load_from_file or load_tags_from_file:
            chapters = tags = None
            if load_from_file:
                CLog.info(f"Loading full chapter data from file '{load_from_file}'")
                with open(load_from_file, "r") as f:
                    chapters = json.load(f)
                    print(f"Chapters: {len(chapters)}")
            if load_tags_from_file:
                CLog.info(f"Loading full tag data from file '{load_from_file}'")
                with open(load_tags_from_file, "r") as f:
                    tags = json.load(f)
                    print(f"Tags: {len(tags)}")
            return chapters, tags

        chapters = chapter_list['course']['chapters']
        tags = chapter_list['course']['tags']

        print(f"Tags: {len(tags)}")
        # print(*[json.dumps(tag) for tag in tags], sep="\n")
        # print(*tags, sep="\n")

        print(f"Chapters: {len(chapters)}")
        # print(*[json.dumps(chapter) for chapter in chapters], sep="\n")
        # print(*chapters, sep="\n")

        complexity = {}
        for chapter in chapters:
            d = chapter['complexity']
            if d in complexity:
                complexity[d].append(chapter['name'])
            else:
                complexity[d] = [chapter['name']]

        for k, v in complexity.items():
            print(f"complexity {k}: {len(v)} chapters! ")

        for chapter in chapters:
            chapter_detail = self.get_chapter(chapter['id'])
            chapter['title'] = chapter_detail['chapter']['title']
            chapter['subTitle'] = chapter_detail['chapter']['subTitle']
            chapter['fullTitle'] = chapter_detail['chapter']['fullTitle']
            chapter['quizzes'] = chapter_detail['chapter']['items']

            tag = [tag for tag in tags if tag['id'] == chapter_detail['chapter']['tag']['id']][0]
            tag['service'] = chapter_detail['chapter']['tag']['service']
            # print("tag", json.dumps(tag))
            print("chapter_id", chapter['id'])

            for i, quiz in enumerate(chapter['quizzes']):
                quiz_detail = self.get_quiz(chapter['id'], quiz)
                if quiz['type'] == "quiz":
                    quiz_detail['quiz']['commonInfo']['tag'].pop('service')
                    # print("quiz", json.dumps(quiz_detail))
                    chapter['quizzes'][i]['detail'] = quiz_detail['quiz']
                elif quiz['type'] == "theory":
                    chapter['quizzes'][i]['detail'] = quiz_detail['theory']
                else:
                    raise Exception(f"Unknown quiz type '{quiz['type']}'")

            # print("chapter", json.dumps(chapter))

        # print("chapters", json.dumps(chapters[:1]))
        with open(save_to_file, "w", encoding='utf8') as f:
            json.dump(chapters, f, indent=2, ensure_ascii=False)

        with open(save_tags_to_file, "w", encoding='utf8') as f:
            json.dump(tags, f, indent=2, ensure_ascii=False)

        return chapters, tags

    def submit_question(self, question_id):
        """
        {"passingId":181121756,"result":[76201,76204,76203],"question":33904,"graphicResults":[]} -> type 1, 2
        {"passingId":181200120,"result":"9","question":26945,"graphicResults":[]} --> type 5

        :param question_id:
        :return:
        """
        url = "https://logiclike.com/quiz2/save-answer.json?no_redirect=1"

    def get_all_chapters_with_solution(self, chapter_ids, output_folder=None):
        print(chapter_ids)
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)

        chapters = []
        questions_all = []
        errors = []
        for chapterid in chapter_ids:
            chapter_detail = self.get_chapter_with_solution(chapterid)
            if not chapter_detail:
                errors.append(chapterid)
                continue
            chapters.append(chapter_detail)
            if output_folder:
                write_list_of_dict_to_file(chapter_detail, os.path.join(output_folder, f"{chapterid}.json"))
                questions_all.extend(parse_simplified_questions_from_chapter_deatail(chapter_detail))

        if output_folder:
            CLog.info(f"Writing chapter data to folder '{output_folder}'")
            # print(json.dumps(questions, ensure_ascii=False))
            write_list_of_dict_to_file(questions_all, os.path.join(output_folder, f"questions_all.csv"))

            with open(os.path.join(output_folder, "error.log"), "w", encoding='utf8') as f:
                f.write("ERROR:" + json.dumps(errors))

        CLog.error(f"CANNOT get chapters: {json.dumps(errors)}")
        return chapters

    def get_chapter_with_solution(self, chapter_id, output_folder=None):
        chapter_detail = self.get_chapter(chapter_id)

        chapter_detail = chapter_detail['chapter']


        chapter_detail['quizzes'] = chapter_detail['items']
        chapter_detail.pop('items')

        print(json.dumps(chapter_detail, ensure_ascii=False))

        print(len(chapter_detail['quizzes']))

        for i, quiz in enumerate(chapter_detail['quizzes']):
            print("quiz", i, quiz)
            res = self.get_quiz(chapter_id, quiz, step=2)
            if not res:
                CLog.error(f"ERROR getting quiz solution from chapter #{chapter_id}, maybe quiz NOT SOLVED?")
                CLog.info(f"Chapter url: https://logiclike.com/cabinet#/chapter/{chapter_id}")
                return None
            if quiz['type'] == "quiz":
                res['quiz']['commonInfo']['tag'].pop('service')
                # print("quiz", json.dumps(quiz_detail))
                chapter_detail['quizzes'][i]['detail'] = res['quiz']
            elif quiz['type'] == "theory":
                chapter_detail['quizzes'][i]['detail'] = res['theory']
            else:
                raise Exception(f"Unknown quiz type '{quiz['type']}'")
            # chapter_detail['quizzes'].append(res)

        if output_folder:
            folder = os.path.join(output_folder, str(chapter_id))
            os.makedirs(folder, exist_ok=True)

            CLog.info(f"Writing chapter data to folder '{folder}'")

            write_list_of_dict_to_file(chapter_detail, os.path.join(folder, f"{chapter_id}.json"))

            questions = parse_simplified_questions_from_chapter_deatail(chapter_detail)
            # print(json.dumps(questions, ensure_ascii=False))
            write_list_of_dict_to_file(questions, os.path.join(folder, f"{chapter_id}.csv"))

        return chapter_detail


def write_list_of_dict_to_file(data, output_file):
    if not data:
        return
    with open(output_file, "w", encoding='utf8') as f:
        if output_file.endswith(".json"):
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            for data in data:
                print("data", data)
                writer.writerow(data)


def make_simple_chap_list(input_file, output_file):
    logiclike = LogicLike()
    chapter_list, _ = logiclike.get_full_chapter_data(load_from_file=input_file)
    # print(json.dumps(chapter_list[0], ensure_ascii=False))

    chapter_list_lite = []
    for i, chap in enumerate(chapter_list):
        quizzes = []
        for quiz in chap['quizzes']:
            quiz_lite = {
            }
            if quiz['type'] == 'quiz':
                quiz_lite['question_type'] = quiz['detail']['questions'][0]['type']
                # quiz_lite['url'] = f"https://logiclike.com/cabinet#/chapter/{chap['id']}/quiz/{quiz['id']}/process"
            else:
                quiz_lite['url'] = f"https://logiclike.com/user/course-theory/{quiz['id']}.json"
                quiz_lite["type"] = quiz['type']
            quiz_lite["id"] = quiz['id']
            quizzes.append(quiz_lite)
        chapter_list_lite.append({
            "no.": i+1,
            "id": chap['id'],
            "name": chap['name'],
            "title": chap['title'],
            "subTitle": chap['subTitle'],
            "complexity": chap['complexity'],
            "tagId": chap['tagId'],
            "url": f"https://logiclike.com/cabinet#/chapter/{chap['id']}",
            "preview": "https://logiclike.com/" + chap['preview'],
            "quiz_count": len(chap['quizzes']),
            "quizzes": json.dumps(quizzes, ensure_ascii=False, indent=2)
        })

    CLog.info(f"Writing chapter list lite to file '{output_file}'")
    write_list_of_dict_to_file(chapter_list_lite, output_file)


def make_simple_tag_list(input_file, output_file):
    logiclike = LogicLike()
    _, tag_list = logiclike.get_full_chapter_data(load_tags_from_file=input_file)

    tag_list_lite = []
    for i, tag in enumerate(tag_list):
        tag_list_lite.append({
            "no.": i + 1,
            "id": tag['id'],
            "title": tag['title'],
            "icon": tag['icon'],
            "url": tag['url']
        })

    CLog.info(f"Writing tag list lite to file '{output_file}'")
    write_list_of_dict_to_file(tag_list_lite, output_file)


def stats(username, password, folder):
    logiclike = LogicLike()
    logiclike.login(username, password)
    chapter_list_file = os.path.join(folder, "chapter_list_raw.json")
    # chapters_list = logiclike.get_chapter_list(save_to_file=chapter_list_file)
    chapters_list1 = logiclike.get_chapter_list(load_from_file=chapter_list_file)

    # chapters, tags = logiclike.get_full_chapter_data(chapter_list=chapters_list1,
    #                                                  save_to_file="../../data/logiclike/chapters_full_wo_answer.json",
    #                                                  save_tags_to_file="../../data/logiclike/tags_full.json")

    chapters, tags = logiclike.get_full_chapter_data(load_from_file=os.path.join(folder, "chapters_full_wo_answer.json"),
                                                     load_tags_from_file=os.path.join(folder, "tags_full.json"))
    print("chapters", json.dumps(chapters[0], ensure_ascii=False))
    print("tags", json.dumps(tags, ensure_ascii=False))

    quiz_types = set()
    question_types = set()
    graphic_count = []
    variant_count = []
    quiz_count = []
    theories = []
    terms = []
    for chapter in chapters:
        quiz_count.append(len(chapter['quizzes']))
        for quiz in chapter['quizzes']:
            quiz_types.add(quiz['type'])
            if quiz['type'] == 'quiz':
                quiz_types.add(quiz['detail']['commonInfo']['type'])
                # quiz_types.add(quiz['detail']['commonInfo']['questionCount'])
                for question in quiz['detail']['questions']:
                    # question_types.add(question['type'])
                    variant_count.append(len(question['variants']))
                    if question['graphic']:
                        graphic_count.append(len(question['graphic']['items']))
                    else:
                        graphic_count.append(0)

                    if question['theory']:
                        theories.append(question['theory'])
                    if question['terms']:
                        terms.append(question['terms'])

    print(quiz_types)
    print(question_types)
    print("graphic items count", Counter(graphic_count))
    print("variant count", Counter(variant_count))
    print("quiz count", Counter(quiz_count))

    print(json.dumps(sorted(theories, key=lambda k: k['id']), ensure_ascii=False))
    print(len(theories), len(list(set([k['id'] for k in theories]))))
    print(json.dumps(sorted(terms, key=lambda k: k['hash']), ensure_ascii=False))
    print(len(terms), len(list(set([k['hash'] for k in terms]))))


if __name__ == "__main__":
    # make_simple_chap_list("../../data/logiclike/chapters_full_wo_answer.json", "../../data/logiclike/chapter_list_lite.csv")
    # make_simple_tag_list("../../data/logiclike/tags_full.json", "../../data/logiclike/tags_lite.csv")

    username, password = "thucngch@gmail.com", "183126"
    logiclike = LogicLike()
    logiclike.login(username, password)
    chapters = "1883,1801,1842,1844,2145,1865,1846,2014,1237,1197,2501,554,357,572,2392,2406,447,89,2391,1573,2153,28,2102,2332,281,821,1501,1234,822,1189,1782,346,508,1585,416,2387,260,1186,553,1723,830,2356,1571,819,2357,2340,194,2388,1159,283,347,2358,138,581,359,406,2359,1574,262,355,2333,1748,322,349,444,369,1556,1240,263,323,360,1202,411,1557,1720,2381,1562,2380,1737,2371,415,1719,2334,2354,392,1035,813,1621,2382,139,1741,2534,584,368,2368,264,1742,51,372"
    # chapters = "1201"
    # chapter = logiclike.get_chapter_with_solution(chapter_id, output_folder="../../problems/logiclike")
    chapter = logiclike.get_all_chapters_with_solution(chapters.split(","), output_folder="../../problems/logiclike")
    print(json.dumps(chapter, ensure_ascii=False))

    # stats(username, password, "/home/thuc/projects/ucode/content_crawler/data/logiclike")

