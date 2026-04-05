"""
Payment domain built-in subagents for DeerFlow 2.0
支付领域内置子智能体（订单 / 支付 / 退款 / 营销）
适用于金融支付、电商交易、清结算业务场景
"""

from deerflow.subagents.config import SubagentConfig

# ------------------------------------------------------------------------------
# 1. 订单子 Agent：查询、状态、幂等、流水核对
# ------------------------------------------------------------------------------
payment_order_agent = SubagentConfig(
    name="payment_order_agent",
    description=(
        "负责支付订单相关业务：订单创建、订单查询、状态流转、流水核对、幂等判断。"
        "当用户涉及订单信息、交易状态、流水记录、订单重试时，必须委托此子Agent。"
    ),
    system_prompt=(
        "你是支付领域的订单处理专家，严格遵循支付系统规范。\n"
        "1. 必须校验订单号、用户ID、商户ID合法性。\n"
        "2. 必须判断订单状态：待支付、支付中、成功、失败、关闭、退款中。\n"
        "3. 必须强调幂等性，禁止重复提交。\n"
        "4. 只输出结构化结果，不编造数据。\n"
        "5. 异常单、状态不一致单必须提示人工介入。\n"
    ),
    tools=[
        "query_order_info",
        "query_order_status",
        "query_order_flow",
        "check_idempotent",
    ],
    disallowed_tools=["bash", "code", "file_write", "task"],
    model="inherit",
    max_turns=15,
    timeout_seconds=120,
)

# ------------------------------------------------------------------------------
# 2. 支付子 Agent：支付路由、渠道选择、签名、结果通知
# ------------------------------------------------------------------------------
payment_pay_agent = SubagentConfig(
    name="payment_pay_agent",
    description=(
        "负责支付核心链路：创建支付单、选择支付渠道（微信/支付宝/网银）、签名校验、"
        "结果回调处理、掉单补发、支付状态同步。"
        "当用户发起支付、查询支付结果、处理掉单时，必须委托此子Agent。"
    ),
    system_prompt=(
        "你是支付核心执行专家，严格遵循资金安全规范。\n"
        "1. 必须校验金额、币种、商户、用户、订单关系。\n"
        "2. 必须根据金额、商户、用户地域智能选择最优支付渠道。\n"
        "3. 必须验证签名、验签、防篡改、防重放。\n"
        "4. 掉单必须自动重试，超过阈值则触发预警。\n"
        "5. 严禁泄露密钥、签名、渠道敏感信息。\n"
    ),
    tools=[
        "create_pay_order",
        "choose_pay_channel",
        "verify_sign",
        "query_pay_result",
        "retry_notify",
    ],
    disallowed_tools=["bash", "code", "file_write", "task"],
    model="inherit",
    max_turns=20,
    timeout_seconds=150,
)

# ------------------------------------------------------------------------------
# 3. 退款子 Agent：退款规则、风控拦截、金额拆分、原路退回
# ------------------------------------------------------------------------------
payment_refund_agent = SubagentConfig(
    name="payment_refund_agent",
    description=(
        "负责退款全流程：退款申请、金额拆分、原路退回、风控拦截、退款状态同步、"
        "退款失败重试、手续费退还。"
        "当用户申请退款、查询退款进度、处理退款失败时，必须委托此子Agent。"
    ),
    system_prompt=(
        "你是退款处理专家，严格遵守资金与合规规则。\n"
        "1. 必须校验原支付单是否可退（状态、有效期、是否已退）。\n"
        "2. 必须校验退款金额 ≤ 支付金额，支持部分退款。\n"
        "3. 高风险订单必须触发风控拦截。\n"
        "4. 原路退回：微信→微信，支付宝→支付宝，卡→卡。\n"
        "5. 退款失败必须自动重试并记录原因。\n"
    ),
    tools=[
        "check_refund_allowed",
        "split_refund_amount",
        "create_refund_order",
        "query_refund_status",
        "risk_check_refund",
    ],
    disallowed_tools=["bash", "code", "file_write", "task"],
    model="inherit",
    max_turns=20,
    timeout_seconds=180,
)

# ------------------------------------------------------------------------------
# 4. 营销子 Agent：优惠、券、满减、折扣、抵扣计算
# ------------------------------------------------------------------------------
payment_marketing_agent = SubagentConfig(
    name="payment_marketing_agent",
    description=(
        "负责支付环节的营销优惠计算：优惠券、满减、折扣、会员权益、运费抵扣、"
        "商品券、跨店优惠，计算最终实付金额。"
        "当用户下单、支付前需要计算优惠时，必须委托此子Agent。"
    ),
    system_prompt=(
        "你是支付营销计算专家，保证计算准确、规则一致。\n"
        "1. 必须读取用户可用券、可用权益。\n"
        "2. 按优先级计算：商品券 > 店铺券 > 平台券 > 满减。\n"
        "3. 不可叠加的优惠必须自动互斥。\n"
        "4. 最终实付金额 = 原价 - 优惠 - 抵扣。\n"
        "5. 计算过程必须可解释、可回溯。\n"
    ),
    tools=[
        "list_user_coupons",
        "calculate_discount",
        "check_coupon_valid",
        "compute_final_pay_amount",
    ],
    disallowed_tools=["bash", "code", "file_write", "task"],
    model="inherit",
    max_turns=15,
    timeout_seconds=90,
)

# ------------------------------------------------------------------------------
# 统一导出（和 DeerFlow 内置格式完全一致）
# ------------------------------------------------------------------------------
PAYMENT_SUBAGENTS = {
    "payment_order_agent": payment_order_agent,
    "payment_pay_agent": payment_pay_agent,
    "payment_refund_agent": payment_refund_agent,
    "payment_marketing_agent": payment_marketing_agent,
}