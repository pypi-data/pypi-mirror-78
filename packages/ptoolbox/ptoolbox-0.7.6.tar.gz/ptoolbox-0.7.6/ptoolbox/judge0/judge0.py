# coding=utf-8
import json
import logging
import requests

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


def get_languages():
    url = "https://j0.ucode.vn/languages"

    response = requests.request("GET", url)

    res = json.loads(response.text)
    print(json.dumps(res))


def post_submission():
    url = "https://j0.ucode.vn/submissions"

    payload = {
        "language_id": 50,
        "source_code": """#include <stdio.h>
    int main(void) {
      char name[10];
      scanf("%s", name);
      printf("hello %s", name);
      return 0;
    }""",
        "stdin": "world"}

    headers = {
        'content-type': "application/json",
        'accept': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print(response.text)


def get_submission(id):
    url = f"https://j0.ucode.vn/submissions/{id}"

    response = requests.request("GET", url)

    print(response.text)


if __name__ == "__main__":
    # get_languages()
    # post_submission()
    get_submission("d376f121-cbf6-4787-815d-2bf64a25b483")

