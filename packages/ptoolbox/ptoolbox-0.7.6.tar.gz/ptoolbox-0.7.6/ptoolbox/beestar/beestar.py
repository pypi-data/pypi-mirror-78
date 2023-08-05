# coding=utf-8
import copy
import glob
import logging

__author__ = 'ThucNC'

import configparser
import os
import re
import time
from typing import List
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup
from ptoolbox.helpers.clog import CLog
from ptoolbox.models.question import Question, QuestionOption, QuestionType

_logger = logging.getLogger(__name__)


def strip_br(s):
    while s.strip().endswith("<br/>"):
        s = s.strip()[:-5]
    return s.strip()


class Beestar:
    def __init__(self, host="beestar.org"):
        self.base_url = "https://" + host
        self.username = None
        self.csrf_token = None
        self.s = requests.session()
        self._headers = {
            'host': host,
            'origin': self.base_url,
            'referer': self.base_url + '/user?cmd=getLogin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.122 Safari/537.36',
        }

    def login(self, username, password):
        """
        login, return student list
        [
            (id, email, name, url),
            (id, email, name, url),
        ]
        :param username:
        :param password:
        :return:
        """
        login_url = self.base_url + "/user?cmd=login"

        data = {
            "loginID": username,
            "password": password,
            "Login": ""
        }
        r = self.s.post(login_url, headers=self._headers, data=data, allow_redirects=False)
        print(r.status_code)

        if r.status_code == 302:
            host = urlsplit(r.headers['Location']).netloc
            self.base_url = "https://" + host
            self._headers = {
                'host': host,
                'origin': self.base_url,
                'referer': self.base_url + '/user?cmd=getLogin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/81.0.4044.122 Safari/537.36',
            }
            login_url = self.base_url + "/user?cmd=login"
            r = self.s.post(login_url, headers=self._headers, data=data)
            print(r.status_code)

        # print(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')
        students = soup.select("table.edgeblue tr")
        if students:
            titles = students[0].select("td")
            if len(titles) == 4 and titles[1].text == "Student":
                CLog.info(f"Found {len(students)-1} students!")
                res = []
                for student in students[1:]:
                    # print(student)
                    tds = student.select("td")
                    a_tag = tds[1].select("a")[0]
                    res.append((tds[2].text, tds[3].text, a_tag.text, self.base_url + a_tag['href']))
                return res

        CLog.error("Login failed!")
        return []

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('BEESTAR'):
            CLog.error(f'Section `BEESTAR` should exist in {credential_file} file')
            return None
        if not config.has_option('BEESTAR', 'cookie'):
            CLog.error(f'cookie are missing in {credential_file} file')
            return None

        return config.get('BEESTAR', 'cookie')

    def login_by_cookie(self, cookie):
        self._headers['cookie'] = cookie

    def get_review_detail(self, review_url, output_folder):
        CLog.info(f"Getting quiz {review_url}")
        headers = copy.deepcopy(self._headers)
        r = self.s.get(review_url, headers=headers)
        print(r.status_code)
        # print(r.headers)
        # print(r.text)

        test_url = self.base_url + "/exam?cmd=reviewresult"
        r = self.s.get(test_url, headers=headers)
        # print(r.status_code)
        # print(r.headers)

        soup = BeautifulSoup(r.text, 'html.parser')

        title = soup.select("center")[0].select("h2")[0]
        # if "Grade 5 GT Math Exercise Results: week 1, ex. 2" in title.text:
        #     print(soup.prettify())
        CLog.warn(f"Got quiz: {title.text}")
        file_name = "-".join(title.text.lower().replace(":", "").replace(",", "").replace(".", "").split())

        output_file = os.path.join(output_folder, file_name + "_raw.html")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(r.text)

        self.clean_html(soup, output_folder, file_name)

    def clean_html(self, soup, output_folder, file_name):
        body = soup.select("body")[0]
        centers = soup.select("center")
        title = centers[0].select("h2")[0]
        centers[0].replaceWith(title)
        centers[-1].decompose()

        scripts = soup.select("script")
        for script in scripts:
            script.extract()

        bookmarks = soup.select("span.bm")
        for bookmark in bookmarks:
            bookmark.extract()

        inputs = soup.select("input")
        for input_tag in inputs:
            input_tag.extract()

        # print(soup.prettify())

        body.attrs = {}
        imgs = soup.select("body image")
        # print("img:", imgs)
        for img in imgs:
            if "or_diam.gif" in img['src']:
                img['src'] = self.base_url + "/images/or_diam.gif"
            elif "white_diam.gif" in img['src']:
                # img.replaceWith(img.contents)
                # img.extract()
                s = ""
                for c in img.contents:
                    s += str(c)
                img.replaceWith(BeautifulSoup(s, 'html.parser'))


        # if "Grade 5 GT Math Exercise Results: week 1, ex. 2" in title.text:
        #     print("YYYY")
        # print(soup.prettify())

        with_ans = soup.prettify()

        imgs = soup.select("image")
        for img in imgs:
            if "diam.gif" in img['src']:
                img.extract()

        fonts = soup.select("font")
        for font in fonts:
            if font['size'] == "2":
                font.extract()

        without_ans = soup.prettify()

        output_file = os.path.join(output_folder, file_name + ".html")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(without_ans)
        out_file_with_ans = os.path.join(output_folder, file_name + "_ans.html")
        with open(out_file_with_ans, "w", encoding="utf-8") as f:
            f.write(with_ans)

        return without_ans, with_ans

    @staticmethod
    def read_quiz_from_file(html_file_with_ans) -> (str, List[Question]):
        CLog.info(f"Reading beestar quiz from file {html_file_with_ans}")
        questions = []
        multiple_question = False
        with open(html_file_with_ans, "r") as f:
            quiz_html = f.read()
            soup = BeautifulSoup(quiz_html, 'html.parser')
            title = soup.select("h2")[0].text.strip()
            CLog.info(f"Quiz title: {title}")

            questions_html = quiz_html.split("<hr/>")
            for question_html in questions_html[1:]:
                question_soup = BeautifulSoup(question_html, 'html.parser')
                if question_soup.select("b"):
                    # print("Question:", question_soup.prettify())
                    question_number_tags = []
                    for b_tag in question_soup.select("b"):
                        s = b_tag.text.strip()
                        if s.endswith('.') and s[:-1].isdigit() and 1 <= int(s[:-1]) <= 10:
                            # b_tag.decompose()
                            question_number_tags.append(b_tag)
                    if len(question_number_tags) <= 1:
                        questions.append(Beestar.parse_question(question_soup))
                    else:
                        CLog.warn("MULTIPLE QUESTION FOUND!")
                        multiple_question = True
                        a_question_soup = BeautifulSoup("", 'html.parser')
                        first = True
                        for child in question_soup.children:
                            # print("child", child)
                            if child in question_number_tags[1:]:
                                # find previous image
                                image = None
                                to_removed = None
                                br_count = 0
                                p = child.previous_sibling
                                for _ in range(5):
                                    if p:
                                        if p.name == "br":
                                            br_count += 1
                                        elif p.name and p.select("img"):
                                            to_removed = p
                                            image = p.select("img")[0]
                                        p = p.previous_sibling
                                if image and br_count < 3:
                                    tmp = copy.copy(image)
                                    if to_removed:
                                        to_removed.decompose()
                                    image = tmp
                                    # print("a_question_soup", a_question_soup.prettify())
                                    # s = a_question_soup.prettify()
                                    # i = s.find("""<br/>\n<br/>\n<br/>""")
                                    # if i > 0:
                                    #     s = s[:i]
                                    #     a_question_soup = BeautifulSoup(s, 'html.parser')
                                questions.append(Beestar.parse_question(a_question_soup,
                                                                        base_question=first,
                                                                        sub_question=not first))
                                first = False
                                # print("HOHOOH", a_question_soup.decode_contents())
                                # print("HOHOOH HOHO")
                                a_question_soup = BeautifulSoup("", 'html.parser')
                                br = a_question_soup.new_tag("br")
                                if image and br_count < 3:
                                    a_question_soup.append(image)
                                    a_question_soup.append(br)
                                    a_question_soup.append(br)

                            a_question_soup.append(copy.copy(child))
                        # s = a_question_soup.prettify()
                        # i = s.find("""<br/>\n<br/>\n<br/>""")
                        # if i > 0:
                        #     s = s[:i]
                        #     a_question_soup = BeautifulSoup(s, 'html.parser')
                        questions.append(Beestar.parse_question(a_question_soup, sub_question=True))
                        # print("HOHOOH", a_question_soup.decode_contents())
                        # print("HOHOOH HOHO")
        CLog.info(f"Done, {len(questions)} questions found!" + (" MULTIPLE QUESTION FOUND" if multiple_question else ""))
        return title, questions

    @staticmethod
    def parse_question(question_soup, base_question=False, sub_question=False) -> Question:
        """
        parse một nhóm câu hỏi ngăn cách bởi <hr/>
        :param question_soup:
        :return:
        """
        # print("Question: ", question_soup)
        for p_tag in question_soup.select("p"):
            if not p_tag.text.strip():
                p_tag.decompose()

        solution = None
        for solution_tag in question_soup.select("font"):
            if solution_tag['size'] == "2":
                solution = solution_tag.decode_contents().strip()
                # print("solution:", solution)
                # remove everything goes after solution
                tag = solution_tag.next_sibling
                while tag:
                    # print("next", tag)
                    tmp = tag
                    tag = tag.next_sibling
                    tmp.extract()
                solution_tag.extract()
                break

        options = []
        to_be_extracted = []
        for b_tag in question_soup.select("b"):
            if b_tag.text.strip() in ["A.", "B.", "C.", "D.", "E.", "F."]:
                is_correct = False
                if b_tag.previous_sibling and b_tag.previous_sibling.name == "image" or \
                        b_tag.previous_sibling and b_tag.previous_sibling.previous_sibling \
                        and b_tag.previous_sibling.previous_sibling.name == "image":
                    # and "or_diam.gif" in next_tag["src"]:
                    if b_tag.previous_sibling.name == "image":
                        b_tag.previous_sibling.decompose()
                    else:
                        b_tag.previous_sibling.previous_sibling.decompose()
                    is_correct = True

                option_soup = BeautifulSoup("", 'html.parser')
                for next_sib in b_tag.next_siblings:
                    if next_sib.name == 'b' and next_sib.text.strip() in ["A.", "B.", "C.", "D.", "E.", "F."]:
                        break
                    if next_sib.name != "image":
                        option_soup.append(copy.copy(next_sib))
                        to_be_extracted.append(next_sib)

                # next_tag = b_tag.next_sibling
                # next_tag.extract()
                #
                # option_soup = BeautifulSoup("", 'html.parser')
                # while next_tag and not (next_tag.name == 'b'
                #                         and next_tag.text.strip() in ["A.", "B.", "C.", "D.", "E.", "F."]):
                #     print("next sibling:", next_tag)
                #     option_soup.append(copy.copy(next_tag))
                #     tmp = next_tag
                #     next_tag = next_tag.next_sibling
                #     tmp.extract()
                b_tag.extract()

                # print("Option found", option_soup.decode_contents().strip(), is_correct)
                options.append(QuestionOption(content=strip_br(option_soup.decode_contents().strip()), is_correct=is_correct))
                # print('option', options[-1])

                for tag in to_be_extracted:
                    tag.extract()

        for b_tag in question_soup.select("b"):
            s = b_tag.text.strip()
            if s.endswith('.') and s[:-1].isdigit() and 1 <= int(s[:-1]) <= 10:
                b_tag.decompose()

        # print("Question:", question_soup.prettify())
        # print("Options:", options)
        # print("Solution:", solution)

        if options:
            if options[0].content.find("<") < 0 <= options[-1].content.find("<"):
                # plain text option, remove redundant image of next sub question in last option
                options[-1].content = options[-1].content[:options[-1].content.find("<")].strip()

            # remove redundant image of next question in last option
            option0_soup = BeautifulSoup(options[0].content, 'html.parser').select("img")
            optionn_soup = BeautifulSoup(options[-1].content, 'html.parser').select("img")
            if len(option0_soup) == 1 and len(optionn_soup) > 1:
                options[-1].content = optionn_soup[0].prettify()

        question = Question(statement_format="html",
                            statement_language="en",
                            statement=question_soup.decode_contents().strip(),
                            options=options,
                            type=QuestionType.MULTI_CHOICE,
                            solution=solution,
                            base_question=base_question,
                            sub_question=sub_question
                            )

        # print("statement:", question.statement)
        return question

    def get_student_quiz_list(self, student, include_passed_quizzes=False):
        student_url = student[3]
        headers = copy.deepcopy(self._headers)
        r = self.s.get(student_url, headers=headers)

        print(r.status_code)
        # print(r.headers)
        # print(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')
        quiz_tags = soup.select("a")
        quizzes = []
        for quiz_tag in quiz_tags:
            href = quiz_tag['href']
            if "startexerciseconfirm" in href:
                quizzes.append(self.base_url + href)

        passed_quizzes = []
        if include_passed_quizzes:
            print("Getting passed quizzes url...")
            r = self.s.get(self.base_url + "/exam?cmd=termhistoryexercises", headers=headers)
            print(r.status_code)
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            # quiz_tags = soup.select("table.edgeorange a")
            quiz_tags = soup.select("table a")
            more_urls = []
            for quiz_tag in quiz_tags:
                href = quiz_tag['href']
                if "startexerciseconfirm" in href:
                    passed_quizzes.append(self.base_url + href)
                elif "termhistoryexercises" in href:
                    more_urls.append(self.base_url + href)
            print(*passed_quizzes, sep='\n')
            print("more url", more_urls)
            for more_url in more_urls:
                time.sleep(2) # ko có cái này ko load đc dữ liệu cho các req sau
                r = self.s.get(more_url, headers=headers)
                print(r.status_code)
                soup = BeautifulSoup(r.text, 'html.parser')
                quiz_tags = soup.select("a")
                for quiz_tag in quiz_tags:
                    href = quiz_tag['href']
                    if "startexerciseconfirm" in href:
                        passed_quizzes.append(self.base_url + href)

            print(*passed_quizzes, sep='\n')
        # print("len", len(quizzes), len(passed_quizzes))
        # print(*quizzes, sep='\n')
        # print("len")
        # print(*passed_quizzes, sep='\n')
        return quizzes, list(set(passed_quizzes))

    def start_exercise(self, quiz_url):
        CLog.info(f"Starting quiz {quiz_url}")
        headers = copy.deepcopy(self._headers)
        r = self.s.get(quiz_url, headers=headers)
        # print(r.status_code)
        # print(r.headers)
        # print(r.text)

        test_url = self.base_url + "/exam?cmd=startexercise&status=NSTART"
        r = self.s.get(test_url, headers=headers)
        print(r.status_code)
        # print(r.headers)
        print("Start exercise:")
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        input_tags = soup.select("form input")

        cmd = exam_id = student_id = start_dt = em_type = trace_num = submitExam = ""
        for input_tag in input_tags:
            if input_tag["name"] == "cmd":
                cmd = input_tag["value"]
            if input_tag["name"] == "exam_id":
                exam_id = input_tag["value"]
            if input_tag["name"] == "student_id":
                student_id = input_tag["value"]
            if input_tag["name"] == "start_dt":
                start_dt = input_tag["value"]
            if input_tag["name"] == "em_type":
                em_type = input_tag["value"]
            if input_tag["name"] == "trace_num":
                trace_num = input_tag["value"]
            if input_tag["name"] == "submitExam":
                submitExam = input_tag["value"]

        submit_url = self.base_url + "/exam"

        data = {
            "cmd": cmd,
            "submitExam": submitExam,
            "exam_id": exam_id,
            "student_id": student_id,
            "start_dt": start_dt,
            "em_type": em_type,
            "trace_num": trace_num

        }
        print(data)
        r = self.s.post(submit_url, headers=headers, data=data)

        print(r.status_code)
        print(r.headers)
        # print(r.text)

    def get_all_quizzes(self, username, password, output_folder, include_passed_quizzes=False):
        students = self.login(username, password)
        if not students:
            return []

        for student in students:
            CLog.warn(f"Getting quizzes for student {student}, include past quizzes: {include_passed_quizzes}")
            quizzes, passed_quizzes = self.get_student_quiz_list(student, include_passed_quizzes)
            print("quiz count:", len(quizzes), "past quizzes:", len(passed_quizzes))
            # print(*passed_quizzes, sep='\n')
            # return
            for quiz_url in quizzes:
                if "status=NSTART" in quiz_url:
                    CLog.info(
                        f"Exercise not Finished yet. Trying to submit it first before getting result: {quiz_url}...")
                    self.start_exercise(quiz_url)
                    time.sleep(1)
                    self.get_review_detail(quiz_url.replace("status=NSTART", "status=FINISH"), output_folder)
                    # break
                else:
                    # pass
                    self.get_review_detail(quiz_url, output_folder)
                time.sleep(1)
            if include_passed_quizzes:
                # print("Passed quizzes", *passed_quizzes, sep="\n")
                CLog.warn(f"Getting passed quizzes for student {student}")
                for quiz_url in passed_quizzes:
                    if "status=NSTART" in quiz_url:
                        CLog.info(
                            f"Exercise not Finished yet. Trying to submit it first before getting result: {quiz_url}...")
                        self.start_exercise(quiz_url)
                        time.sleep(1)
                        self.get_review_detail(quiz_url.replace("status=NSTART", "status=MADEUP"), output_folder)
                        # break
                    else:
                        # pass
                        self.get_review_detail(quiz_url, output_folder)
                    time.sleep(1)
            # break

    @staticmethod
    def read_quizzes_files_from_folder(folder):
        """

        :param folder: wildcards supported: grade-2-gt-math
        :return:
        """
        files = glob.glob(folder)
        CLog.info(f"Found {len(files)} file(s)!")
        files = sorted(files, key=lambda f: int(re.sub('[^0-9]', '', f)))
        print(*files, sep="\n")
        return files


if __name__ == "__main__":
    beestar = Beestar()

    # students = beestar.login("studylandjsc@gmail.com", "qmq8yh")
    # students = beestar.login("gthuc.nguyen@gmail.com", "pxnv84")
    # beestar.get_review_detail("https://beestar.org/exam?cmd=startexerciseconfirm&session_num3=5510668262045598&status=MADEUP&descID=1171&em_type=WKEX&src=exam_history&check_sus=true",
    #                           "../../problems/bs")

    httmlfile = "../../problems/bs/beestar-grade-5-gt-math-exercise-results-week-1-ex-2-spring-2020_raw.html"
    with open(httmlfile, "r") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        beestar.clean_html(soup, "../../problems/", "beestar-grade-5-gt-math-exercise-results-week-1-ex-2-spring-2020")

    # output_folder = "/home/thuc/projects/ucode/content_crawler/data/beestar"
    # output_folder = "../../problems/bs"
    # students = beestar.get_all_quizzes(username="gthuc.nguyen@gmail.com", password="pxnv84",
    #                                    output_folder=output_folder, include_passed_quizzes=True)

    # title, quiz = beestar.read_quiz_from_file("/home/thuc/projects/ucode/content_crawler/data/beestar/"
    #                                           "beestar-grade-5-gt-math-exercise-results-week-15-ex-2-spring-2020_ans.html")
    #                                           # "beestar-grade-2-gt-math-exercise-results-week-10-ex-1-spring-2020_ans.html")
    # for question in quiz:
    #     print(question)

    # files = beestar.read_quizzes_files_from_folder(
    #     "/home/thuc/projects/ucode/content_crawler/data/beestar/*grade-2-gt-math*_ans.html"
    # )


