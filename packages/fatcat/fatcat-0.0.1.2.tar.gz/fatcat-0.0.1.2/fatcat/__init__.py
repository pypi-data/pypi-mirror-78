import requests

class vps():
    def total_memory(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['MemTotal'])/1e+6, 2))
            return total_memory
        except:
            return "-"

    def free_memory(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['MemFree'])/1e+6, 2))
            return total_memory
        except:
            return "-"

    def available_memory(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['MemAvailable'])/1e+6, 2))
            return total_memory
        except:
            return "-"

    def cached_memory(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['Cached'])/1e+6, 2))
            return total_memory
        except:
            return "-"

    def active_memory(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['Active'])/1e+6, 2))
            return total_memory
        except:
            return "-"

    def inactive_memory(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['Inactive'])/1e+6, 2))
            return total_memory
        except:
            return "-"

    def swap_total(self, url):
        try:
            response = requests.get(url + "meminfo")
            data = response.json()['data']
            total_memory = float(round(int(data['SwapTotal'])/1e+6, 2))
            return total_memory
        except:
            return "-"
