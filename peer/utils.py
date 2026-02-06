import socket

def get_local_ip():
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1" 


def create_messagebox(user_friends):
    messagebox = {}
    new_message_flags = {}
    for friend in user_friends:
        messagebox[friend] = []
        new_message_flags[friend] = False

    return messagebox, new_message_flags

def print_messages(messages, username):
    for messsage in messages:
        if messsage["from"] == username:
            print("[YOU]: " + messsage["message"])
        else:
            message_from = messsage["from"]
            print(f"[{message_from}]: " + messsage["message"])