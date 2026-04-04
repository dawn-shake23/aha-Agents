"""
长期记忆模块（简化版 RAG 记忆）
用于存储结构化知识、历史对话摘要、业务规则
配合 SummaryMemory 形成完整分层记忆：
短期 → 中期(摘要) → 长期(检索)
"""

from typing import List, Dict
import json


class LongTermMemory:
    def __init__(self):
        # 实际项目可替换为 FAISS / Chroma / 向量库
        self.memory_store: List[Dict] = []

    def add_memory(self, content: str, memory_type: str = "knowledge"):
        """添加长期记忆"""
        self.memory_store.append({
            "content": content,
            "type": memory_type,
            "length": len(content)
        })

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        简化检索：关键词匹配（真实项目可换成 embedding 语义检索）
        """
        candidates = []
        query_words = set(query.lower().split())

        for item in self.memory_store:
            cnt = sum(1 for word in query_words if word in item["content"].lower())
            if cnt > 0:
                candidates.append((-cnt, item["content"]))

        candidates.sort()
        return [item[1] for item in candidates[:top_k]]

    def save_to_file(self, path: str = "long_term_memory.json"):
        """持久化（工程必备）"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.memory_store, f, ensure_ascii=False, indent=2)

    def load_from_file(self, path: str = "long_term_memory.json"):
        """加载记忆"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.memory_store = json.load(f)
        except:
            self.memory_store = []

    def clear(self):
        self.memory_store.clear()


# ------------------------------
# 示例（可直接跑）
# ------------------------------
if __name__ == "__main__":
    ltm = LongTermMemory()

    ltm.add_memory("Agent分为短期、中期、长期三层记忆。")
    ltm.add_memory("摘要记忆用于压缩长对话，降低token消耗。")
    ltm.add_memory("RAG用于从知识库检索相关知识，减少幻觉。")
    ltm.add_memory("DeerFlow是工业级Agent编排框架，强调可控与可追溯。")

    query = "什么是分层记忆？"
    result = ltm.retrieve(query)
    print("检索结果：")
    for r in result:
        print("-", r)

    ltm.save_to_file()