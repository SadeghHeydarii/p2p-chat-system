import socket
import threading
from com_server import *
from utils import *

BUFFER_SIZE = 1024

server_socket = None
server_running = True
server_thread = None
my_user = None
logged_in = False
username = None
user_friends = None
messages = None
new_message_flags = None
active_chat_flags = None


# ===============================
# TCP SERVER
# ===============================
def start_server(listen_port):
    global server_socket, server_running

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", listen_port))
        server_socket.listen(5)
        server_socket.settimeout(1.0)

        print(f"🟢 [SERVER] Listening on port {listen_port} ...")

        while server_running:
            try:
                conn, addr = server_socket.accept()
                print(f"🔗 [SERVER] Connected by {addr}")

                data = conn.recv(BUFFER_SIZE)
                if not data:
                    continue
                peer_username = data.decode().strip()

                if peer_username not in user_friends:
                    friendship(username, peer_username)

                threading.Thread(
                    target=handle_peer,
                    args=(conn, peer_username),
                    daemon=True
                ).start()

            except socket.timeout:
                continue
            except OSError as e:
                print(f"⚠️ [SERVER ERROR] Socket closed or error: {e}")
                break
            except Exception as e:
                print(f"⚠️ [SERVER ERROR] {e}")

    except Exception as e:
        print(f"❌ [SERVER INIT ERROR] Failed to start server: {e}")
    finally:
        if server_socket:
            server_socket.close()
        print("🛑 [SERVER] Server stopped")


def handle_peer(conn, peer_username):
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print(f"⚪ [INFO] {peer_username} disconnected")
                break

            msg_text = data.decode().strip()

            if active_chat_flags.get(peer_username, False):
                print(f"💬 [{peer_username}] {msg_text}")
                new_message_flags[peer_username] = False
            else:
                new_message_flags[peer_username] = True

            if len(message_box.get(peer_username, [])) == 0:
                messages = fetch_messages(peer_username, username)
                message_box[peer_username] = messages
            else:
                message_box[peer_username].append({"message": msg_text, "from": peer_username})

    except ConnectionResetError:
        print(f"⚪ [INFO] {peer_username} connection reset")
    except Exception as e:
        print(f"⚠️ [SERVER ERROR] {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass


# ===============================
# TCP CLIENT
# ===============================
def start_client(peer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((peer["ip"], peer["port"]))
        print(f"🔗 [CLIENT] Connected to peer {peer['ip']}:{peer['port']}")

        try:
            client.sendall(username.encode())
        except Exception as e:
            print(f"⚠️ [CLIENT ERROR] Failed to send username: {e}")
            return

        while True:
            try:
                msg = input("✉️ Enter message (type 'exit' to end): ").strip()
            except KeyboardInterrupt:
                print("\n🛑 [CLIENT] Keyboard interrupt, exiting chat...")
                break
            except Exception as e:
                print(f"⚠️ [CLIENT INPUT ERROR] {e}")
                continue

            if msg.lower() == "exit":
                print("✅ [CLIENT] Chat ended")
                break

            try:
                client.sendall(msg.encode())
                save_message(my_user["username"], peer["username"], msg)
                message_box[peer["username"]].append({"message": msg, "from": username})
            except BrokenPipeError:
                print(f"⚪ [INFO] {peer['username']} disconnected")
                break
            except Exception as e:
                print(f"⚠️ [CLIENT ERROR] Failed to send message: {e}")
                break

    except ConnectionRefusedError:
        print(f"⚪ [INFO] Peer {peer['username']} is offline or refused connection")
    except Exception as e:
        print(f"❌ [CLIENT ERROR] {e}")
    finally:
        try:
            client.close()
        except Exception:
            pass
        print("🛑 [CLIENT] Connection closed")


# ===============================
# MAIN
# ===============================
def print_command_prompt():
    print("\n🔹 Available commands: register | login | connect | status | show chat | end chat | logout | exit")
    print("🔹 Enter your command:")


if __name__ == "__main__":

    try:
        while True:
            try:
                command = input("👉 Command: ").strip().lower()
            except KeyboardInterrupt:
                print("\n🛑 Exiting application by user...")
                break
            except Exception as e:
                print(f"⚠️ [INPUT ERROR] {e}")
                continue

            # -------- REGISTER --------
            if command == "register":
                if logged_in:
                    print("❌ Logout first to register again")
                    continue
                try:
                    username = input("Choose username: ").strip()
                    port = int(input("Choose port: ").strip())
                    user_ip = get_local_ip()
                    if register(username, user_ip, port):
                        print("✅ Registered successfully")
                    else:
                        print("❌ Registration failed")
                except ValueError:
                    print("⚠️ Invalid port, please enter a number")
                except Exception as e:
                    print(f"⚠️ [REGISTER ERROR] {e}")

            # -------- LOGIN --------
            elif command == "login":
                if logged_in:
                    print("❌ Already logged in")
                    continue
                try:
                    username = input("Enter your username: ").strip()
                    peers = get_peers()
                    for p in peers:
                        if p["username"] == username:
                            print("✅ Login successful")
                            logged_in = True

                            my_user = get_peer_info(username)
                            user_friends = get_friends(username)
                            message_box, new_message_flags = create_messagebox(user_friends)
                            active_chat_flags = new_message_flags.copy()
                            print("📦 Messages loaded:", message_box)

                            if server_thread is None:
                                server_running = True
                                server_thread = threading.Thread(
                                    target=start_server,
                                    args=(my_user["port"],),
                                    daemon=False
                                )
                                server_thread.start()
                            break
                    else:
                        print("❌ Username not found")
                except Exception as e:
                    print(f"⚠️ [LOGIN ERROR] {e}")

            # -------- CONNECT --------
            elif command == "connect":
                if not logged_in:
                    print("❌ Login first")
                    continue
                try:
                    peer_username = input("Enter peer username to connect: ").strip()
                    peer_info = get_peer_info(peer_username)
                    if peer_username not in user_friends:
                        friendship(username, peer_username)
                    if len(message_box.get(peer_username, [])) == 0:
                        messages = fetch_messages(peer_username, username)
                        message_box[peer_username] = messages
                    if peer_info and peer_info.get("ip"):
                        start_client(peer_info)
                    else:
                        print("❌ Peer not found or offline")
                except Exception as e:
                    print(f"⚠️ [CONNECT ERROR] {e}")

            # -------- STATUS --------
            elif command == "status":
                if not logged_in:
                    print("❌ Login first")
                    continue
                print("📊 Friends status:")
                for friend in user_friends:
                    flag = "*" if new_message_flags.get(friend, False) else ""
                    print(f"👤 {friend} {flag}")

            # -------- SHOW CHAT --------
            elif command == "show chat":
                if not logged_in:
                    print("❌ Login first")
                    continue
                try:
                    peer_username = input("Enter peer username to show chat: ").strip()
                    if len(message_box.get(peer_username, [])) == 0:
                        messages = fetch_messages(peer_username, username)
                        message_box[peer_username] = messages
                    print("💬 Chat with", peer_username)
                    print_messages(message_box[peer_username], username)
                    active_chat_flags[peer_username] = True
                    new_message_flags[peer_username] = False
                except Exception as e:
                    print(f"⚠️ [SHOW CHAT ERROR] {e}")

            # -------- END SHOW CHAT --------
            elif command == "end chat":
                if not logged_in:
                    print("❌ Login first")
                    continue
                try:
                    peer_username = input("Enter peer username to end chat: ").strip()
                    active_chat_flags[peer_username] = False
                    print(f"✅ Chat with {peer_username} ended")
                except Exception as e:
                    print(f"⚠️ [END CHAT ERROR] {e}")

            # -------- LOGOUT --------
            elif command == "logout":
                if not logged_in:
                    print("❌ Not logged in")
                    continue
                print("🔌 Logging out...")
                logged_in = False
                server_running = False
                try:
                    if server_socket:
                        server_socket.close()
                except Exception:
                    pass
                server_thread = None
                username = None
                print("✅ Logged out successfully")

            # -------- EXIT --------
            elif command == "exit":
                print("👋 Exiting application...")
                server_running = False
                try:
                    if server_socket:
                        server_socket.close()
                except Exception:
                    pass
                break

            else:
                print("⚠️ Unknown command! Please try again.")

    except Exception as e:
        print(f"❌ [FATAL ERROR] {e}")
