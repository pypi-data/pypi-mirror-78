import copy
import os
import codecs
from jinja2 import Template
from ptoolbox.helpers.misc import make_problem_code

from ptoolbox.dsa.dsa_problem_file import check_problem, find_section, read_testcases_from_file
from ptoolbox.helpers.clog import CLog
from ptoolbox.models.general_models import Problem, TestCase


def join_lines(lines):
    return ''.join([l+'\n' for l in lines]).strip()


class DsaProblem:
    @staticmethod
    def _parse_statement_file(statement_file, problem: Problem):
        with open(statement_file) as fi:
            statement = fi.read()
            lines = statement.splitlines()

            source_link = None
            s = lines[0]
            if not s.strip():
                s = lines[1]
            if s.startswith('[//]:'):
                o = s.find('(')
                if o:
                    source_link = s[o + 1:s.find(')')].strip()
                else:
                    source_link = s[5:].strip()
            problem.src_url = source_link

            statement_i, statement_c = find_section('#\s+.*', lines)
            if statement_i:
                title = lines[statement_i[0]][1:].strip()
                problem.name = title

                s = lines[statement_i[0] + 1].strip()
                if not s.strip():
                    s = lines[statement_i[0] + 2]
                if s.startswith('[//]:'):
                    problem.preview = s
                    o = s.find('(')
                    if o:
                        code = s[o + 1:s.find(')')].strip()
                    else:
                        code = s[5:].strip()
                    problem.code = code
                    problem.slug = problem.code.replace('_', '-')

            if statement_i:
                problem.statement = join_lines(statement_c[statement_i[0]])

            input_i, input_c = find_section('(#+\s*Input|Input\s*$)', lines)
            if input_i:
                problem.input_format = join_lines(input_c[input_i[0]])

            output_i, output_c = find_section('(#+\s*Output.*|Output\s*$|#+\s*Ouput.*|Ouput\s*$)', lines)
            if output_i:
                problem.output_format = join_lines(output_c[output_i[0]])

            constraints_i, constraints_c = find_section('(#+\s*Constraint.*|Constraints\s*$|#+\s*Giới hạn.*)', lines)
            if constraints_i:
                problem.constraints = join_lines(constraints_c[constraints_i[0]])

            tags_i, tags_c = find_section('#+\s*Tag.*', lines)
            if tags_i:
                tags = []
                for t in tags_c[tags_i[0]]:
                    t = t.strip()
                    if t:
                        if t.startswith('-'):
                            tags.append(t[1:].strip())
                        else:
                            tags.append(t)
                problem.tags = problem.topics = tags

            difficulty_i, difficulty_c = find_section('#+\s*Difficulty.*', lines)
            if difficulty_i:
                try:
                    problem.difficulty = float(difficulty_c[difficulty_i[0]][0])
                except ValueError:
                    CLog.warn(f"Difficulty is not parsable: {difficulty_c[difficulty_i[0]][0]}")

            sample_input_i, sample_input_c = find_section('#+\s*Sample input(.*)', lines)
            sample_output_i, sample_output_c = find_section('#+\s*Sample (ou|Ou|out|Out)put(.*)', lines)
            explanation_i, explanation_c = find_section('#+\s*Explanation(.*)', lines)
            if sample_input_i:
                for i in range(len(sample_input_i)):
                    testcase = TestCase()
                    testcase.input = join_lines(sample_input_c[sample_input_i[i]]).strip('`').strip()
                    testcase.output = join_lines(sample_output_c[sample_output_i[i]]).strip('`').strip()
                    if len(explanation_i) > i:
                        testcase.explanation = join_lines(explanation_c[explanation_i[i]]).strip('`').strip()

                    problem.testcases.append(testcase)


    @staticmethod
    def load(problem_folder, load_testcase=False, translations=[]):
        """

        :param problem_folder:
        :param load_testcase:
        :param translations: ['vi']
        :return:
        """
        problem_code = check_problem(problem_folder)
        statement_file = os.path.join(problem_folder, f"{problem_code}.md")

        problem = Problem()
        problem.slug = make_problem_code(problem_code)
        problem.code = problem_code
        problem.preview = f'[//]: # ({problem_code})'

        DsaProblem._parse_statement_file(statement_file, problem)
        if translations:
            for lang in translations:
                lang_statement_file = os.path.join(problem_folder, f"{problem_code}.{lang}.md")
                if not os.path.exists(lang_statement_file):
                    CLog.warn(f"Translation file not existed: {lang_statement_file}")
                else:
                    tran_problem = copy.copy(problem)
                    DsaProblem._parse_statement_file(lang_statement_file, tran_problem)
                    problem.translations[lang] = tran_problem

        solution_file = os.path.join(problem_folder, f"{problem_code}.py")
        if os.path.isfile(solution_file):
            with open(solution_file) as f:
                problem.solution = f.read()

        if load_testcase:
            file_names = ["testcases_manual_stock.txt", "testcases_manual.txt", "testcases_stock.txt", "testcases.txt"]
            for file_name in file_names:
                testcase_file = os.path.abspath(os.path.join(problem_folder, file_name))

                if not os.path.exists(testcase_file):
                    CLog.warn(f'`{testcase_file}` file not existed, skipping...')
                else:
                    tests = read_testcases_from_file(testcase_file)
                    print(f"reading testcases in file {testcase_file}: {len(tests)}")
                    for t in tests:
                        input, output = t['input'], t['output']
                        print(f"Input: {input}, output: {output}")
                        if input not in [test.input for test in problem.testcases]:
                            problem.testcases.append(TestCase(input=input, output=output))

        if not problem.testcases_sample and problem.testcases:
            problem.testcases_sample = problem.testcases[:1]

        return problem

    @staticmethod
    def save(problem : Problem, base_folder=".", problem_code=None, overwrite=False):
        """
        :param problem:
        :param problem_code: name of problem folder
        :param base_folder: the parent folder that will contain the problem folder
        :return:
        """
        if not problem_code:
            problem_code = problem.name

        problem_code = make_problem_code(problem_code)

        problem.code = problem_code

        problem_folder = os.path.join(base_folder, problem_code)

        if os.path.exists(problem_folder):
            if not overwrite:
                CLog.error('Problem folder existed! Delete the folder or use `overwrite` instead.')
                return
            else:
                CLog.warn('Problem folder existed! Content will be overwritten.')

        if not os.path.exists(problem_folder):
            os.makedirs(problem_folder)

        # if not os.path.exists(problem_folder + "/testcases"):
        #     os.makedirs(problem_folder + "/testcases")

        if not problem.name:
            problem.name = (' '.join(problem_code.split('_'))).title()

        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')

        if problem.testcases:
            with open(os.path.join(template_path, 'testcases.txt.j2')) as file_:
                template = Template(file_.read())
                content = template.render(testcases=problem.testcases)
                f = open(problem_folder + "/testcases.txt", 'w')
                f.write(content)
                f.close()

        if problem.testcases_sample:
            with open(os.path.join(template_path, 'testcases.txt.j2')) as file_:
                template = Template(file_.read())
                content = template.render(testcases=problem.testcases_sample)
                f = open(problem_folder + "/testcases_manual.txt", 'w')
                f.write(content)
                f.close()

        if problem.stock_testcases:
            with open(os.path.join(template_path, 'testcases.txt.j2')) as file_:
                template = Template(file_.read())
                content = template.render(testcases=problem.stock_testcases)
                f = open(problem_folder + "/testcases_stock.txt", 'w')
                f.write(content)
                f.close()

        if problem.stock_testcases_sample:
            with open(os.path.join(template_path, 'testcases.txt.j2')) as file_:
                template = Template(file_.read())
                content = template.render(testcases=problem.stock_testcases_sample)
                f = open(problem_folder + "/testcases_manual_stock.txt", 'w')
                f.write(content)
                f.close()

        if not problem.testcases_sample:
            problem.testcases_sample = problem.stock_testcases_sample

        with open(os.path.join(template_path, 'statement.md.j2')) as file_:
            template = Template(file_.read())
            statement = template.render(problem=problem)
            f = codecs.open(problem_folder + ("/%s.md" % problem_code), "w", "utf-8")
            f.write(statement)
            f.close()
            f = codecs.open(problem_folder + ("/%s.vi.md" % problem_code), "w", "utf-8")
            f.write(statement)
            f.close()

        with open(os.path.join(template_path, 'editorial.md.j2')) as file_:
            template = Template(file_.read())
            statement = template.render(problem=problem)
            f = codecs.open(problem_folder + ("/%s_editorial.md" % problem_code), "w", "utf-8")
            f.write(statement)
            f.close()

        with open(os.path.join(template_path, 'solution.py.j2')) as file_:
            template = Template(file_.read())
            content = template.render(problem_code=problem_code,
                                      solution=problem.solution if problem.solution else "pass")
            f = open(problem_folder + ("/%s.py" % problem_code), 'w')
            f.write(content)
            f.close()

        with open(os.path.join(template_path, 'generator.py.j2')) as file_:
            template = Template(file_.read())
            content = template.render(problem_code=problem_code)
            f = open(problem_folder + ("/%s_generator.py" % problem_code), 'w')
            f.write(content)
            f.close()

        if problem.solutions:
            for solution in problem.solutions:
                f = open(problem_folder + ("/solution.%s" % solution["lang"]), 'w')
                f.write(solution["code"])
                f.close()

        problem_folder = os.path.abspath(problem_folder)

        CLog.important(f'Problem created at `{problem_folder}`')


if __name__ == "__main__":
    # load_problem('/home/thuc/teko/online-judge/dsa-problems/number_theory/num001_sumab')
    # load_problem('/home/thuc/teko/online-judge/dsa-problems/unsorted/minhhhh/m010_odd_to_even')
    # problem = load_problem('/home/thuc/teko/online-judge/ptoolbox/problems/array001_counting_sort3')
    dsa_problem = DsaProblem.load('/home/thuc/teko/online-judge/dsa-problems/number_theory/num001_sumab')
    print(dsa_problem.prints())

