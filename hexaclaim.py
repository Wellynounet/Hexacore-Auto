import requests

# URL endpoints
BASE_URL = "https://hexacore-tg-api.onrender.com/api"
auth_url = f"{BASE_URL}/app-auth"
mission_url = "https://twitter.com/intent/tweet?text=Join%20me%20at%20Hexacore%20Gaming%20Universe%20and%20earn%20rewards!%20link:%20{REFERRAL_LINK}"
url_cek_mission = f"{BASE_URL}/mission-complete"
passive_income_url = f"{BASE_URL}/total-passive"
upgrade_level_url = f"{BASE_URL}/upgrade-level"
check_level_url = f"{BASE_URL}/level"
buy_tap_url = f"{BASE_URL}/buy-tap-passes"

status_check_url = {
    "missions": f"{BASE_URL}/status/mission",
    "upgrade_level": f"{BASE_URL}/status/upgrade-level",
    "check_level": f"{BASE_URL}/status/check-level",
    "passive_income": f"{BASE_URL}/status/passive-income",
    "buy_tap": f"{BASE_URL}/status/buy-tap"
}

# Header umum untuk request
common_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://ago-wallet.hexacore.io",
    "Priority": "u=1, i",
    "Referer": "https://ago-wallet.hexacore.io/"
}

# Header khusus untuk otentikasi
auth_headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://ago-wallet.hexacore.io",
    "Referer": "https://ago-wallet.hexacore.io/",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}

def request_with_auth(url, method='GET', headers=None, json=None):
    response = requests.request(method, url, headers=headers, json=json)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed for {url}: {response.text}")
        return None

def is_feature_enabled(feature):
    status = request_with_auth(status_check_url[feature], headers=common_headers)
    return status and status.get("enabled", False)

def read_user_data(filename):
    user_data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                user_data.append((parts[0].strip(), parts[1].strip()))
    return user_data

def print_results(username, mission_results=None, upgrade_level_result=None, check_level_result=None, passive_income_result=None, buy_tap_result=None):
    print("=========HEXA BOT=============")
    print(f"Username: \"{username}\"")
    if mission_results:
        for mission_id, response in mission_results.items():
            print(f"Mission {mission_id}: {response}")
    if upgrade_level_result:
        print(f"Upgrade Level: {upgrade_level_result}")
        if not upgrade_level_result.get("success", True):
            print("Balance not sufficient")
    if check_level_result:
        print(f"Level: {check_level_result}")
    if passive_income_result:
        total_passive_income = passive_income_result.get("total_passive_income", "N/A")
        print(f"Passive Income: {total_passive_income}")
    if buy_tap_result:
        print(f"Buy Tap: {buy_tap_result}")
    print("=" * 80)

def handle_mission(user_data, referral_links):
    for user_id, username in user_data:
        auth_payload = {"user_id": user_id, "username": username}
        auth_response = request_with_auth(auth_url, 'POST', headers=auth_headers, json=auth_payload)
        if auth_response:
            token = auth_response.get("token", "")
            if token:
                common_headers["Authorization"] = f"Bearer {token}"
                print("-" * 80)
                if is_feature_enabled("missions"):
                    mission_results = {}
                    for referral_link in referral_links:
                        full_mission_url = mission_url.replace("{REFERRAL_LINK}", referral_link)
                        print(f"Visiting referral link: {full_mission_url}")
                    for mission_id in mission_ids:
                        mission_response = request_with_auth(url_cek_mission, 'POST', headers=common_headers, json={"missionId": mission_id})
                        mission_results[mission_id] = mission_response if mission_response else {"error": "Failed to complete mission"}
                    print_results(username, mission_results=mission_results)
                else:
                    print("Missions feature is not enabled.")
                print("-" * 80)
            else:
                print(f"Failed to get token for user_id={user_id}, username={username}")
        else:
            print(f"Auth failed for user_id={user_id}, username={username}")

def main():
    user_data = read_user_data('data.txt')
    referral_links = [
        "https://twitter.com/settings/profile",
        "https://twitter.com/Hexacore_UGC",
        "https://twitter.com/pocketspacegg",
        "https://twitter.com/aleks_blanche",
        "https://twitter.com/AlexanderKorch7",
        "https://twitter.com/settings/profile",
        "https://discord.com/invite/2Z8XurKufH"
    ]

    print("=========HEXA BOT=============")
    print("Options:")
    print("1. Claim mission")
    print("2. Upgrade level")
    print("3. Check level")
    print("4. Check passive income")
    print("5. Buy Tap 1 Day")

    choice = input("Enter your choice: ")

    if choice == "1":
        handle_mission(user_data, referral_links)
    elif choice == "2":
        for user_id, username in user_data:
            auth_payload = {"user_id": user_id, "username": username}
            auth_response = request_with_auth(auth_url, 'POST', headers=auth_headers, json=auth_payload)
            if auth_response:
                token = auth_response.get("token", "")
                if token:
                    common_headers["Authorization"] = f"Bearer {token}"
                    if is_feature_enabled("upgrade_level"):
                        upgrade_level_result = request_with_auth(upgrade_level_url, 'POST', headers=common_headers)
                        print_results(username, upgrade_level_result=upgrade_level_result)
                    else:
                        print("Upgrade Level feature is not enabled.")
                else:
                    print(f"Failed to get token for user_id={user_id}, username={username}")
            else:
                print(f"Auth failed for user_id={user_id}, username={username}")
    elif choice == "3":
        for user_id, username in user_data:
            auth_payload = {"user_id": user_id, "username": username}
            auth_response = request_with_auth(auth_url, 'POST', headers=auth_headers, json=auth_payload)
            if auth_response:
                token = auth_response.get("token", "")
                if token:
                    common_headers["Authorization"] = f"Bearer {token}"
                    if is_feature_enabled("check_level"):
                        check_level_result = request_with_auth(check_level_url, headers=common_headers)
                        print_results(username, check_level_result=check_level_result)
                    else:
                        print("Check Level feature is not enabled.")
                else:
                    print(f"Failed to get token for user_id={user_id}, username={username}")
            else:
                print(f"Auth failed for user_id={user_id}, username={username}")
    elif choice == "4":
        for user_id, username in user_data:
            auth_payload = {"user_id": user_id, "username": username}
            auth_response = request_with_auth(auth_url, 'POST', headers=auth_headers, json=auth_payload)
            if auth_response:
                token = auth_response.get("token", "")
                if token:
                    common_headers["Authorization"] = f"Bearer {token}"
                    if is_feature_enabled("passive_income"):
                        passive_income_result = request_with_auth(passive_income_url, headers=common_headers)
                        print_results(username, passive_income_result=passive_income_result)
                    else:
                        print("Passive Income feature is not enabled.")
                else:
                    print(f"Failed to get token for user_id={user_id}, username={username}")
            else:
                print(f"Auth failed for user_id={user_id}, username={username}")
    elif choice == "5":
        for user_id, username in user_data:
            auth_payload = {"user_id": user_id, "username": username}
            auth_response = request_with_auth(auth_url, 'POST', headers=auth_headers, json=auth_payload)
            if auth_response:
                token = auth_response.get("token", "")
                if token:
                    common_headers["Authorization"] = f"Bearer {token}"
                    if is_feature_enabled("buy_tap"):
                        buy_tap_payload = {"name": "1_day"}
                        buy_tap_result = request_with_auth(buy_tap_url, 'POST', headers=common_headers, json=buy_tap_payload)
                        print_results(username, buy_tap_result=buy_tap_result)
                    else:
                        print("Buy Tap feature is not enabled.")
                else:
                    print(f"Failed to get token for user_id={user_id}, username={username}")
            else:
                print(f"Auth failed for user_id={user_id}, username={username}")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
