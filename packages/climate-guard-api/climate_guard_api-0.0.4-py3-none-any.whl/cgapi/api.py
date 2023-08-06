from requests import Session
from .error import NotImplemented, Unauthorized


class ClimateGuardApi:
    BASE_URL = 'https://api.climateguard.info'
    API_PREFIX = '/api/telegramBot'
    API_URL = BASE_URL + API_PREFIX
    _request = Session()
    token = ''

    def __init__(self, login: str, password: str, base_url=None):
        if base_url:
            self.BASE_URL = base_url
        token: bool = self.token_obtain(login, password)
        self.token = token
        self._request.headers.update({'Authorization': f'Bearer {token}'})

    def token_obtain(self, login: str, password: str):
        json = {'email': login, 'password': password}
        response = self._request.post(f'{self.BASE_URL}/api/loginViaApi', json=json)
        data = response.json()
        if 'error' in data:
            raise Unauthorized('Invalid auth data')
        if 'success' in data:
            success: dict = data['success']
            return success.get('access_token', False)
        else:
            raise NotImplemented('Server returns no info')

    def get_last_box_data(self, box_id: int):
        json = {'box_id': box_id}
        return self._request.get(f'{self.API_URL}/getLastBoxData', json=json)

    def get_last_box_data(self, box_id: int):
        json = {'box_id': box_id}
        return self._request.get(f'{self.API_URL}/getLastBoxData', json=json)

    def get_box_data_for_period(self, box_id: int, start_date: str, end_date: str):
        json = {'box_id': box_id, "start_date": start_date, "end_date": end_date}
        return self._request.get(f'{self.API_URL}/getBoxDataForPeriod', json=json)

    def get_buildings(self):
        return self._request.get(f'{self.API_URL}/getBuildings')

    def get_rooms(self, building_id: int):
        json = {'building_id': building_id}
        return self._request.get(f'{self.API_URL}/getRooms', json=json)

    def get_boxes(self, room_id: int):
        json = {'room_id': room_id}
        return self._request.get(f'{self.API_URL}/getBoxes', json=json)