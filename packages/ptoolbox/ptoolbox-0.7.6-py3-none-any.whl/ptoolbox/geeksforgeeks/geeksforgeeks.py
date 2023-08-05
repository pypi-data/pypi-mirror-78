import copy
import html

import requests
from tomd import Tomd
from bs4 import BeautifulSoup

from ptoolbox.models.general_models import Problem, TestCase


def to_markdown(html_text):
    if not html_text:
        return ""
    # html_text = html_text.replace("$$$", "$")
    soup = BeautifulSoup(html_text, 'html.parser')

    # img tag must be inside <p> tag
    imgs = soup.select("center > img")
    if imgs:
        for img in imgs:
            img['src'] = "https://open.kattis.com" + img['src']
            img.string = img['alt']
            del img['style']
            del img['alt']
            img.parent.name = "p"

    html_ = html.unescape(soup.decode())
    print(html_)
    res = Tomd(html_).markdown.strip()

    return res


class GeeksForGeeks:
    def __init__(self):
        self.username = None
        self.s = requests.session()
        self._headers = {
            'origin': 'https://practice.geeksforgeeks.org/',
            'referer': 'https://practice.geeksforgeeks.org/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
        }

    def get_problem(self, problem_slug):
        url = 'https://practice.geeksforgeeks.org/problems/{}'.format(problem_slug)
        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        raw = r.text

        soup = BeautifulSoup(raw, 'html.parser')
        problem_title_tag = soup.select('div#border div.row strong')[0]

        problem = Problem()
        problem.src_url = url
        problem.src_id = problem.slug = problem_slug
        problem.name = problem_title_tag.text.strip()
        print(problem.name)

        return

        problem_body = soup.select("div.problemQuestion")[0]
        h2s = problem_body.select("h2")
        input_tag = output_tag = None
        for h2 in h2s:
            if h2.text == "Input":
                input_tag = h2
            elif h2.text == "Output":
                output_tag = h2

        print(str(input_tag))

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

        print(input_tags.prettify())

        print(str(output_tag))

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

        print(output_tags.prettify())

        problem.input_format = to_markdown(input_tags.decode())
        problem.output_format = to_markdown(output_tags.decode())

        print(problem.input_format)
        print(problem.output_format)

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

        print(len(problem.stock_testcases_sample))

        print(str(problem_body))

        problem.statement = to_markdown(problem_body.decode())
        print(problem.statement)

        return problem


if __name__ == "__main__":
    # prepare_testcases("../problems/prob1", True)
    gg = GeeksForGeeks()
    # dsa_problem = gg.get_problem("counts-zeros-xor-pairs/0")
    # dsa_problem = gg.get_problem("n-queen-problem/0")

    problem_slugs = [
        'n-queen-problem/0',
        'counts-zeros-xor-pairs/0',
        'rotate-array-by-n-elements/0',
        'kth-smallest-element/0',
        'arraylist-operation/1',
        'max-distance-between-same-elements/1',
        'game-of-death-in-a-circle/0',
        'diagonal-sum-in-binary-tree/1',
        'delete-middle-element-of-a-stack/1',
        'next-happy-number/0',
        'count-subsequences-of-type-ai-bj-ck4425/1',
        'count-subsequences-of-type-ai-bj-ck/0',
        'distinct-occurrences/1',
        'count-of-strings-that-can-be-formed-using-a-b-and-c-under-given-constraints/0',
    ]

    for slug in problem_slugs:
        dsa_problem = gg.get_problem(slug)
        break

    # DsaProblem.save(dsa_problem, "../problems", overwrite=True)

