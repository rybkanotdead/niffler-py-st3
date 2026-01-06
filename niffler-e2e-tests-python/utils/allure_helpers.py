import json
import logging
import allure
import curlify
from requests import Response
from json import JSONDecodeError
from allure_commons.types import AttachmentType


def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа
    в allure шаг и аллюр аттачмент и в консоль."""

    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]
        with allure.step(f"{method} {url}"):

            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            logging.debug(curl)
            logging.debug(response.text)

            allure.attach(
                body=curl.encode("utf8"),
                name=f"Request {response.status_code}",
                attachment_type=AttachmentType.TEXT,
                extension=".txt"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )
            except JSONDecodeError:
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt")
            headers_dict = dict(response.headers)
            allure.attach(
                body=json.dumps(headers_dict, indent=4).encode("utf8"),
                name=f"Response headers {response.status_code}",
                attachment_type=AttachmentType.JSON,
                extension=".json"
            )
        return response

    return wrapper


def attach_sql(cursor, statement, parameters, context):
    """Прикрепляет SQL запрос в аллюре"""

    statement_with_params = statement % parameters
    name = statement.split(" ")[0] + " " + context.engine.url.database
    allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)