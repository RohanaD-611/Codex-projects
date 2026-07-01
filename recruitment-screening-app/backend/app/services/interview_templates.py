from typing import List, Tuple

from app.schemas import InterviewQuestion, InterviewQuestionResponse


DISPLAY_NAMES = {
    "hr": "HR面试",
    "business": "业务面试",
    "executive": "管理层面试",
}


BASE_QUESTIONS = {
    "hr": [
        ("请介绍一下你目前看机会的主要原因。", "判断求职动机、稳定性和职业规划。"),
        ("你对海外 base 或跨区域协作的期待是什么？", "确认工作地点和协作方式适配度。"),
        ("你过去最适应和最不适应的团队文化分别是什么？", "评估文化适应和团队融合风险。"),
        ("你目前的薪酬结构和期望区间是什么？", "补齐薪酬匹配信息。"),
        ("你接受怎样的出差频率和跨时区沟通节奏？", "确认出海岗位工作强度适配度。"),
        ("你选择下一份工作最看重的三个因素是什么？", "识别决策优先级。"),
        ("你如何描述自己的沟通风格？", "判断沟通方式与团队环境是否匹配。"),
        ("你过去离职或转岗的主要原因是什么？", "评估稳定性和职业轨迹。"),
        ("你是否有工作许可或签证方面需要公司支持？", "确认入职可行性。"),
        ("你希望直属上级如何管理你？", "评估管理方式适配。"),
    ],
    "business": [
        ("请讲一个与你申请岗位最相关的项目或业务成果。", "验证核心经验与 JD 的关系。"),
        ("你在该项目中负责哪些关键决策？", "判断真实职责和影响力。"),
        ("你如何拆解一个新市场或新客户群的进入策略？", "评估业务分析和落地能力。"),
        ("请说明一次目标没有达成时你的复盘过程。", "观察问题解决和复盘能力。"),
        ("你最熟悉的客户类型、渠道或业务模式是什么？", "核对行业和市场经验。"),
        ("你如何衡量自己团队或项目的成功？", "确认指标意识。"),
        ("你遇到过最复杂的跨部门协作问题是什么？", "评估协同能力。"),
        ("如果入职前三个月只能做三件事，你会怎么排优先级？", "评估岗位理解和执行计划。"),
        ("你如何处理总部要求和本地市场现实之间的冲突？", "判断出海管理适配度。"),
        ("请介绍一次你推动变化但遇到阻力的经历。", "评估影响力和韧性。"),
    ],
    "executive": [
        ("你如何判断一个海外市场是否值得长期投入？", "评估战略判断。"),
        ("你如何平衡短期业绩和长期组织建设？", "判断管理成熟度。"),
        ("你过去影响过哪些超出本职范围的业务结果？", "评估组织影响力。"),
        ("你如何建立总部与海外团队之间的信任？", "验证跨文化领导力。"),
        ("如果预算、人才和时间都有限，你会优先解决什么？", "观察资源配置能力。"),
        ("你如何识别并培养当地核心人才？", "评估本地团队建设能力。"),
        ("请讲一次你做过的高风险业务决策。", "评估决策质量和风险意识。"),
        ("你对这个岗位未来 12 个月的最大挑战有什么判断？", "判断业务视角。"),
        ("你如何处理与关键利益相关方的冲突？", "评估高层沟通能力。"),
        ("你希望在这家公司建立怎样的长期影响？", "评估长期动机和格局。"),
    ],
}


def get_interview_questions(candidate_id: str, candidate_name: str, level: str) -> InterviewQuestionResponse:
    items = BASE_QUESTIONS.get(level, BASE_QUESTIONS["hr"])
    questions = [
        InterviewQuestion(
            id=f"{level}_{index:03d}",
            question=question,
            intent=intent,
            evidence="V1 通用模板；V2 接入 AI 后基于候选人简历和匹配结果生成。",
        )
        for index, (question, intent) in enumerate(_expand(items), start=1)
    ]
    return InterviewQuestionResponse(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        level=level,
        display_name=DISPLAY_NAMES.get(level, "HR面试"),
        questions=questions,
    )


def _expand(items: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    prompts = list(items)
    while len(prompts) < 24:
        base_q, base_i = items[len(prompts) % len(items)]
        prompts.append((f"追问：{base_q}", f"深入验证：{base_i}"))
    return prompts
