import requests
import random
import time
import urllib.parse
import json

# Function to read data from file data.txt and extract user_id
def load_user_data(filename):
    with open(filename, "r") as file:
        data = file.readlines()
    
    user_data = []
    for line in data:
        # Extract the `user` part of the payload
        parsed_data = urllib.parse.parse_qs(line.strip())
        user_info = parsed_data.get('user', [None])[0]
        if user_info:
            user_info_decoded = urllib.parse.unquote(user_info)
            user_info_dict = json.loads(user_info_decoded)  # Using json.loads instead of eval for safety
            user_id = user_info_dict.get("id")
            username = user_info_dict.get("username")
            user_data.append((user_id, username, line.strip()))
    
    return user_data

# URL and Header
login_url = "https://ago-api.hexacore.io/api/app-auth"  # Make sure this is defined here
user_exists_url = "https://ago-api.hexacore.io/api/user-exists"
balance_url_template = "https://ago-api.hexacore.io/api/balance/{}"
daily_checkin_url = "https://ago-api.hexacore.io/api/daily-checkin"
available_taps_url = "https://ago-api.hexacore.io/api/available-taps"
buy_taps_url = "https://ago-api.hexacore.io/api/buy-tap-passes"
mining_complete_url = "https://ago-api.hexacore.io/api/mining-complete"

headers = {
    "Content-Type": "application/json",
    "Origin": "https://ago-wallet.hexacore.io",
    "Referer": "https://ago-wallet.hexacore.io/",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

# Function to login and get token from data.txt
def login_from_data(data_line):
    payload = {"data": data_line}
    print(f"Fetching Data For Login")
    response = requests.post(login_url, json=payload, headers=headers)
    try:
        response_data = response.json()
        token = response_data.get("token")
        if token:
            # Extract user_info part to get user_id
            parsed_data = urllib.parse.parse_qs(data_line)
            user_info = parsed_data.get('user', [None])[0]
            if user_info:
                user_info_decoded = urllib.parse.unquote(user_info)
                print(f"Decoded user_info: ........")  # Debug print
                user_info_dict = json.loads(user_info_decoded)  # Safely parse JSON-like string
                user_id = user_info_dict.get("id")
                print(f"Token successfully obtained: ........")
                return token, user_id
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response. Response content:")
        print(response.text)
    return None, None

# Function to check if user exists
def check_user_exists(token):
    headers['Authorization'] = token
    response = requests.get(user_exists_url, headers=headers)
    return response.json().get("exists")

# Function to get balance
def get_balance(user_id, token):
    balance_url = balance_url_template.format(user_id)
    headers['Authorization'] = token
    response = requests.get(balance_url, headers=headers)
    
    if response.status_code == 200:
        try:
            balance_data = response.json()
            return balance_data.get("user_id"), balance_data.get("balance")
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON response during balance retrieval. Response content:")
            print(response.text)
            return None, None
    else:
        print(f"Failed to retrieve balance. HTTP Status Code: {response.status_code}")
        print("Response content:")
        print(response.text)
        return None, None

# Function for daily check-in
def daily_checkin(token):
    headers['Authorization'] = token
    checkin_payload = {"day": random.randint(1, 20)}
    response = requests.post(daily_checkin_url, json=checkin_payload, headers=headers)
    return response.json().get("available_at"), response.json().get("success")

# Function to check available taps
def check_available_taps(token):
    headers['Authorization'] = token
    response = requests.get(available_taps_url, headers=headers)
    return response.json().get("available_taps")

# Function to buy taps
def buy_taps(token):
    headers['Authorization'] = token
    buy_taps_options = ["1_days", "3_days", "7_days"]
    buy_taps_payload = {"name": random.choice(buy_taps_options)}
    
    response = requests.post(buy_taps_url, json=buy_taps_payload, headers=headers)
    
    try:
        response_data = response.json()
        return response_data.get("success")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response. Response content:")
        print(response.text)
        return None

# Function to complete mining
def mining_complete(token):
    headers['Authorization'] = token
    mining_payload = {"taps": random.randint(50, 150)}
    response = requests.post(mining_complete_url, json=mining_payload, headers=headers)
    print(f"Mining Payload: {mining_payload}")
    return response.json().get("success")

# Main function to execute the entire process sequentially for each user
def main():
    data_file = "data.txt"
    user_data_list = load_user_data(data_file)
    
    while True:
        for user_id, username, data_line in user_data_list:
            print(f"\nProcessing user: {username} (ID: {user_id})")
            token, user_id = login_from_data(data_line)
            if token:
                print(f"Token: Successfully Obtained")

                # Check if user exists
                exists = check_user_exists(token)
                print(f"User Exists: {exists}")

                # Get balance
                user_id, balance = get_balance(user_id, token)
                print(f"User ID: {user_id}, Balance: {balance}")

                # Daily check-in
                available_at, success = daily_checkin(token)
                print(f"Daily Check-in: Success={success}, Available at={available_at}")

                # Check available taps
                available_taps = check_available_taps(token)
                print(f"Available Taps: {available_taps}")

                # Buy taps
                success = buy_taps(token)
                print(f"Buy Taps: Success={success}")

                # Mining complete
                success = mining_complete(token)
                print(f"Mining Complete: Success={success}")

                # Countdown before next user iteration
                delay = random.randint(5, 10)
                print(f"Waiting for {delay} seconds before processing the next user...")
                for i in range(delay, 0, -1):
                    print(f"{i} seconds remaining...", end="\r")
                    time.sleep(1)
            else:
                print("Login failed!")

        print("\nAll users processed. Starting the next cycle...")
        time.sleep(30)  # Delay before starting the next full cycle of all users

if __name__ == "__main__":
    main()
