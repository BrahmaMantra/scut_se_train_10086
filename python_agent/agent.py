import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import api_tools
from inspect import getmembers, isfunction, getdoc

# 加载环境变量 (会自动寻找 .env 文件并加载)
load_dotenv()

class DataAnalysisAgent:
    def __init__(self):
        """
        初始化 Agent。
        它会自动从 .env 文件加载 API Key、模型名称和 Base URL。
        """
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.model = os.getenv("LLM_MODEL", "gpt-4o") # 默认为 gpt-4o
        self.tools = self._get_api_tools()
        self.available_functions = self._get_available_functions()

    def _get_api_tools(self):
        """
        将 api_tools.py 中的函数转换为 OpenAI Tools 格式。
        这部分代码会自动读取函数的名称、文档字符串和参数，
        让 LLM 能够理解每个工具的作用。
        """
        tools = []
        for name, func in getmembers(api_tools, isfunction):
            if name.startswith("get_"): # 只注册我们定义的工具函数
                tool_doc = getdoc(func)
                tools.append({
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool_doc,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                # 这里为了简化，我们让 LLM 根据函数签名和文档自行推断参数。
                                # 对于更复杂的场景，可以详细定义每个参数的类型和描述。
                            },
                            "required": [] # 同上，让LLM自行决定
                        },
                    },
                })
        return tools

    def _get_available_functions(self):
        """获取可供调用的函数实例的字典。"""
        return {name: func for name, func in getmembers(api_tools, isfunction)}

    def run(self, user_query: str):
        """
        运行 Agent 的主流程。
        """
        print(f"\n[Agent] 收到问题: {user_query}")
        
        # 初始消息包含用户的提问
        messages = [{"role": "user", "content": user_query}]
        
        # 第一次调用 LLM，让它判断是否需要使用工具
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
        )
        
        response_message = response.choices[0].message
        messages.append(response_message) # 将 LLM 的回复加入到对话历史

        # 检查 LLM 是否决定调用工具
        tool_calls = response_message.tool_calls
        if tool_calls:
            print(f"[Agent] LLM 决定调用工具: {[(tc.function.name, tc.function.arguments) for tc in tool_calls]}")
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions[function_name]
                
                try:
                    # 解析 LLM 生成的参数
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    error_message = f"错误: LLM生成了无效的参数JSON: {tool_call.function.arguments}"
                    print(f"[Agent] {error_message}")
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": error_message,
                    })
                    continue # 处理下一个工具调用
                
                # 调用实际的函数
                function_response = function_to_call(**function_args)
                
                # 将工具的返回结果告知 LLM
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    }
                )
            
            # 再次调用 LLM，让它根据工具的返回结果，生成最终的自然语言答案
            print("[Agent] 将工具结果返回给 LLM 进行总结...")
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return final_response.choices[0].message.content
        else:
            # 如果 LLM 认为不需要调用工具，直接返回它的回答
            print("[Agent] LLM 无需工具即可直接回答。")
            return response_message.content 