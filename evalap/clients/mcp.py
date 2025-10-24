import json
from collections import defaultdict

import requests

from evalap.api.config import MCP_BRIDGE_URL
from evalap.clients.schemas.openai import ChatCompletionResponse
from evalap.logger import logger
from evalap.utils import log_and_raise_for_status

from .llm import LlmClient


class MCPBridgeClient:
    def __init__(self):
        self.url = MCP_BRIDGE_URL
        self.refresh()

    def fetch_tools(self) -> dict:
        url = self.url
        path = "/mcp/tools"
        headers = {}
        response = requests.get(
            url + path,
            headers=headers,
            timeout=10,
        )
        log_and_raise_for_status(response, "MCP bridge client error")
        tools = response.json()
        return tools

    def get_tool(self, tool_name: str) -> list:
        for tool_set_name, tools in self.tools.items():
            if tool_set_name == tool_name:
                return tools["tools"]

            for tool in tools["tools"]:
                if tool_name == tool["name"]:
                    return [tool]

        raise ValueError("MCP tool not found")

    def call_tool(self, tool_name: str, params: str):
        url = self.url
        path = f"/mcp/tools/{tool_name}/call"
        headers = {}

        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            logger.error(f"failed to decode json for {tool_name}")
            return None

        response = requests.post(url + path, headers=headers, json=params)
        log_and_raise_for_status(response, "MCP bridge tools call error")
        response = response.json()
        return response

    def tools2openai(self, tool_names: list[str]):
        tools = []
        for tool_name in tool_names:
            mcp_tools = self.get_tool(tool_name)
            for mcp_tool in mcp_tools:
                tool = {
                    "type": "function",
                    "function": {
                        "name": mcp_tool["name"],
                        "description": mcp_tool["description"],
                        "parameters": mcp_tool["inputSchema"],
                        # "strict": False,
                    },
                }
                tools.append(tool)
        return tools

    def refresh(self):
        self.tools: dict = self.fetch_tools()


def multi_step_generate(
    model_base_url: str,
    model_api_key: str,
    model_name: str,
    messages: list,
    sampling_params: dict,
    mcp_bridge: MCPBridgeClient | None = None,
    max_steps=10,
    max_steps_search=2,
) -> (ChatCompletionResponse, list[list[dict]]):
    cpt = 0
    steps: list[list[dict]] = []  # list of tools calls
    tools_count = defaultdict(int)
    aiclient = LlmClient(base_url=model_base_url, api_key=model_api_key)
    if "tools" in sampling_params and "tool_choice" not in sampling_params:
        sampling_params = sampling_params | {"tool_choice": "auto"}

    while cpt < max_steps:
        cpt += 1
        result = aiclient.generate(model=model_name, messages=messages, **sampling_params)
        completion = result.choices[0]
        # Add the completion result to messages
        messages.append(completion.message.model_dump())

        # Check if finished
        if completion.finish_reason in [None, "", "stop", "length"] or mcp_bridge is None:
            break

        # MCP/toolings loop
        # --
        if completion.finish_reason not in ["tool_calls"]:
            logger.warning("Unknown LLM finish reason: %s" % completion.finish_reason)
        # If tool_calls, loop over the tool and execute @FUTURE async.gather for concurent execution
        substeps = []
        for tool_call in completion.message.tool_calls or []:
            # Run tool
            tool_call_result = mcp_bridge.call_tool(tool_call.function.name, tool_call.function.arguments)
            # Format result
            if tool_call_result is None:
                tool_content = []
            else:
                tool_content = [{"type": "text", "text": part["text"]} for part in filter(lambda x: x["type"] == "text", tool_call_result["content"])]

            if len(tool_content) == 0:
                tool_content = [{"type": "text", "text": "the tool call result is empty"}]
            elif len(tool_content) > 1:
                logger.warning("Tool call content size is greater than 1 for {tool_call.function.name}")
            tool_content = "\n\n".join([x["text"] for x in tool_content])
            messages.append(
                {
                    "role": "tool",
                    "content": tool_content,
                    "tool_call_id": tool_call.id,
                }
            )

            # Accumute tool call result to save it in answers result.
            substeps.append(
                {
                    "tool_name": tool_call.function.name,
                    "tool_params": tool_call.function.arguments,
                    "tool_result": tool_content,
                }
            )

            tools_count[tool_call.function.name] += 1
            # Avoid deep search recursion
            if tool_call.function.name.startswith("search") and tools_count[tool_call.function.name] >= max_steps_search:
                cpt = max_steps

        steps.append(substeps)

    # if max_steps has been reached
    if messages[-1]["role"] == "tool":
        logger.warning(f"Multi-step agents max steps has been reached for model {model_name}.")
        sampling_params["tool_choice"] = "none"
        result = aiclient.generate(model=model_name, messages=messages, **sampling_params)

    return result, steps
