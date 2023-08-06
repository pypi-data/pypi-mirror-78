import requests

BASE = "http://207.244.227.19:69/"


def total_memory(url):
    try:
        response = requests.get(BASE + "meminfo")
        data = response.json()['data']
        total_memory = float(round(int(data['MemTotal'])/1e+6, 2))
        # print(f"free mem: {float(round(int(data['MemFree'])/1e+6, 2))} GB")
        # print(f"ava mem: {float(round(int(data['MemAvailable'])/1e+6, 2))} GB")
        # print(f"cache mem: {float(round(int(data['Cached'])/1e+6, 2))} GB")
        # print(f"active mem: {float(round(int(data['Active'])/1e+6, 2))} GB")
        # print(f"inactive mem: {float(round(int(data['Inactive'])/1e+6, 2))} GB")
        #print(f"swap total: {float(round(int(data['SwapTotal'])/1e+6, 2))} GB")
        return total_memory
    except:
        return "-"
