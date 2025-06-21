from agent import DataAnalysisAgent

def main():
    """
    启动与数据分析助手的命令行交互会话。
    """
    # 初始化 Agent (它会自动从 .env 读取配置)
    agent = DataAnalysisAgent()
    
    # 打印欢迎信息
    print("--- 数据分析助手 ---")
    print("您好！我是您的数据分析助手，请问有什么可以帮您？")
    print("例如: '查一下区域 3747835140194172928 的人群构成' 或 '昨天天河区栅格32有多少女性用户？'")
    print("输入 'exit' 或 'quit' 即可退出程序。")
    print("-" * 20)
    
    # 进入主循环，接收用户输入
    while True:
        try:
            # 从用户处获取输入
            query = input("您 > ")
            
            # 检查退出条件
            if query.lower() in ["exit", "quit"]:
                print("感谢使用，再见！")
                break
                
            # 如果输入为空，则继续下一次循环
            if not query:
                continue
                
            # 调用 Agent 处理查询并获取响应
            response = agent.run(query)
            
            # 打印助手的回答
            print(f"助手 > {response}")
            
        except KeyboardInterrupt:
            # 允许用户通过 Ctrl+C 优雅地退出
            print("\n感谢使用，再见！")
            break
        except Exception as e:
            # 捕获意外错误并打印
            print(f"\n[错误] 发生了一个意料之外的错误: {e}")
            print("请重试。如果问题持续存在，请检查您的配置或网络连接。")

if __name__ == "__main__":
    main() 