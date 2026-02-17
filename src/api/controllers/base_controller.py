import json

import allure
import httpx

from src.api.logger import get_logger


class BaseController:
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._client = httpx.Client(timeout=30)
        self._jwt_token: str | None = jwt_token
        self._logger = get_logger(self.__class__.__name__)

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _authenticate(self) -> str:
        if self._jwt_token:
            return self._jwt_token

        url = self._url("/api/login")
        with allure.step("Authenticate API client"):
            response = self._client.post(
                url,
                json={"api_token": self.api_token},
            )
            response.raise_for_status()
            self._jwt_token = response.json()["jwt"]
            return self._jwt_token

    def _headers(self, *, content_type: bool = False) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self._authenticate()}"}
        if content_type:
            headers["Content-Type"] = "application/json"
        return headers

    @staticmethod
    def _extract_data(payload: dict | list) -> dict | list:
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    @staticmethod
    def _response_json(response: httpx.Response) -> dict | list:
        if not response.content:
            return {}
        try:
            return response.json()
        except UnicodeDecodeError, json.JSONDecodeError, ValueError:
            text = response.content.decode("utf-8", errors="replace")
            return {"raw": text}

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        url = self._url(endpoint)
        with allure.step(f"GET {endpoint}"):
            self._logger.debug("GET %s params=%s", url, params)
            response = self._client.get(url, headers=self._headers(), params=params)
            self._logger.debug("GET %s -> %s", url, response.status_code)
            response.raise_for_status()
            return self._response_json(response)

    def _post(self, endpoint: str, data: dict | None = None, params: dict | None = None) -> dict:
        url = self._url(endpoint)
        with allure.step(f"POST {endpoint}"):
            self._logger.debug("POST %s params=%s", url, params)
            response = self._client.post(url, headers=self._headers(content_type=True), params=params, json=data)
            self._logger.debug("POST %s -> %s", url, response.status_code)
            response.raise_for_status()
            return self._response_json(response)

    def _put(self, endpoint: str, data: dict | None = None) -> dict:
        url = self._url(endpoint)
        with allure.step(f"PUT {endpoint}"):
            self._logger.debug("PUT %s", url)
            response = self._client.put(url, headers=self._headers(content_type=True), json=data)
            self._logger.debug("PUT %s -> %s", url, response.status_code)
            response.raise_for_status()
            return self._response_json(response)

    def _patch(self, endpoint: str, data: dict | None = None) -> dict:
        url = self._url(endpoint)
        with allure.step(f"PATCH {endpoint}"):
            self._logger.debug("PATCH %s", url)
            response = self._client.patch(url, headers=self._headers(content_type=True), json=data)
            self._logger.debug("PATCH %s -> %s", url, response.status_code)
            response.raise_for_status()
            return self._response_json(response)

    def _delete(self, endpoint: str, params: dict | None = None) -> dict | None:
        url = self._url(endpoint)
        with allure.step(f"DELETE {endpoint}"):
            self._logger.debug("DELETE %s params=%s", url, params)
            response = self._client.delete(url, headers=self._headers(), params=params)
            self._logger.debug("DELETE %s -> %s", url, response.status_code)
            response.raise_for_status()
            if response.content:
                return self._response_json(response)
            return None
