import os
from agent import DataAnalysisAgent

def test_single_query():
    # We expect environment variables to be set when running this script
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("LLM_MODEL")

    if not all([api_key, base_url, model]):
        print("错误: 缺少必要的环境变量。请设置 OPENAI_API_KEY, OPENAI_BASE_URL, 和 LLM_MODEL。")
        # Remind user about the placeholder URL
        if not base_url or "your-qwen-api-base-url" in base_url:
            print("提醒: 您似乎没有配置有效的 OPENAI_BASE_URL。请将其替换为您的模型服务提供商的实际 URL。")
        return

    print("--- Agent 单次测试 ---")
    agent = DataAnalysisAgent()
    
    # query = "帮我查一下 A-01-01 区域的用户画像"
    # From the database, we know region '3747835140194172928' has data
    query = "帮我查一下 3747835140194172928 区域的用户画像"
    print(f"测试问题: {query}")
    
    try:
        response = agent.run(query)
        print("\n--- Agent 回复 ---")
        print(response)
        print("\n--- 测试结束 ---")
    except Exception as e:
        print(f"\n[测试错误] 运行 Agent 时发生错误: {e}")
        if "Failed to resolve" in str(e) or "Connection refused" in str(e):
             print("错误提示: 无法连接到您提供的 Base URL。请检查该地址是否正确，以及您的网络连接是否通畅。")

if __name__ == "__main__":
    test_single_query() 