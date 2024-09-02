import os
import sys
import time
import requests
from colorama import *
from datetime import datetime, timezone


script_dir = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(script_dir, "init_data.txt")


class TabiZoo:
    def __init__(self):
        self.line = Fore.LIGHTWHITE_EX + "-" * 50

    def headers(self, data):
        return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://miniapp.tabibot.com",
        "Pragma": "no-cache",
        "Referer": "https://miniapp.tabibot.com/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        "Rawdata": f"{data}",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36'
    }

    def user_info(self, data):
        url = f"https://api.tabibot.com/api/user/v1/profile"
        headers = self.headers(data=data)
        response = requests.get(url=url, headers=headers)
        return response

    def mining_info(self, data):
        url = f"https://api.tabibot.com/api/mining/v1/info"
        headers = self.headers(data=data)
        response = requests.get(url=url, headers=headers)
        return response

    def check_in(self, data):
        url = f"https://api.tabibot.com/api/user/v1/check-in"
        headers = self.headers(data=data)
        response = requests.post(url=url, headers=headers)
        return response

    def level_up(self, data):
        url = f"https://api.tabibot.com/api/user/v1/level-up"
        headers = self.headers(data=data)
        response = requests.post(url=url, headers=headers)
        return response

    def claim(self, data):
        url = f"https://api.tabibot.com/api/mining/v1/claim"
        headers = self.headers(data=data)
        response = requests.post(url=url, headers=headers)
        return response

    def task_info(self, data):
        url = f"https://api.tabibot.com/api/task/v1/list"
        headers = self.headers(data=data)
        response = requests.get(url=url, headers=headers)
        return response

    def do_task(self, data, task_tag):
        url = "https://api.tabibot.com/api/task/v1/verify/task"
        headers = self.headers(data=data)
        payload = {"task_tag": task_tag}
        response = requests.post(url=url, headers=headers, json=payload)
        return response

    def banner_info(self, data):
        url = f"https://api.tabibot.com/api/task/v1/mine/banners"
        headers = self.headers(data=data)
        response = requests.get(url=url, headers=headers)
        return response

    def banner_task(self, data, task_tag):
        url = f"https://api.tabibot.com/api/task/v1/mine?project_tag=mine_{task_tag}"
        headers = self.headers(data=data)

        response = requests.get(url=url, headers=headers)
        return response

    def do_banner(self, data, task_tag):
        url = "https://api.tabibot.com/api/task/v1/verify/task"
        headers = self.headers(data=data)
        payload = {"task_tag": task_tag}
        response = requests.post(url=url, headers=headers, json=payload)
        return response

    def do_project(self, data, task_tag):
        url = "https://api.tabibot.com/api/task/v1/verify/project"
        headers = self.headers(data=data)
        payload = {"project_tag": f"mine_{task_tag}"}
        response = requests.post(url=url, headers=headers, json=payload)
        return response

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{Fore.LIGHTBLACK_EX}[{now}]{Style.RESET_ALL} {message}")

    def main(self):
        while True:

            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{Fore.LIGHTYELLOW_EX}Аккаунтов: {Fore.LIGHTWHITE_EX}{num_acc}")
            end_at_list = []
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{Fore.LIGHTYELLOW_EX}Номер аккаунта: {Fore.LIGHTWHITE_EX}{no+1}/{num_acc}")

                try:
                    user_info = self.user_info(data=data).json()

                    user = user_info["data"]["user"]

                    username = user["name"]
                    balance = user["coins"]
                    level = user["level"]
                    streak = user["streak"]
                    self.log(f"{Fore.LIGHTYELLOW_EX}Аккаунт: {Fore.LIGHTWHITE_EX}{username}")
                    self.log(f"{Fore.LIGHTYELLOW_EX}Балланс: {Fore.LIGHTWHITE_EX}{balance:,}")
                    self.log(f"{Fore.LIGHTYELLOW_EX}Уровень: {Fore.LIGHTWHITE_EX}{level}")
                    self.log(f"{Fore.LIGHTYELLOW_EX}Streak: {Fore.LIGHTWHITE_EX}{streak}")
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка получения информации об аккаунте: {str(e)}")
                time.sleep(1)
                try:
                    response = self.task_info(data=data)

                    if response.text.strip():
                        tasks2 = response.json()


                        for project2 in tasks2.get('data', []):
                            task_listt = project2.get('task_list', [])
                            for task in task_listt:
                                status = task.get("user_task_status")
                                if status == 2:
                                    tag = task.get('task_tag')
                                    dtask3 = self.do_task(data=data, task_tag=tag).json()

                                    if dtask3.get("message") == "success":
                                        reward = dtask3["data"]['reward']
                                        self.log(
                                            f"{Fore.LIGHTYELLOW_EX}Выполнил задание: {Fore.LIGHTWHITE_EX}{tag} {Fore.LIGHTYELLOW_EX}Получено: {Fore.LIGHTWHITE_EX}{reward}")

                    else:

                        return response

                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка заданий: {e}")
                time.sleep(1)
                try:
                    tasks = self.banner_info(data=data).json()

                    for project in tasks.get('data', []):
                        task_list = project.get('title', [])

                        dtask = self.banner_task(data=data, task_tag=task_list).json()

                        status_d = dtask["data"]["user_project_status"]
                        if status_d == 2:
                            task_list1 = dtask["data"].get("list", [])
                            all_status_one = False
                            for task1 in task_list1:
                                status = task1.get("user_task_status")

                                if status == 2:
                                    tag = task1.get('task_tag')
                                    self.do_banner(data=data, task_tag=tag).json()
                                else:
                                    all_status_one = True
                            if all_status_one:

                                proj = self.do_project(data=data, task_tag=task_list).json()

                                if proj.get("message") == "success":
                                    rew = proj["data"]["reward"]
                                    self.log(f"{Fore.LIGHTYELLOW_EX}Выполнил задание: {Fore.LIGHTWHITE_EX}{task_list} {Fore.LIGHTYELLOW_EX}Получено: {Fore.LIGHTWHITE_EX}{rew}")

                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка заданий: {e}")
                time.sleep(1)
                try:
                    info = self.claim(data=data).json()

                    claim = info["data"]
                    if claim:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Забрал награду")
                    else:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Еще не прощел кулдаун награды")
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка награды!")
                time.sleep(1)
                try:
                    check_in = self.check_in(data=data).json()

                    if check_in["data"]["check_in_status"] == 1:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Чекин сделан")
                    else:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Еще не пришло время чекина")
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка чекина!")
                time.sleep(1)
                try:
                    level_up = self.level_up(data=data).json()

                    current_level = level_up['data']['user']["level"]
                    if level_up["message"] == "success":
                        self.log(f"{Fore.LIGHTYELLOW_EX}Улучшил")
                        self.log(f"{Fore.LIGHTYELLOW_EX}Ваш новый уровень: {Fore.LIGHTWHITE_EX}{current_level}")

                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Не хватает монет для улучшения!")
                time.sleep(1)
                try:
                    mining_info = self.mining_info(data=data).json()

                    end_time = mining_info['data']['mining_data']["next_claim_time"]
                    end_at_list.append(end_time)
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка получения кулдауна!")

            if end_at_list:
                now = datetime.now(timezone.utc).timestamp()
                wait_times = []
                for end_at_str in end_at_list:
                    end_at = datetime.fromisoformat(end_at_str.replace("Z", "+00:00"))
                    if end_at.timestamp() > now:
                        wait_times.append(end_at.timestamp() - now)

                if wait_times:
                    wait_time = min(wait_times)
                else:
                    wait_time = 15 * 60
            else:
                wait_time = 15 * 60

            wait_hours = int(wait_time // 3600)
            wait_minutes = int((wait_time % 3600) // 60)

            wait_message_parts = []
            if wait_hours > 0:
                wait_message_parts.append(f"{wait_hours} часов")
            if wait_minutes > 0:
                wait_message_parts.append(f"{wait_minutes} минут")

            wait_message = ", ".join(wait_message_parts)
            self.log(f"Жду {wait_message}!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        tabi = TabiZoo()
        tabi.main()
    except KeyboardInterrupt:
        sys.exit()
