"""
Agent 记忆模块简易实现
包含：短期对话记忆、基础的记忆管理策略
"""

from typing import List, Dict


class ShortTermMemory:
    """
    短期记忆：管理最近 N 轮对话历史
    自动裁剪长度，防止上下文过长
    """

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """添加一轮对话"""
        self.history.append({
            "role": role,
            "content": content
        })
        # 自动裁剪，只保留最近 max_turns 轮
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def get_history(self) -> List[Dict[str, str]]:
        """获取完整历史"""
        return self.history

    def clear(self) -> None:
        """清空记忆"""
        self.history.clear()


class LongTermMemoryDemo:
    """
    长期记忆示例（简化版）
    真实场景可对接向量库（FAISS/Chroma）+ RAG 检索
    """

    def __init__(self):
        # 模拟外部知识库
        self.knowledge_base = {}

    def save_knowledge(self, key: str, value: str) -> None:
        self.knowledge_base[key] = value

    def retrieve(self, query: str) -> str:
        # 简化匹配，真实场景使用 embedding + 相似度检索
        for k, v in self.knowledge_base.items():
            if query in k:
                return v
        return "未找到相关记忆"


if __name__ == "__main__":
    # 简单使用示例
    stm = ShortTermMemory(max_turns=5)
    stm.add_message("user", "什么是Agent记忆？")
    stm.add_message("assistant", "记忆用于维持上下文和历史信息。")
    print(stm.get_history())