import os
import re
from dataclasses import dataclass, field
from typing import Generator, Optional, Tuple

import requests

# @TODO: Will be obsolete when MFS will use albert-api to do RAG
from evalap.api.config import MFS_API_KEY_V2
from evalap.logger import logger
from evalap.utils import log_and_raise_for_status, retry

from .schemas.openai_rag import Chunk, RagChatCompletionResponse, Search


@dataclass
class LlmApiUrl:
    albert_prod: str = "https://albert.api.etalab.gouv.fr/v1"
    albert_staging: str = "https://albert.api.staging.etalab.gouv.fr/v1"
    mistral: str = "https://api.mistral.ai/v1"
    openai: str = "https://api.openai.com/v1"
    anthropic: str = "https://api.anthropic.com/v1"
    header_keys: dict = field(
        default_factory=lambda: {
            "albert_prod": {"Authorization": "Bearer {ALBERT_API_KEY}"},
            "albert_staging": {"Authorization": "Bearer {ALBERT_API_KEY_STAGING}"},
            "mistral": {"Authorization": "Bearer {MISTRAL_API_KEY}"},
            "openai": {
                "Authorization": "Bearer {OPENAI_API_KEY}",
                #    "OpenAI-Organization": "{OPENAI_ORG_KEY}",
            },
            "anthropic": {
                "x-api-key": "{ANTHROPIC_API_KEY}",
                "anthropic-version": "2023-06-01",
            },
        }
    )

    def build_header(self, provider: str, h_pattern: str = r"\{(.*?)\}"):
        headers = {}
        for h, t in LlmApiUrl.header_keys[provider].items():
            # Format the headers from the environ
            match = re.search(h_pattern, t)
            if not match or not os.getenv(match.group(1)):
                headers[h] = t
            else:
                headers[h] = t.format(**{match.group(1): os.getenv(match.group(1))})
        return headers


LlmApiUrl = LlmApiUrl()  # headers_keys does not exist otherwise...


@dataclass
class LlmApiModels:
    albert_prod: set[str] = field(default_factory=set)
    albert_staging: set[str] = field(default_factory=set)
    mistral: set[str] = field(default_factory=set)
    openai: set[str] = field(default_factory=set)
    anthropic: set[str] = field(default_factory=set)

    @classmethod
    def _sync_openai_api_models(cls):
        self = cls()

        for provider, _ in self.__dict__.items():
            if provider.startswith("_"):
                continue

            url = getattr(LlmApiUrl, provider)
            headers = LlmApiUrl.build_header(provider)
            try:
                response = requests.get(f"{url}/models", headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Model discovery error: {e}")
                continue
            models_data = response.json()
            models = {model["id"] for model in models_data["data"]}
            models |= {alias for model in models_data["data"] for alias in (model.get("aliases") or [])}
            setattr(self, provider, models)

        return self

    def _all_models(self) -> set:
        provider_models = [
            models for provider, models in self.__dict__.items() if not provider.startswith("_")
        ]
        return {model for models in provider_models for model in models}


LlmApiModels = LlmApiModels._sync_openai_api_models()


def get_api_url(model: str) -> (str | None, dict):
    for provider, models in LlmApiModels.__dict__.items():
        if provider.startswith("__"):
            continue
        if model in models:
            headers = LlmApiUrl.build_header(provider)
            return getattr(LlmApiUrl, provider), headers
    return None, {}


class LlmClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    @staticmethod
    def _get_streaming_response(response: requests.Response) -> Generator[bytes, None, None]:
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk

    def get_url_and_headers(self, model: str) -> tuple[str, dict]:
        url = self.base_url
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        else:
            _url, h = get_api_url(model)
            url = _url or url
            headers.update(h)

        return url, headers

    @retry(tries=3, delay=5)
    def generate(
        self,
        messages: str | list[dict] | None,
        model: str,
        stream: bool = False,
        path: str = "/chat/completions",
        **sampling_params,
    ) -> RagChatCompletionResponse | Generator:
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

        url, headers = self.get_url_and_headers(model)
        if not url:
            raise ValueError(f"Model unknown: {model}")
        response = requests.post(url + path, headers=headers, json=json_data, stream=stream, timeout=300)
        log_and_raise_for_status(response, "Albert API error")

        if stream:
            return self._get_streaming_response(response)

        r = response.json()
        # @TODO catch base URL to switch-case the context decoding
        chat = RagChatCompletionResponse(**r)
        # MFS decoding
        # @deprecated
        if hasattr(chat, "rag_context"):
            refs = sum([x.references for x in chat.rag_context or []], [])
            chunks = []
            url, headers = self.get_url_and_headers(model)
            headers = {"Authorization": f"Bearer {MFS_API_KEY_V2}"}

            # From pyalbert
            def doc_to_chunk(doc: dict) -> str:
                context = ""
                if "context" in doc:
                    context = "  ( > ".join(doc["context"]) + ")"

                text = "\n".join([doc["title"] + context, doc["introduction"], doc["text"]])
                return text

            for chunkid in refs:
                response = requests.get(url.removesuffix("/v1") + f"/v2/get_chunk/{chunkid}", headers=headers)
                log_and_raise_for_status(response, "MFS fetch chunk")
                chunk = response.json()
                chunks.append(doc_to_chunk(chunk))

            chat.search_results = [Search(chunk=Chunk(content=chunk), score=1) for chunk in chunks]

        return chat

    @retry(tries=3, delay=5)
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

        url, headers = self.get_url_and_headers(model)
        response = requests.post(url + path, headers=headers, json=json_data, timeout=300)
        log_and_raise_for_status(response, "LLM API error")
        results = response.json()
        if openai_format:
            return results

        if isinstance(texts, str):
            results = results["data"][0]["embedding"]
        else:
            results = [x["embedding"] for x in results["data"]]

        return results


#
# Utils
#


def split_think_answer(answer: str, think_token="</think>") -> Tuple[Optional[str], str]:
    """Separate the reasoning token from the regular answer if any"""
    pattern = re.escape(think_token)
    match = re.search(pattern, answer, re.IGNORECASE)
    if match:
        start, end = match.span()
        think = answer[:end].strip()
        answer = answer[end:].strip()
        return think, answer
    else:
        # behave like original logic
        return None, answer.strip()
