# coding=utf-8
import json
import logging
import os
from collections import Counter
import requests
from bs4 import BeautifulSoup

from ptoolbox.helpers.clog import CLog
from ptoolbox.models.question import Question, QuestionOption, QuestionType, QuestionContent

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


class IQSha:
    def __init__(self):
        self.username = None
        self.csrf_token = None
        self.s = requests.session()
        self._headers = {
            'origin': 'https://iqsha.ru',
            'referer': 'https://iqsha.ru',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
        }

    def login(self, email, password):
        url = "https://iqsha.ru/users/login"
        data = {
            "email": email,
            "password": password,
        }
        r = self.s.post(url, json=data, headers=self._headers)

        print(r.status_code)
        # print(r.headers)
        res = r.json()
        if res.get('email') == email:
            CLog.info(f"Login successfull with email: {email}")
        else:
            CLog.error(f"Login failed: {r.text}")

    def _get_url_and_parse_first_script(self, url):
        r = self.s.get(url, headers=self._headers)

        # print(r.status_code)
        # print(r.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        js = soup.select("script")[0].decode_contents().strip()

        data = js[js.find("{"):-1]
        return json.loads(data)

    def get_quiz_url(self, path, year):
        if year < 21:
            if year > 7:
                clazz = f"{year - 7}-klass"
            elif year > 4:
                clazz = f"{year}-let"
            else:
                clazz = f"{year}-goda"

            url = f"https://iqsha.ru/uprazhneniya/run/{path}/{clazz}"
        else:
            if year == 21:
                clazz = "preschool"
            elif year == 22:
                clazz = 'pre-k'
            elif year == 23:
                clazz = 'kindergarten'
            else:
                clazz = 'school'
            url = f"https://iqsha.com/quizzes/run/{path}/{clazz}"
        return url

    def get_chapter_list(self, save_to_file=None, load_from_file=None):
        if load_from_file:
            CLog.info(f"Loading chapter list from file '{load_from_file}'")
            with open(load_from_file, "r") as f:
                return json.load(f)

    def get_catalog(self, save_to_file=None, load_from_file=None):
        if load_from_file:
            CLog.info(f"Loading catalog from file '{os.path.abspath(load_from_file)}'")
            with open(load_from_file, "r") as f:
                return json.load(f)

        url = "https://iqsha.ru/uprazhneniya"
        # url = "https://iqsha.com/quizzes"
        catalog = self._get_url_and_parse_first_script(url)
        print(json.dumps(catalog, ensure_ascii=False))
        res = []
        for theme in catalog['catalog']:
            if not theme.get('topics'):
                CLog.warn(f"No topic in theme {theme['name']}")
                continue
            print(theme['name'], theme['years'], len(theme['topics']))
            theme.pop('items')
            for topic in theme['topics']:
                print("    ", topic['name'], topic['years'], len(topic['items']))
                for item in topic['items']:
                    print("    ", "    ", item['name'], item['years'], item['path'], item['count_question'])
                    for i, y in enumerate(item['years']):
                        url = self.get_quiz_url(item['path'], y)
                        # item['years'][i] = (y, url)
                        # problems = iqsha.get_problems(url)
                        # print(f"          >>> {len(problems['performed']['questions'])} >>>", json.dumps(problems))
                        print("    ", "    ", "    ", url)
            res.append(theme)

        if save_to_file:
            CLog.info(f"Saving catalog to file '{os.path.abspath(save_to_file)}'")
            with open(save_to_file, "w", encoding='utf8') as f:
                json.dump(res, f, indent=2, ensure_ascii=False)
        # else:
        #     print(json.dumps(res, ensure_ascii=False))
        return res

    def get_full_catalog_with_questions(self, catalog=None, save_to_file=None, load_from_file=None):
        if load_from_file:
            CLog.info(f"Loading full catalog with questions from file '{os.path.abspath(load_from_file)}'")
            with open(load_from_file, "r") as f:
                return json.load(f)

        for theme in catalog:
            # break
            print(theme['name'])
            for topic in theme['topics']:
                print("    ", topic['name'])
                for item in topic['items']:
                    print("    ", "    ", item['name'])
                    item['questions'] = dict()
                    for year in item['years']:
                        # if year > 7:
                        #     continue
                        url = self.get_quiz_url(item['path'], year)
                        print("    ", "    ", "    ", url)

                        problems = self.get_problems(url)
                        # print(json.dumps(problems))

                        print("    ", "    ", "    ", f"# of questions: {len(problems['performed']['questions'])}")
                        item['questions'][year] = problems['performed']['questions']

        if save_to_file:
            CLog.info(f"Saving full catalog with questions to file '{os.path.abspath(save_to_file)}'")
            with open(save_to_file, "w", encoding='utf8') as f:
                json.dump(catalog, f, indent=2, ensure_ascii=False)
        # else:
        #     print(json.dumps(res, ensure_ascii=False))
        return catalog

    def get_problems(self, topic_url):
        return self._get_url_and_parse_first_script(topic_url)

    def read_courses_from_full_catalog_file(self, full_catalog_file, year=2):
        """
        year: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        :param full_catalog_file:
        :param year:
        :return:
        """
        full_catalog = self.get_catalog(load_from_file=full_catalog_file)
        print("Theme count:", len(full_catalog))
        question_types = []
        ignore_questions = []
        chapters = []
        for theme in full_catalog: # theme = chapter
            # theme: {"id": 10163, "parent_id": 0, "name": "Логика и мышление", "path": "logika-i-myshlenie", "topics": [...], "years": [2, 3, 4, 5, 6, 7, 21, 22, 23, 24]}

            chapter = {
                "name": theme['name'],
                "path": theme['path']
            }
            # print("######################")
            # print("Theme:", theme['name'])

            sub_chaps = []
            for topic in theme['topics']:  # theme = subchap
                #topic: {"id": 10165, "parent_id": 10163, "name": "Исключаем лишнее", "path": "isklyuchaem-lishnee", "years": [2, 3, 4, 5, 6, 7, 21, 22, 23, 24], "items": []
                # print("topic:", json.dumps(topic, ensure_ascii=False))
                # print("    topic:", topic['name'])
                sub_chap = {
                    "name": topic['name'],
                    "path": topic['path']
                }
                lessons = []
                for item in topic['items']: # item = lesson
                    # item: {"id": 192, "topic_id": 10165, "name": "Лишняя картинка", "path": "lishnjaja-kartinka", "preview_url": "", "count_question": 48, "limit_to_diplom": 4, "performance_for_diploma": 90, "icon": {"preset": "style-1", "png": "/img-v2/icons/exercises/web/92-2c149db9319780c07b5b8bc0734e567ef1934c4b.png"}, "years": [5, 6, 7]}
                    lesson = {
                        "name": item['name'],
                        "path": item['path'],
                        "icon": ("https://iqsha.ru" + item['icon']['png']) if item['icon']['png'] else None,
                        "question_count": item["count_question"]
                    }
                    # print("         item:", item['name'])
                    # print("item:", json.dumps(item, ensure_ascii=False))
                    # return
                    lesson_questions = []
                    for y, questions in item['questions'].items():
                        y = int(y)
                        if y != year:
                            continue
                        lesson["url"] = self.get_quiz_url(item['path'], y)
                        # print("Question count:", y, len(questions))
                        for question in questions:
                            view_type = question['view_type']
                            answer_type = question['answer']['type']
                            question_types.append(view_type)

                            question['year'] = y
                            lesson_question = self.parse_question(question, lesson["url"])
                            if lesson_question:
                                lesson_questions.append(lesson_question)
                            else:
                                ignore_questions.append(view_type)
                            # if question["instruction"]:
                            #     print(json.dumps(question))
                            #     return

                            # if view_type == 51 :#and answer_type not in [1, 2, 3, 4]:
                            #     print(theme['path'], item['path'], view_type, answer_type)
                            #     print(self.get_quiz_url(item['path'], y))
                            #     print(json.dumps(question))
                            #     return [], 0, 0
                    if lesson_questions:
                        lesson['questions'] = lesson_questions
                        lessons.append(lesson)
                if lessons:
                    sub_chap['lessons'] = lessons
                    sub_chaps.append(sub_chap)
            if sub_chaps:
                chapter['sub_chapters'] = sub_chaps
                chapters.append(chapter)

        print("question_types", len(question_types), json.dumps(Counter(question_types)))
        print("ignore_questions", len(ignore_questions), json.dumps(Counter(ignore_questions)))
        return chapters, len(question_types), len(ignore_questions)

    def parse_question(self, q, quiz_url=""):
        """
        quest, instruction, explanation, option đều có các trường sau, riêng option có thêm
        {
    "text": "<p style=\"text-align: justify;\">Чай в чашке номер один самый сладкий. Где самый сладкий чай?</p>",
    "voice": {
      "id": "57691",
      "guid": "57691",
      "name": "Чай в чашке номер один самый сладкий. Где самый сладкий чай?",
      "mp3": "/upload/voice/5/7/6/i57691/57691.mp3",
      "ogg": "/upload/voice/5/7/6/i57691/57691.ogg",
      "autoplay": false
    }
        :param question:
        :return:
        """
        question = Question(
            src_id=q['id'],
            statement=q['quest']['text'],
            statement_format='html',
            statement_media=self.parse_question_content(q['quest']),
            statement_language="vi",
            hint=self.parse_question_content(q['instruction']),
            solutions=self.parse_question_content(q['explanation']),
            option_display=q['answer'],
            source={
                "quiz_url": quiz_url,
                "src_id": q['id']
            }
        )

        question.statement_media.text = question.statement_media.text_type = None
        # print(q['view_type'], q['answer']['type'])
        if q['view_type'] == 1:
            ans_type = q['answer']['type']
            # print(len(q['answers']))
            if ans_type in [1, 2, 4]:
                if ans_type == 1:
                    question.type=QuestionType.SINGLE_CHOICE
                elif ans_type == 2:
                    question.type = QuestionType.MULTI_CHOICE
                else:
                    question.type = QuestionType.DRAG_DROP
                question.options = []
                answers = []
                for i, op in enumerate(q['answers']):
                    option_content = self.parse_question_content(op)
                    option = QuestionOption(
                        id=op['id'],
                        # contents=self.parse_question_content(op),
                        is_correct=str(op['value'])=="1",

                        text=option_content.text,
                        text_type=option_content.text_type,
                        image=option_content.image,
                        image_type=option_content.image_type,
                        video=option_content.video,
                        video_type=option_content.video_type,
                        sound=option_content.sound,
                        sound_text=option_content.sound_text,
                    )

                    if ans_type == 4:
                        option.value = json.loads(op['value'])
                    if option.is_correct:
                        answers.append(str(i))
                    option.settings = op['settings'] or {}
                    option.settings['position'] = op['position']
                    option.settings['size'] = op['size']
                    question.options.append(option)
                question.answer = ",".join(answers)
            elif ans_type == 3:

                # print("len", len(q['answers']))
                if len(q['answers'])>1:
                    question.type = QuestionType.FILL_IN
                    # print(quiz_url)
                    statement = question.statement
                    soup = BeautifulSoup(statement, 'html.parser')
                    fields = soup.select("img.iq_field")
                    field_list = []
                    values = {}
                    for op in q['answers']:
                        values[op['id']] = op['value']

                    for field in fields:
                        # replace = "{{%s}}" % f"x{field['data-id']}"
                        replace = "{{%s}}" % values[field['data-id']]
                        field_list.append(field['data-id'])
                        field.insert_after(soup.new_string(replace))
                        field.extract()

                    # ans = []
                    # for data_id in field_list:
                    #     for op in q['answers']:
                    #         if op['id'] == data_id:
                    #             ans.append(f"x{op['id']}::{op['value']}")
                    #             break
                    # question.answer = "||".join(ans)
                    question.answer = None
                    # print("before", question.statement)
                    question.statement = soup.decode_contents()
                    # print("after", question.statement)
                    # print("ans:", question.answer)
                    # print(json.dumps(q, ensure_ascii=False))
                else:
                    question.type = QuestionType.SHORT_ANSWER
                    question.answer = str(q['answers'][0]["value"]).strip()
                    # print("shortanswer", json.dumps(q))
                    # print("answer:", question.answer)
                    # if not question.answer:
                    #     print("shortanswer", json.dumps(q))
                    # print(q['answers'][0])
            else:
                CLog.warn(f"Not supported view_type {q['view_type']} and answer type {ans_type}")
                return None
        elif q['view_type'] == 2:
            question.type = QuestionType.THEORY
        elif q['view_type'] == 3:
            question.type = QuestionType.PUZZLE
            op = q['state']['puzzle']
            if op['preview']:
                op['preview'] = "https://iqsha.ru" + op['preview']
                for part in op['parts']:
                    part['src'] = "https://iqsha.ru" + part['src']
            question.options = op
        elif q['view_type'] == 141:
            question.type = QuestionType.CLASSIFY
            op = q['state']['param']
            for group in op['list']:
                for i, url in enumerate(group):
                    group[i] = "https://iqsha.ru" + url
            question.options = op
        elif q['view_type'] == 91:
            question.type = QuestionType.MATCHING
            op = q['state']['list']
            for pair in op:
                pair['src1'] = "https://iqsha.ru" + pair['src1']
                pair['src2'] = "https://iqsha.ru" + pair['src2']
            question.options = op
        elif q['view_type'] == 131:
            question.type = QuestionType.SORTING
            op = q['state']['param']
            for i, url in enumerate(op['imageList']):
                op['imageList'][i] = "https://iqsha.ru" + url
            question.options = op
        elif q['view_type'] == 71:
            question.type = QuestionType.FIND_DIFF
            op = q['state']
            op['src1'] = "https://iqsha.ru" + op['src1']
            op['src2'] = "https://iqsha.ru" + op['src2']
            question.options = op
        elif q['view_type'] == 121:
            question.type = QuestionType.MEMORY
            op = q['state']['param']
            op['img_face_down'] = "https://iqsha.ru" + op['imageList'][0]
            op['list'] = []
            for img in op['imageList'][1:]:
                op['list'].append({
                    'src1': "https://iqsha.ru" + img,
                    'src2': "https://iqsha.ru" + img,
                })
            # op.pop('imageList')
            question.options = op
        else:
            CLog.warn(f"Not supported view_type {q['view_type']}")
            return None

        return question

    def parse_question_content(self, q) -> QuestionContent:
        if not q:
            return None
        qcontent = QuestionContent()
        if q.get("text"):
            qcontent.text = q.get("text")
            qcontent.text_type = "html"

        if q.get("voice"):
            qcontent.sound_text = q["voice"].get("name")
            if q["voice"].get("mp3"):
                qcontent.sound = "https://iqsha.ru" + q["voice"].get("mp3")
            else:
                qcontent.sound = "https://iqsha.ru" + q["voice"].get("ogg")
        return qcontent


if __name__ == "__main__":
    iqsha = IQSha()
    years = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    count = {}
    total = 0
    for y in years:
        course, n, ignores = iqsha.read_courses_from_full_catalog_file(
            full_catalog_file="/home/thuc/projects/ucode/content_crawler/data/iqsha/catalog_with_questions.json",
            year=y
        )
        count[y] = (n, ignores)
        total += n
        # json.dump(course, open(f"../../problems/iqsha/course{y}.json", "w"), ensure_ascii=False)'
        for chap in course:
            print(chap["name"])
            for subchap in chap['sub_chapters']:
                for lesson in subchap['lessons']:
                    for question in lesson['questions']:
                        if question.type == QuestionType.FILL_IN:
                            print(question.to_json())
                            # print("after:", question.answer)
                            break

    print(count)
    print("Total:", total)

    # iqsha.login("gthuc.nguyen@gmail.com", "ngoaho85")
    # # catalog = iqsha.get_catalog(save_to_file='../../problems/iqsha/catalog.json')
    # catalog = iqsha.get_catalog(load_from_file='../../problems/iqsha/catalog.json')
    # print(len(catalog))
    # print(json.dumps(catalog, ensure_ascii=False))
    #
    # full_catalog = iqsha.get_full_catalog_with_questions(
    #     catalog,
    #     save_to_file='../../problems/iqsha/catalog_with_questions.json')

    # full_catalog = iqsha.get_full_catalog_with_questions(
    #     load_from_file='../../problems/iqsha/catalog_with_questions.json')

    # question_types = []
    # answer_types = []
    # print(f"Question view types: {Counter(question_types)}")
    # print(f"Answer types: {Counter(answer_types)}")

    # problems = iqsha.get_problems("https://iqsha.ru/uprazhneniya/run/bolshojj-ili-malenkijj/3-goda")
    # print(json.dumps(problems))
    # print(len(problems['performed']['questions']))
    # questions = []
    # for q in problems['performed']['questions']:
    #     questions.append(q['id'])
    # print(sorted(questions))

    # print("Final:", json.dumps(full_catalog, ensure_ascii=False))