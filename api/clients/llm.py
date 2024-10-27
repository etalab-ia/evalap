from typing import Generator

import requests

from api.utils import log_and_raise_for_status, retry

from .schemas.openai import ChatCompletionResponse


class LlmClient:
    def __init__(self, api_key=None, base_url=None):
        self.url = base_url
        self.api_key = api_key

    @staticmethod
    def _get_streaming_response(response: requests.Response) -> Generator[bytes, None, None]:
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk

    @retry(tries=3, delay=2)
    def generate(
        self,
        messages: str | list[dict] | None,
        model: str,
        stream: bool = False,
        path: str = "/chat/completions",
        **sampling_params,
    ) -> ChatCompletionResponse | Generator:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, list):
            # Assume ChatCompletionRequest
            pass
        else:
            raise ValueError("messages type not supported. Messages must be str of list[dict]")

        json_data = sampling_params.copy()
        json_data["messages"] = messages
        json_data["model"] = model
        json_data["stream"] = stream

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = self.url
        response = requests.post(url + path, headers=headers, json=json_data, stream=stream)
        log_and_raise_for_status(response, "Albert API error")

        if stream:
            return self._get_streaming_response(response)

        r = response.json()
        return ChatCompletionResponse(**r)

    @retry(tries=3, delay=2)
    def create_embeddings(
        self,
        texts: str | list[str],
        model: str,
        doc_type: str | None = None,
        path: str = "/embeddings",
        openai_format: bool = False,
    ) -> list[float] | list[list[float]] | dict:
        """Simple interface to create an embedding vector from a text input or a list of texd inputs."""

        json_data = {"input": texts}
        json_data["model"] = model
        if doc_type:
            json_data["doc_type"] = doc_type

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = self.url
        response = requests.post(url + path, headers=headers, json=json_data)
        log_and_raise_for_status(response, "LLM API error")
        results = response.json()
        if openai_format:
            return results

        if isinstance(texts, str):
            results = results["data"][0]["embedding"]
        else:
            results = [x["embedding"] for x in results["data"]]

        return results
