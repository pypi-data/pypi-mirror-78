# coding=utf-8
import logging
import os
from distutils.dir_util import copy_tree

from ptoolbox.codeforces.codeforces import Codeforces
from ptoolbox.dsa.dsa_problem import DsaProblem

__author__ = 'ThucNC'

from ptoolbox.helpers.misc import make_problem_code

from ptoolbox.kattis.kattis import Kattis

_logger = logging.getLogger(__name__)


def read_all_problems(base_folder, nested_folder=0, load_testcase=False, translations=[]):
    res = []
    problem_folders = [f.path for f in os.scandir(base_folder) if f.is_dir()]
    for problem_folder in sorted(problem_folders):
        if nested_folder:
            for i in range(nested_folder):
                subfolders = [f.path for f in os.scandir(problem_folder) if f.is_dir()]
                for folder in sorted(subfolders):
                    print(problem_folder)
                    problem = DsaProblem.load(os.path.join(problem_folder, folder),
                                              load_testcase=load_testcase,
                                              translations=translations)
                    res.append((os.path.join(problem_folder, folder), problem))
        else:
            print(problem_folder)
            problem = DsaProblem.load(problem_folder, load_testcase=load_testcase, translations=translations)
            res.append((problem_folder, problem))
    return res


def get_all_codeforce_problem(base_folder):
    problem_folders = [f.path for f in os.scandir(base_folder) if f.is_dir()]
    cf = Codeforces()
    for problem_folder in sorted(problem_folders):
        problem = DsaProblem.load(problem_folder)
        if problem.src_url:
            output_folder = os.path.join(os.path.dirname(problem_folder), os.path.basename(problem_folder).lower())
            print("Getting", problem.src_url, "from", problem_folder, "to", output_folder)
            dsa_problem = cf.get_problem_from_url(problem.src_url)
            DsaProblem.save(dsa_problem, output_folder, None, overwrite=False)


def get_all_kattis_problem(base_folder):
    problem_folders = [f.path for f in os.scandir(base_folder) if f.is_dir()]
    kt = Kattis()
    for problem_folder in sorted(problem_folders):
        problem = DsaProblem.load(problem_folder)
        if problem.src_url:
            dsa_problem = kt.get_problem(problem.src_url)
            difficulty = int(Kattis.original_difficulty(dsa_problem.difficulty) * 10)
            output_folder = os.path.join(os.path.dirname(base_folder), "new",
                                         f"difficulty_{difficulty}")
            print("Getting", problem.src_url, "from", problem_folder, "to", output_folder)
            problem_code = make_problem_code(dsa_problem.name)
            DsaProblem.save(dsa_problem, output_folder, problem_code, overwrite=True)
            copy_tree(problem_folder, os.path.join(output_folder, problem_code, "_vi"))
        # break


def rearrange_codeforce_problems():
    problems = read_all_problems("/home/thuc/projects/ucode/dsa-problems/codeforces_new", 1)

    for prob in problems:
        difficulty = Codeforces.original_difficulty(prob[1].difficulty)
        problem_folder = os.path.dirname(prob[0])
        problem_name = os.path.basename(prob[0])
        print("current path:", problem_folder, "problem_name:", problem_name)
        old_problem_folder = f"/home/thuc/projects/ucode/dsa-problems/codeforces/" \
                             f"{os.path.basename(problem_folder).capitalize()}"
        print("old path:", old_problem_folder)
        if not os.path.exists(old_problem_folder):
            raise Exception(f"not found: {old_problem_folder}")
        new_base = f"/home/thuc/projects/ucode/dsa-problems/codeforces/difficulty_{difficulty}"

        copy_tree(os.path.join(problem_folder, problem_name), os.path.join(new_base, problem_name))
        copy_tree(old_problem_folder, os.path.join(new_base, problem_name, "_vi"))
        print("new base:", new_base)
        if not os.path.exists(new_base):
            os.makedirs(new_base)
        print(prob[1].src_url, '-', difficulty, '-', prob[0])


if __name__ == "__main__":
    # list all problem
    # folder = "/home/thuc/projects/ucode/dsa-problems/codeforces"
    # problems = read_all_problems(folder, 1)
    # for prob in problems:
    #     difficulty = Codeforces.original_difficulty(prob[1].difficulty)
    #     print(prob[1].src_url, '-', difficulty, '-', prob[1].name, '-', ",".join(prob[1].tags), '-', prob[0])
    # rearrange_codeforce_problems()
    # get_all_codeforce_problem(folder)

    get_all_kattis_problem("/home/thuc/projects/ucode/dsa-problems/katis/unsorted")
