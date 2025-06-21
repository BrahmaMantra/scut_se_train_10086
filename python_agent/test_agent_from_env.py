from agent import DataAnalysisAgent
import os

def test_from_env_file():
    """
    直接从 .env 文件加载配置并运行 Agent 的单次测试。
    """
    # 确认必要的环境变量是否能从环境中（即 .env 文件）加载
    # 这里我们只做打印提示，因为 agent.py 内部会自己加载
    print("--- Agent 单次测试 (从 .env 加载) ---")
    if not os.getenv("OPENAI_BASE_URL") or "your-qwen-api-base-url" in os.getenv("OPENAI_BASE_URL", ""):
        print("提醒: 将从 .env 文件读取 OPENAI_BASE_URL。请确保该文件存在且已正确配置URL。")
        
    agent = DataAnalysisAgent()
    
    query = "帮我查一下 3747835140194172928 区域的用户画像"
    print(f"测试问题: {query}")
    
    try:
        response = agent.run(query)
        print("\n--- Agent 回复 ---")
        print(response)
        print("\n--- 测试结束 ---")
    except Exception as e:
        print(f"\n[测试错误] 运行 Agent 时发生错误: {e}")

if __name__ == "__main__":
    # 在脚本开始时，我们不确定 .env 是否已加载。
    # DataAnalysisAgent 的 __init__ 方法会调用 load_dotenv()，
    # 但为了在测试脚本早期就能给出提示，我们在这里也检查一下。
    # 真正的加载逻辑依赖于 agent.py。
    from dotenv import load_dotenv
    load_dotenv() # 确保 .env 已加载
    test_from_env_file() 