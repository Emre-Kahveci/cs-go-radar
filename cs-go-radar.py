import pymem
from time import sleep

# Offsets
offsets = {
    'entityList': 0x4DFFF7C,
    'localPlayer': 0xDEA98C,
    'teamNum': 0xF4,
    'spotted': 0x93D,
}

def radar() -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll
    
    while True:
        localPlayer = pm.read_uint(client + offsets["localPlayer"])

        for i in range(1,64):
            entity = pm.read_uint(client + offsets["entityList"] + i * 0x10)
            
            #if the entity is not empty and not localPlayer
            if entity == 0 or entity == localPlayer:
                continue

            #if entity and localPlayer are not on the same team
            if pm.read_uint(entity + offsets["teamNum"]) == pm.read_uint(localPlayer + offsets["teamNum"]):
                continue

            pm.write_bool(entity + offsets["spotted"], True)

        sleep(0.01)
if __name__ == "__main__":
    radar()