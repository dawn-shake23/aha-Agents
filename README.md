AHA (Agent High-Availability) 是一个轻量级、高稳定的 Agent 执行框架。提供状态持久化、崩溃恢复、重试熔断、上下文隔离与可扩展技能调用，让 LLM Agent 在复杂任务中保持稳定、可靠、可观测。

AHA-Agent 是一个轻量级 Super Agent Harness，通过调度子任务、维护状态记忆、提供沙箱执行与可扩展技能，实现复杂任务自动化。采用主从 Agent 思想，将复杂任务拆分为多步独立子任务，每步独立上下文、独立工具调用，避免互相干扰。

核心结构：
Sub-Agents（主 Agent + 子任务 Agent）
Memory（记忆）
Sandbox（沙箱执行环境）
Skills（可扩展技能）

核心特性：
Skills 与 Tools、Sub-Agents、Sandbox、Context Engineering、长期记忆

