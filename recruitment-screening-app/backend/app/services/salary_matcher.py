from app.schemas import SalaryBudget, SalaryExpectation, SalaryMatchResult


def match_salary(
    job_budget: SalaryBudget,
    expectation: SalaryExpectation,
) -> SalaryMatchResult:
    if job_budget.min is None or job_budget.max is None:
        return SalaryMatchResult(status="无法判断", score=70, reason="岗位未提供完整薪酬预算。")

    if expectation.amount_min is None and expectation.amount_max is None:
        return SalaryMatchResult(status="待确认", score=75, reason="简历中未识别到候选人期望薪资。")

    if expectation.currency and expectation.currency.upper() != job_budget.currency.upper():
        return SalaryMatchResult(status="需人工确认", score=65, reason="候选人薪酬币种与岗位预算币种不一致。")

    if expectation.period and expectation.period != job_budget.period:
        return SalaryMatchResult(status="需人工确认", score=65, reason="候选人薪酬周期与岗位预算周期不一致。")

    expected_low = expectation.amount_min or expectation.amount_max or 0
    expected_high = expectation.amount_max or expectation.amount_min or 0
    budget_min = job_budget.min
    budget_max = job_budget.max

    if expected_low >= budget_min and expected_high <= budget_max:
        return SalaryMatchResult(status="匹配", score=95, reason="候选人期望薪资在岗位预算范围内。")

    if expected_low <= budget_max and expected_high <= budget_max * 1.1:
        return SalaryMatchResult(status="基本匹配", score=82, reason="候选人薪资上限略高或部分落在预算范围内。")

    if expected_low <= budget_max * 1.3:
        return SalaryMatchResult(status="偏高", score=60, reason="候选人期望薪资高于岗位预算 10%-30%。")

    return SalaryMatchResult(status="明显偏高", score=35, reason="候选人期望薪资高于岗位预算 30% 以上。")
