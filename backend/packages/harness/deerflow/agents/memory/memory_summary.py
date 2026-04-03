"""
Agent 中期记忆模块 —— Summary Memory
功能：
1. 对多轮对话进行摘要式压缩
2. 控制上下文长度，降低 token 消耗
3. 保留关键信息，提升长对话稳定性
属于分层记忆体系的一部分：短期记忆 → 摘要记忆 → 长期记忆
"""

import asyncio


class SummaryMemory:
    def __init__(self, max_history=10, max_summary_length=512):
        self.raw_history = []
        self.summary = ""
        self.max_history = max_history
        self.max_summary_length = max_summary_length

    def add_user_message(self, content: str):
        self.raw_history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.raw_history.append({"role": "assistant", "content": content})

    def need_summarize(self) -> bool:
        """超过一定轮数，触发摘要压缩"""
        return len(self.raw_history) >= self.max_history

    async def generate_summary(self, llm_call_func) -> None:
        """
        调用 LLM 对历史进行摘要
        :param llm_call_func: 外部传入的异步 LLM 调用函数
        """
        if not self.raw_history:
            return

        prompt = self._build_summary_prompt()
        # 真实场景这里调用模型
        summary_result = await llm_call_func(prompt)
        self.summary = summary_result[:self.max_summary_length]

        # 摘要后保留少量最新对话，避免完全失忆
        self.raw_history = self.raw_history[-3:]

    def get_memory_context(self) -> str:
        """获取最终可放入 prompt 的记忆上下文"""
        context = ""
        if self.summary:
            context += f"历史摘要：{self.summary}\n\n"

        context += "最近对话：\n"
        for item in self.raw_history:
            context += f"{item['role']}: {item['content']}\n"
        return context

    def _build_summary_prompt(self) -> str:
        history_text = "\n".join(
            [f"{item['role']}: {item['content']}" for item in self.raw_history]
        )
        return f"""
请对以下对话进行精简摘要，保留：
- 用户核心需求
- 关键结论
- 决策与约束
不要冗余，不要抒情，控制长度。

对话：
{history_text}

摘要：
""".strip()

    def clear(self):
        self.raw_history.clear()
        self.summary = ""


# ------------------------------
# 模拟使用示例
# ------------------------------
async def mock_llm_call(prompt: str) -> str:
    # 真实场景替换成 Qwen / DeepSeek / Claude
    return "用户询问了Agent记忆架构，助理解释了分层记忆、摘要压缩、长对话优化策略。"


async def demo():
    mem = SummaryMemory(max_history=6)

    # 模拟多轮对话
    for i in range(7):
        mem.add_user_message(f"用户问题{i}")
        mem.add_assistant_message(f"助手回答{i}")

    print("触发摘要前长度:", len(mem.raw_history))

    if mem.need_summarize():
        await mem.generate_summary(mock_llm_call)
        print("摘要完成")

    print("\n最终记忆上下文：")
    print(mem.get_memory_context())


if __name__ == "__main__":
    asyncio.run(demo())