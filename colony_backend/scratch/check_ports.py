import socket

def check():
    ports = [8000, 1080, 1081, 1082, 1083, 1084]
    print("--- PORT AUDIT ---")
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        res = s.connect_ex(('127.0.0.1', p))
        status = "OPEN" if res == 0 else "CLOSED"
        print(f"Port {p}: {status}")
        s.close()

if __name__ == "__main__":
    check()
