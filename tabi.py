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
            "Host": "app.tabibot.com",
            "Origin": "https://app.tabibot.com",
            "Pragma": "no-cache",
            "Rawdata": f"{data}",
            "Referer": "https://app.tabibot.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        }
    def user_info(self, data):
        url = f"https://app.tabibot.com/api/user/profile"
        headers = self.headers(data=data)
        response = requests.get(url=url, headers=headers)
        return response

    def mining_info(self, data):
        url = f"https://app.tabibot.com/api/mining/info"
        headers = self.headers(data=data)
        response = requests.get(url=url, headers=headers)
        return response

    def check_in(self, data):
        url = f"https://app.tabibot.com/api/user/check-in"
        headers = self.headers(data=data)
        response = requests.post(url=url, headers=headers)
        return response

    def level_up(self, data):
        url = f"https://app.tabibot.com/api/user/level-up"
        headers = self.headers(data=data)
        response = requests.post(url=url, headers=headers)
        return response

    def claim(self, data):
        url = f"https://app.tabibot.com/api/mining/claim"
        headers = self.headers(data=data)
        response = requests.post(url=url, headers=headers)
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
                    username = user_info["name"]
                    balance = user_info["coins"]
                    level = user_info["level"]
                    self.log(f"{Fore.LIGHTYELLOW_EX}Аккаунт: {Fore.LIGHTWHITE_EX}{username}")
                    self.log(f"{Fore.LIGHTYELLOW_EX}Балланс: {Fore.LIGHTWHITE_EX}{balance:,}")
                    self.log(f"{Fore.LIGHTYELLOW_EX}Уровень: {Fore.LIGHTWHITE_EX}{level}")

                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка получения информации об аккаунте: {str(e)}")

                try:
                    claim = self.claim(data=data).json()
                    if claim:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Забрал награду")
                    else:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Еще не прощел кулдаун награды")
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка награды!")

                # Check in
                try:
                    check_in = self.check_in(data=data).json()
                    if check_in["hasCheckedIn"]:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Чекин сделан")
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка чекина!")

                try:
                    level_up = self.level_up(data=data).json()
                    current_level = level_up["level"]
                    if current_level > level:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Улучшил")
                        self.log(f"{Fore.LIGHTYELLOW_EX}Ваш новый уровень: {Fore.LIGHTWHITE_EX}{current_level}")
                    else:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Не хватает монет для улучшения")
                except Exception as e:
                    self.log(f"{Fore.LIGHTRED_EX}Ошибка улучшения уровня!")

                try:
                    mining_info = self.mining_info(data=data).json()
                    end_time = mining_info["nextClaimTime"]
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
