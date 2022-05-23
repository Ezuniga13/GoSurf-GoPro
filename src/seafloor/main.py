import requests

def get_ocean_floor_elevation():
    response = requests.get('https://api.open-elevation.com/api/v1/lookup?locations=37.4919,-122.4992|37.4919,-122.6|37.4919,-122.8')
    return response.json()


if __name__ == '__main__':
    print(get_ocean_floor_elevation())

