# coding=utf-8
import asyncio
import csv
import json
import logging
# pip install websocket-client
from datetime import datetime

import websocket

__author__ = 'ThucNC'

from tabulate import tabulate

from ptoolbox.airtable.airtable import Airtable
from ptoolbox.helpers.clog import CLog
from ptoolbox.helpers.crandom import CRandom

_logger = logging.getLogger(__name__)


class Codesignal:
    def __init__(self):
        id = CRandom.string(3, "123456789")
        key = CRandom.string(8)
        ws_uri = f"wss://app.codesignal.com/sockjs/{id}/{key}/websocket"

        ws = websocket.WebSocket()
        ws.connect(ws_uri)
        self.ws = ws

        self.wait_for(["server_id"])
        cmd_connection = ["{\"msg\":\"connect\",\"version\":\"1\",\"support\":[\"1\",\"pre2\",\"pre1\"]}"]
        ws.send(json.dumps(cmd_connection))
        self.wait_for(["connected", "added"])

    def execute_and_wait(self, cmd):
        id = CRandom.string(17)
        cmd = json.dumps(cmd).replace("{{id}}", id)
        self.ws.send(cmd)
        return self.wait_for(["ready", id])

    def get_users_by_ids(self, user_ids):
        """
        return
        [
            {
                "msg": "added",
                "collection": "users",
                "id": "2G6b5RKzCJxPW8geK",
                "fields": {
                  "country": "VN",
                  "initialsAvatar": "https://codesignal.s3.amazonaws.com/avatar-profile-2G6b5RKzCJxPW8geK-1558770770295?_tm=1558770770490",
                  "language": "py3",
                  "primaryLanguage": "go",
                  "privacySettings": {
                    "activities": "everyone",
                    "avatar": "friends",
                    "background": {
                      "roles": "everyone",
                      "location": "partners",
                      "experience": "everyone",
                      "phone": "partners",
                      "linkedinUrl": "partners",
                      "githubUrl": "partners",
                      "skills": "everyone"
                    },
                    "codingScore": "partners",
                    "education": "me",
                    "experience": "me",
                    "email": "everyone",
                    "name": "friends"
                  },
                  "stats": {
                    "badgeProgress": {
                      "recruiter": 0.6
                    }
                  },
                  "username": "haku",
                  "xp": 163367
                }
            }
        ]
        :param user_ids:
        :return:
        """
        ids_str = str(json.dumps(user_ids))
        cmd = ["{\"msg\":\"sub\",\"id\":\"{{id}}\",\"name\":\"users.byIds\",\"params\":[" + ids_str + "]}"]
        return self.execute_and_wait(cmd)

    def get_tournament_info(self, tournament_id: str):
        """
        return:
        {
          "msg": "added",
          "collection": "tournaments",
          "id": "WmYmJ3ydfHAomAZaq",
          "fields": {
            "type": "marathon",
            "title": "CodeMaster's tourney",
            "private": false,
            "duration": 600000,
            "prize": 2000,
            "authorId": null,
            "auto": true,
            "autoTaskSelection": true,
            "startDate": 1597284001450,
            "status": "over",
            "created": 1597283706221,
            "createdDate": 1597283706221,
            "participantCount": 8,
            "feedActionId": "nmPqNkQ2rvAjTCRud",
            "endDate": 1597284603329,
            "taskIds": [
              "5sAQ8p7YsxJvmrTFh",
              "nhzm9BbCKWpE6TRfw",
              "hqrYesGKEaKQnv7Sv",
              "ND8nghbndTNKPP4Tb",
              "LJmqE7h7cNtihQbDa"
            ],
            "pendingRuns": 0,
            "needsFinalize": false
          }
        }

        :param tournament_id:
        :return:
        """
        cmd = ["{\"msg\":\"sub\",\"id\":\"{{id}}\",\"name\":\"tournament\","
                          "\"params\":[\"" + tournament_id + "\"]}"]
        return self.execute_and_wait(cmd)[0]

    def get_tournament_standing(self, tournament_id: str):
        """
        return:
        [
            {
                "msg": "added",
                "collection": "tournamentParticipants",
                "id": "cai7CSmAwvb8AjhDG",
                "fields": {
                  "tournamentId": "vRPK5SKeXSPHPn9qg",
                  "userId": "gTndquYQbKwnW5DsB",
                  "username": "jpt44_yummi_fjs"
                  "country": "VN",
                  "userXP": 131475,
                  "date": 1559816716062,
                  "score": 1100,
                  "timePenalty": 110776,
                  "taskScores": [
                    {
                      "status": "correct",
                      "score": 100,
                      "timePenalty": 110776,
                      "submitAttempts": 1
                    },
                    {
                      "status": "correct",
                      "score": 100,
                      "timePenalty": 62403,
                      "submitAttempts": 1
                    },
                    {
                      "status": "correct",
                      "score": 300,
                      "timePenalty": 35081,
                      "submitAttempts": 1
                    },
                    {
                      "status": "correct",
                      "score": 300,
                      "timePenalty": 91224,
                      "submitAttempts": 1
                    },
                    {
                      "status": "correct",
                      "score": 300,
                      "timePenalty": 43834,
                      "submitAttempts": 1
                    }
                  ],
                  "xp": 2200,
                }
            }
        ]
        :param tournament_id:
        :return:
        """
        cmd = ["{\"msg\":\"sub\",\"id\":\"{{id}}\",\"name\":\"tournamentStandings\","
               "\"params\":[{\"tournamentId\":\"" + tournament_id + "\",\"offset\":0,\"limit\":100}]}"]
        tournament_ranking = []
        for item in self.execute_and_wait(cmd):
            if item['collection'] == 'tournamentParticipants':
                tournament_ranking.append(item)

        user_ids = [item['fields']['userId'] for item in tournament_ranking]
        users = self.get_users_by_ids(user_ids)
        users_dict = {}
        for user in users:
            users_dict[user['id']] = user['fields']['username']
        # print("Users:", len(users), json.dumps(users))
        for item in tournament_ranking:
            item['fields']['username'] = users_dict[item['fields']['userId']]

        return tournament_ranking

    def get_tournament_result(self, tournament: str):
        """
        :param tournament: codesignal tournament id or url
        :return:
        """
        if "/" in tournament:
            tournament = tournament[tournament.rfind("/") + 1 :]

        CLog.info(f"Getting result of tournament `{tournament}`: "
                  f"https://app.codesignal.com/tournaments/{tournament} ...")

        tournament_info = self.get_tournament_info(tournament)
        tournament_standing = self.get_tournament_standing(tournament)

        return tournament_info, tournament_standing

    def wait_for(self, strs):
        res = []
        while True:
            recv = self.ws.recv()
            # print("recv", recv)
            # recv: a["{\"server_id\":\"0\"}"]
            if "a[" not in recv:
                continue
            data = recv[1:]
            data = json.loads(data)

            for i, item in enumerate(data):
                data[i] = json.loads(item)

            print("data", json.dumps(data))
            if 'msg' in data[0] and data[0]['msg'] != "ready":
                res.append(data[0])
            i = 0
            while i < len(strs):
                s = strs[i]
                if s in recv:
                    CLog.echo(f"Got `{s}`")
                    strs.pop(i)
                else:
                    i += 1

            if not strs:
                break
        return res

    def re_judge(self, tournament_standing):
        """
        Only count full-score task
        :param tournament_standing:
        :return:
        """
        for i, item in enumerate(tournament_standing):
            task_score = [100, 100, 300, 300, 300]
            total_score = 0
            time_penalty = 0
            for task_id in range(5):
                if item["fields"]["taskScores"][task_id]["score"] < task_score[task_id]:
                    item["fields"]["taskScores"][task_id]["score"] = 0
                    item["fields"]["taskScores"][task_id]["timePenalty"] = 0
                    item["fields"]["taskScores"][task_id]["status"] = "partial"
                total_score += item["fields"]["taskScores"][task_id]["score"]
                time_penalty = max(time_penalty, item["fields"]["taskScores"][task_id]["timePenalty"])
            item["fields"]["score"] = total_score
            item["fields"]["timePenalty"] = time_penalty
        tournament_standing.sort(key=lambda k: (1100-k["fields"]["score"]) * 1000000 + k["fields"]["timePenalty"])
        return tournament_standing

    def tournament_standing_format(self, tour_info, tournament_standing):
        res = []
        for i, item in enumerate(tournament_standing):
            res.append({
                "tournament_id": tour_info['id'],
                "tournament_time": int(round(tour_info['fields']['startDate']/1000)),
                "rank": i+1,
                "username": item["fields"]["username"],
                "country": item["fields"]["country"],
                "A": item["fields"]["taskScores"][0]["score"],
                "A_t": int(round(item["fields"]["taskScores"][0]["timePenalty"]/1000)),
                "B": item["fields"]["taskScores"][1]["score"],
                "B_t": int(round(item["fields"]["taskScores"][1]["timePenalty"]/1000)),
                "C": item["fields"]["taskScores"][2]["score"],
                "C_t": int(round(item["fields"]["taskScores"][2]["timePenalty"]/1000)),
                "D": item["fields"]["taskScores"][3]["score"],
                "D_t": int(round(item["fields"]["taskScores"][3]["timePenalty"]/1000)),
                "E": item["fields"]["taskScores"][4]["score"],
                "E_t": int(round(item["fields"]["taskScores"][4]["timePenalty"]/1000)),
                "score": item["fields"]["score"],
                "time": int(round(item["fields"]["timePenalty"])/1000),
                "xp": item["fields"]["score"],
            })
        return res

    def f_time(self, second):
        return f"{second // 60}:{second % 60:02d}"

    def tournament_json_to_ascii_table(self, tour_json):
        header = ["#", "User", "Country", "A", "B", "C", "D", "E", "Score",
                  "A_t", "B_t", "C_t", "D_t", "E_t", "Time", "XP"]
        table = []
        for item in tour_json:
            table.append([
                item['rank'], item['username'], item['country'],
                item['A'], item['B'], item['C'], item['D'], item['E'], item['score'],
                self.f_time(item['A_t']), self.f_time(item['B_t']), self.f_time(item['C_t']),
                self.f_time(item['D_t']),self.f_time(item['E_t']),
                self.f_time(item["time"]), item['xp']
            ])

        return tabulate(table, headers=header)

    def read_user_map(self, csv_file="user_map.csv"):
        """
        Read user map list from csv file, eg.:
            thucnguyen	Nguyễn Chí Thức
            quypn	Phạm Ngọc Quý
            danthanh_n	Nguyễn Thạc Đan Thanh
            nghetienhiep	Nghê Tiến Hiệp
        :param csv_file:
        :return:
        """
        with open(csv_file) as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            users = {}
            for row in reader:
                users[row[0]] = row[1]
            return users

    def tournament_standing_to_airtable(self, formatted_standing, airtable: Airtable, user_map=None):
        recs = []
        joined_users = set()
        date_str = datetime.utcfromtimestamp(formatted_standing[0]['tournament_time']).isoformat()
        for item in formatted_standing:
            joined_users.add(item['username'])
            rec = {
                "date": date_str,
                # "date": item['tournament_time'],
                "username": item['username'],
                "rank": item['rank'],
                "A": item['A'],
                "B": item['B'],
                "C": item['C'],
                "D": item['D'],
                "E": item['E'],
                "time": item['time'],
                "XP": item['xp'],
                "tournament": f"https://app.codesignal.com/tournaments/{item['tournament_id']}",
                "score": item['score'],
                "check": True,
            }
            if user_map:
                rec['name'] = user_map.get(item['username'], "")
            recs.append(rec)

        for user in user_map:
            if user not in joined_users:
                rec = {
                    "date": date_str,
                    "username": user,
                    "name": user_map[user],
                    "rank": 1000,
                    "score": -1,
                    "check": False,
                }
                recs.append(rec)

        res = airtable.batch_insert(recs)
        print("Inserted:", len(res), res)

        return res


if __name__ == '__main__':
    # uri = "https://app.codesignal.com/tournaments/WmYmJ3ydfHAomAZaq"
    uri = "https://app.codesignal.com/tournaments/MRkDYWPBMbEb2mdER"
    # uri = "wss://app.codesignal.com/sockjs/885/ikhnrug9/websocket"
    cs = Codesignal()
    tour_info, tour_standing = cs.get_tournament_result(uri)
    tournament_id = tour_info['id']
    tournament_task_ids = tour_info['fields']['taskIds']
    print("Tournament info", json.dumps(tour_info))
    print(f"Tournament id: '{tournament_id}'")
    print(f"Tournament task ids: `{tournament_task_ids}`")
    print(f"Tournament standing: {len(tour_standing)}", json.dumps(tour_standing))

    tour_json = cs.tournament_standing_format(tour_info, tour_standing)
    print(cs.tournament_json_to_ascii_table(tour_json))

    tour_standing = cs.re_judge(tour_standing)
    print(f"\n\nrejudge: {len(tour_standing)}", json.dumps(tour_standing))
    tour_json = cs.tournament_standing_format(tour_info, tour_standing)
    print(f"\n\nREJUDGE result:\n")
    print(cs.tournament_json_to_ascii_table(tour_json))

    users = cs.read_user_map("../../user_map.csv")
    airtable = Airtable(api_key="key7AsmElRf7gYGLD", base_id="appjq5RyjSUAAbFwZ", table_name="cs_raw_log")
    cs.tournament_standing_to_airtable(formatted_standing=tour_json, airtable=airtable, user_map=users)

