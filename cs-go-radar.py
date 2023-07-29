import pymem
from time import sleep
import requests

def get_offset(url = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the JSON file: {e}")
        return None

def radar(offsets = get_offset()) -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll
    
    while True:
        localPlayer = pm.read_uint(client + offsets["signatures"]["dwLocalPlayer"])

        for i in range(1,64):
            entity = pm.read_uint(client + offsets["signatures"]["dwEntityList"] + i * 0x10)
            
            #if the entity is not empty and not localPlayer
            if entity == 0 or entity == localPlayer:
                continue

            #if entity and localPlayer are not on the same team
            if pm.read_uint(entity + offsets["netvars"]["m_iTeamNum"]) == pm.read_uint(localPlayer + offsets["netvars"]["m_iTeamNum"]):
                continue

            pm.write_bool(entity + offsets["netvars"]["m_bSpotted"], True)

        sleep(0.01)
if __name__ == "__main__":
    radar()