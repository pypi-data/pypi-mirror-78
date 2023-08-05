import copy
import html

import requests
from tomd import Tomd
from bs4 import BeautifulSoup

from ptoolbox.dsa.dsa_problem import DsaProblem

from ptoolbox.models.general_models import Problem, TestCase


def to_markdown(html_text):
    if not html_text:
        return ""
    # html_text = html_text.replace("$$$", "$")
    soup = BeautifulSoup(html_text, 'html.parser')

    # img tag must be inside <p> tag
    imgs = soup.select("img")
    if imgs:
        for img in imgs:
            img['src'] = "https://open.kattis.com" + img['src']
            if "alt" in img:
                img.string = img['alt']
            del img['style']
            del img['alt']
            new_tag = soup.new_tag('p')
            img.wrap(new_tag)

    html_ = html.unescape(soup.decode())
    res = Tomd(html_).markdown.strip()

    return res


class Kattis:
    def __init__(self):
        self.username = None
        self.s = requests.session()
        self._headers = {
            'origin': 'https://open.kattis.com/',
            'referer': 'https://open.kattis.com/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
        }

    def get_problem(self, problem_slug):
        if problem_slug.count('/') < 2:
            url = 'https://open.kattis.com/problems/{}'.format(problem_slug)
        else:
            problem_slug = problem_slug.strip("/")
            problem_slug = problem_slug[problem_slug.rfind("/") + 1:]
            url = 'https://open.kattis.com/problems/{}'.format(problem_slug)

        print("Getting problem from:", url)

        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        raw = r.text

        soup = BeautifulSoup(raw, 'html.parser')
        problem_wrapper = soup.select('div.problem-wrapper')[0]
        problem_info = soup.select('div.problem-sidebar div.sidebar-info p')

        problem = Problem()
        if len(problem_info) > 3:
            difficulty = float(problem_info[3].select("span")[0].text)
            # print(difficulty)
            problem.difficulty = Kattis.normalize_difficulty(difficulty)
        problem.src_url = url
        problem.src_id = problem.slug = problem_slug
        problem.name = problem_wrapper.select("div.headline-wrapper > h1")[0].text
        print(problem.name)

        problem_body = problem_wrapper.select("div.problembody")[0]

        h_tags = problem_body.select("h2")
        if not h_tags:
            h_tags = problem_body.select("h3")
        input_tag = output_tag = None
        for h2 in h_tags:
            if h2.text == "Input":
                input_tag = h2
            elif h2.text == "Output":
                output_tag = h2

        # print(str(input_tag))

        # print(problem_wrapper.prettify())

        next_tag = input_tag.next_sibling
        input_tag.extract()
        input_tags = BeautifulSoup("", 'html.parser')
        while next_tag != output_tag:
            if next_tag:
                input_tags.append(copy.copy(next_tag))
            # print(next_tag)
            tmp = next_tag
            next_tag = next_tag.next_sibling
            tmp.extract()

        # print(input_tags.prettify())

        # print(str(output_tag))

        next_tag = output_tag.next_sibling
        output_tag.extract()
        output_tags = BeautifulSoup("", 'html.parser')
        first_sample = problem_body.select("table.sample")[0]
        while next_tag != first_sample:
            if next_tag:
                output_tags.append(copy.copy(next_tag))
            # print(next_tag)
            tmp = next_tag
            next_tag = next_tag.next_sibling
            tmp.extract()

        # print(output_tags.prettify())

        problem.input_format = to_markdown(input_tags.decode())
        problem.output_format = to_markdown(output_tags.decode())

        # print(problem.input_format)
        # print(problem.output_format)

        problem.constraints = 'See inline constraints in the input description'

        sample_tags = problem_body.select("table.sample")
        i = 0
        for sample_tag in sample_tags:
            # print(str(sample_tag))
            sample_test = sample_tag.select("tr > td > pre")
            testcase = TestCase(sample_test[0].text.strip(), sample_test[1].text.strip(), name=str(i + 1))
            # print(testcase)
            problem.stock_testcases_sample.append(testcase)
            sample_tag.extract()
            i += 1

        # print(len(problem.stock_testcases_sample))

        # print(str(problem_body))

        problem.statement = to_markdown(problem_body.decode())
        print(problem.statement)

        return problem

    @staticmethod
    def normalize_difficulty(original_difficulty):
        """
        [1.1, 8.5] --> [2.5, 10]
        :param original_difficulty:
        :return:
        """

        return original_difficulty + 1.5

    @staticmethod
    def original_difficulty(normalized_difficulty):
        return round(normalized_difficulty - 1.5, 1)


if __name__ == "__main__":
    # prepare_testcases("../problems/prob1", True)
    kt = Kattis()
    # kt.login('thucngch', '15041985')
    # dsa_problem = kt.get_problem("tarifa")
    dsa_problem = kt.get_problem("hittingtargets")

    DsaProblem.save(dsa_problem, "../problems", overwrite=True)

