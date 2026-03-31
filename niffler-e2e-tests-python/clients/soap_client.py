"""
SOAP клиент для работы с сервисом Niffler Userdata.

Сервис предоставляет:
- currentUser — получение информации о текущем пользователе
- updateUser  — обновление данных пользователя
- allUsers    — получение списка пользователей
- friends     — получение списка друзей
- sendInvitation    — отправка приглашения дружбы
- acceptInvitation  — принятие приглашения
- declineInvitation — отклонение приглашения
- removeFriend      — удаление из друзей
"""
import requests
import allure
from typing import Optional
from xml.etree import ElementTree as ET


SOAP_NS = "niffler-userdata"
SOAP_ENVELOPE = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="{namespace}">
  <soapenv:Header/>
  <soapenv:Body>
    {body}
  </soapenv:Body>
</soapenv:Envelope>"""


class UserdataSoapClient:
    """SOAP клиент для Niffler Userdata сервиса."""

    def __init__(self, soap_url: str):
        """
        Инициализация SOAP клиента.

        Args:
            soap_url: URL SOAP эндпоинта (например, http://userdata.niffler.dc:8089/ws)
        """
        self.soap_url = soap_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": '""',
        })

    def _send_request(self, body_xml: str) -> ET.Element:
        """
        Отправка SOAP запроса.

        Args:
            body_xml: XML содержимое тела (Body)

        Returns:
            Корневой элемент XML ответа
        """
        envelope = SOAP_ENVELOPE.format(namespace=SOAP_NS, body=body_xml)
        response = self.session.post(self.soap_url, data=envelope.encode("utf-8"))
        response.raise_for_status()
        root = ET.fromstring(response.content)
        return root

    def _extract_body(self, root: ET.Element) -> ET.Element:
        """Извлечение Body из SOAP конверта."""
        ns = {"soapenv": "http://schemas.xmlsoap.org/soap/envelope/"}
        body = root.find("soapenv:Body", ns)
        return body

    def get_current_user(self, username: str) -> dict:
        """
        Получение данных текущего пользователя.

        Args:
            username: имя пользователя

        Returns:
            Словарь с данными пользователя
        """
        body = f"""<tns:currentUserRequest>
            <tns:username>{username}</tns:username>
        </tns:currentUserRequest>"""

        with allure.step(f"SOAP: получение пользователя '{username}'"):
            root = self._send_request(body)
            body_elem = self._extract_body(root)
            return self._parse_user_response(body_elem)

    def update_user(
            self,
            user_id: str,
            username: str,
            firstname: Optional[str] = None,
            surname: Optional[str] = None,
            currency: str = "RUB",
    ) -> dict:
        """
        Обновление данных пользователя.

        Args:
            user_id: UUID пользователя
            username: имя пользователя
            firstname: имя
            surname: фамилия
            currency: валюта (RUB, USD, EUR, KZT)

        Returns:
            Словарь с обновлёнными данными пользователя
        """
        firstname_xml = f"<tns:firstname>{firstname}</tns:firstname>" if firstname else ""
        surname_xml = f"<tns:surname>{surname}</tns:surname>" if surname else ""

        body = f"""<tns:updateUserRequest>
            <tns:user>
                <tns:id>{user_id}</tns:id>
                <tns:username>{username}</tns:username>
                {firstname_xml}
                {surname_xml}
                <tns:currency>{currency}</tns:currency>
            </tns:user>
        </tns:updateUserRequest>"""

        with allure.step(f"SOAP: обновление пользователя '{username}'"):
            root = self._send_request(body)
            body_elem = self._extract_body(root)
            return self._parse_user_response(body_elem)

    def get_all_users(self, username: str, search_query: Optional[str] = None) -> list:
        """
        Получение списка всех пользователей.

        Args:
            username: текущий пользователь
            search_query: поиск по имени (опционально)

        Returns:
            Список словарей с данными пользователей
        """
        search_xml = f"<tns:searchQuery>{search_query}</tns:searchQuery>" if search_query else ""
        body = f"""<tns:allUsersRequest>
            <tns:username>{username}</tns:username>
            {search_xml}
        </tns:allUsersRequest>"""

        with allure.step(f"SOAP: получение всех пользователей для '{username}'"):
            root = self._send_request(body)
            body_elem = self._extract_body(root)
            return self._parse_users_response(body_elem)

    def send_invitation(self, username: str, friend_username: str) -> None:
        """Отправка приглашения дружбы."""
        body = f"""<tns:sendInvitationRequest>
            <tns:username>{username}</tns:username>
            <tns:friendToBeRequested>{friend_username}</tns:friendToBeRequested>
        </tns:sendInvitationRequest>"""

        with allure.step(f"SOAP: отправка приглашения от '{username}' к '{friend_username}'"):
            self._send_request(body)

    def accept_invitation(self, username: str, friend_username: str) -> None:
        """Принятие приглашения дружбы."""
        body = f"""<tns:acceptInvitationRequest>
            <tns:username>{username}</tns:username>
            <tns:friendToBeAdded>{friend_username}</tns:friendToBeAdded>
        </tns:acceptInvitationRequest>"""

        with allure.step(f"SOAP: принятие приглашения '{username}' от '{friend_username}'"):
            self._send_request(body)

    def decline_invitation(self, username: str, friend_username: str) -> None:
        """Отклонение приглашения дружбы."""
        body = f"""<tns:declineInvitationRequest>
            <tns:username>{username}</tns:username>
            <tns:invitationToBeDeclined>{friend_username}</tns:invitationToBeDeclined>
        </tns:declineInvitationRequest>"""

        with allure.step(f"SOAP: отклонение приглашения '{username}' от '{friend_username}'"):
            self._send_request(body)

    def remove_friend(self, username: str, friend_username: str) -> None:
        """Удаление из друзей."""
        body = f"""<tns:removeFriendRequest>
            <tns:username>{username}</tns:username>
            <tns:friendToBeRemoved>{friend_username}</tns:friendToBeRemoved>
        </tns:removeFriendRequest>"""

        with allure.step(f"SOAP: удаление из друзей '{username}' и '{friend_username}'"):
            self._send_request(body)

    def _parse_user_response(self, body: ET.Element) -> dict:
        """Разбор ответа с одним пользователем."""
        tns = SOAP_NS
        user_elem = body.find(f".//{{{tns}}}user")
        if user_elem is None:
            return {}
        return self._user_elem_to_dict(user_elem)

    def _parse_users_response(self, body: ET.Element) -> list:
        """Разбор ответа со списком пользователей."""
        tns = SOAP_NS
        users = []
        for user_elem in body.findall(f".//{{{tns}}}user"):
            users.append(self._user_elem_to_dict(user_elem))
        return users

    @staticmethod
    def _user_elem_to_dict(user_elem: ET.Element) -> dict:
        """Конвертация XML элемента пользователя в словарь."""
        tns = SOAP_NS
        result = {}
        fields = ["id", "username", "firstname", "surname", "fullname", "currency",
                  "photo", "photoSmall", "friendshipStatus"]
        for field in fields:
            elem = user_elem.find(f"{{{tns}}}{field}")
            if elem is not None and elem.text:
                result[field] = elem.text
        return result

    def close(self) -> None:
        """Закрытие сессии."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

