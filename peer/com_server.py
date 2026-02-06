import requests

STUN_SERVER_URL = "http://192.168.1.104:8000"
TIMEOUT = 3

def save_message(sender, receiver, content):

    url = f"{STUN_SERVER_URL}/message/create/"

    payload = {
        "sender": sender,
        "receiver": receiver,
        "content": content
    }

    try:
        r = requests.post(url, json=payload, timeout=3)

        if r.status_code == 201:
            return True
        else:
            print("[DB] Save failed:", r.text)
            return False

    except Exception as e:
        print("[DB ERROR]", e)
        return False


def register(username, ip, port):
    payload = {
        "username": username,
        "ip": ip,
        "port": port
    }

    try:
        r = requests.post(
            f"{STUN_SERVER_URL}/register",
            json=payload,
            timeout=TIMEOUT
        )

        if r.status_code in (200, 201):
            print("[STUN] Registered successfully")
            return True
        else:
            print("[STUN] Registration failed:", r.text)
            return False

    except requests.exceptions.RequestException as e:
        print("[STUN ERROR] Cannot reach STUN server")
        return False

def get_peer_info(username):
    try:
        r = requests.get(
            f"{STUN_SERVER_URL}/peerinfo",
            params={"username": username},
            timeout=TIMEOUT
        )

        if r.status_code == 200:
            data = r.json()
            print(f"[STUN] Peer found: {data}")
            return data

        else:
            print("[STUN] Peer not found")
            return None, None

    except requests.exceptions.RequestException:
        print("[STUN ERROR] Cannot reach STUN server")
        return None, None


def get_peers():
    try:
        r = requests.get(
            f"{STUN_SERVER_URL}/peers",
            timeout=TIMEOUT
        )

        if r.status_code == 200:
            peers = r.json()
            usernames = peers['peers']
            return usernames

        else:
            print("[STUN] Failed to fetch peers")
            return []

    except requests.exceptions.RequestException:
        print("[STUN ERROR] Cannot reach STUN server")
        return []

def get_friends(username):
    try:
        r = requests.get(
            f"{STUN_SERVER_URL}/friend/get/",
            params={"username": username},
            timeout=TIMEOUT
        )

        

        if r.status_code == 200:
            data = r.json()
            data = data['friends']
            friends = []
            for friend in data:
                friends.append(friend["username"])
            return friends

        else:
            print("[STUN] Failed to fetch friends")
            return []

    except requests.exceptions.RequestException:
        print("[STUN ERROR] Cannot reach STUN server")
        return []

def friendship(username1, username2):
    payload = {
        "user1": username1,
        "user2": username2,
    }

    try:
        r = requests.post(
            f"{STUN_SERVER_URL}/friend/start/",
            json=payload,
            timeout=TIMEOUT
        )

        if r.status_code in (200, 201):
            print("[STUN] friendship started successfully")
            return True
        else:
            print("[STUN] friendship failed:", r.text)
            return False

    except requests.exceptions.RequestException as e:
        print("[STUN ERROR] Cannot reach STUN server")
        return False
    
def fetch_messages(username1, username2):
    try:
        r = requests.get(
            f"{STUN_SERVER_URL}/message/get/",
            params={"peer1": username1, "peer2": username2},
            timeout=TIMEOUT
        )

        if r.status_code == 200:
            data = r.json()
            data = data['messages']
            return data

        else:
            print("[STUN] Failed to fetch messages")
            return []

    except requests.exceptions.RequestException:
        print("[STUN ERROR] Cannot reach STUN server")
        return []

