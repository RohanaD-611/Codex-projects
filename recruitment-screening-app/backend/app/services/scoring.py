from typing import Dict, List

from app.schemas import (
    CandidateAnalysisResult,
    CandidateParsedData,
    CandidateScoreBreakdown,
    MatchSection,
    SalaryBudget,
)
from app.services.jd_parser import contains_term
from app.services.salary_matcher import match_salary


def score_candidate(
    analysis_id: str,
    job_title: str,
    job_description: str,
    target_market: str,
    hard_requirements: List[str],
    must_have_skills: List[str],
    nice_to_have_skills: List[str],
    salary_budget: SalaryBudget,
    candidate: CandidateParsedData,
) -> CandidateAnalysisResult:
    resume_text = candidate.resume_text.lower()
    matched_hard = [term for term in hard_requirements if contains_term(resume_text, term)]
    missing_hard = [term for term in hard_requirements if term not in matched_hard]
    matched_must = [term for term in must_have_skills if contains_term(resume_text, term)]
    missing_must = [term for term in must_have_skills if term not in matched_must]
    matched_nice = [term for term in nice_to_have_skills if contains_term(resume_text, term)]

    hard_score = _rate(matched_hard, hard_requirements, 80)
    skills_score = round((_rate(matched_must, must_have_skills, 70) * 0.75) + (_rate(matched_nice, nice_to_have_skills, 50) * 0.25), 2)
    experience_score = _experience_score(candidate.years_experience, job_description)
    market_score = _market_score(target_market, candidate.markets, resume_text)
    language_score = _language_score(candidate.languages, job_description)
    salary = match_salary(salary_budget, candidate.salary_expectation)
    risk_score = _risk_score(missing_hard, missing_must, salary.score, candidate.resume_text)

    scores = CandidateScoreBreakdown(
        hard_requirements=hard_score,
        skills_match=skills_score,
        experience_relevance=experience_score,
        overseas_market_fit=market_score,
        language_communication=language_score,
        salary_match=salary.score,
        risk=risk_score,
    )
    total = round(
        scores.hard_requirements * 0.15
        + scores.skills_match * 0.20
        + scores.experience_relevance * 0.20
        + scores.overseas_market_fit * 0.15
        + scores.language_communication * 0.10
        + scores.salary_match * 0.10
        + scores.risk * 0.10,
        2,
    )
    recommendation = _recommendation(total, hard_score, salary.score)
    strengths, gaps, risks = _insights(candidate, matched_must, missing_must, matched_hard, missing_hard, salary.status)

    return CandidateAnalysisResult(
        candidate_id=candidate.candidate_id,
        analysis_id=analysis_id,
        name=candidate.name,
        resume_file_name=candidate.resume_file_name,
        resume_url=candidate.resume_url,
        detail_url=f"/candidates/{candidate.candidate_id}",
        total_score=total,
        recommendation=recommendation,
        summary=_summary(candidate, target_market, total),
        scores=scores,
        salary_match=salary,
        strengths=strengths,
        gaps=gaps,
        risks=risks,
        profile={
            "current_location": candidate.current_location,
            "years_experience": candidate.years_experience,
            "languages": candidate.languages,
            "skills": candidate.skills,
            "markets": candidate.markets,
        },
        match_analysis={
            "hard_requirements": MatchSection(score=hard_score, matched=matched_hard, missing=missing_hard),
            "must_have": MatchSection(score=_rate(matched_must, must_have_skills, 70), matched=matched_must, missing=missing_must),
            "nice_to_have": MatchSection(score=_rate(matched_nice, nice_to_have_skills, 50), matched=matched_nice, missing=[]),
            "salary": MatchSection(score=salary.score, matched=[salary.status], missing=[], note=salary.reason),
        },
        evidence_snippets=_snippets(candidate.resume_text, matched_must + matched_hard),
    )


def rank_candidates(results: List[CandidateAnalysisResult], top_n: int) -> List[CandidateAnalysisResult]:
    ranked = sorted(results, key=lambda item: item.total_score, reverse=True)
    limited = ranked[: max(top_n, 1)]
    for index, item in enumerate(limited, start=1):
        item.rank = index
    return limited


def _rate(found: List[str], total: List[str], empty_default: float) -> float:
    if not total:
        return float(empty_default)
    return round((len(found) / len(total)) * 100, 2)


def _experience_score(years: float, jd: str) -> float:
    if years >= 8:
        return 95
    if years >= 5:
        return 85
    if years >= 3:
        return 72
    if years >= 1:
        return 55
    return 40 if "junior" in jd.lower() else 30


def _market_score(target_market: str, markets: List[str], resume_text: str) -> float:
    if target_market and target_market.lower() in resume_text:
        return 95
    if markets:
        return 82
    return 55


def _language_score(languages: List[str], jd: str) -> float:
    jd_lower = jd.lower()
    if "english" in jd_lower and "english" not in languages:
        return 45
    if "english" in languages and ("mandarin" in languages or "chinese" in languages):
        return 90
    if languages:
        return 75
    return 60


def _risk_score(missing_hard: List[str], missing_must: List[str], salary_score: float, text: str) -> float:
    score = 90 - (len(missing_hard) * 12) - (len(missing_must) * 8)
    if salary_score < 60:
        score -= 12
    if len(text) < 500:
        score -= 10
    return max(20, min(100, round(score, 2)))


def _recommendation(total: float, hard_score: float, salary_score: float) -> str:
    if hard_score < 50 or salary_score < 40:
        return "谨慎考虑"
    if total >= 90:
        return "强推荐进入面试"
    if total >= 80:
        return "推荐进入面试"
    if total >= 70:
        return "备选"
    if total >= 60:
        return "谨慎考虑"
    return "暂不推荐"


def _insights(candidate: CandidateParsedData, matched_must: List[str], missing_must: List[str], matched_hard: List[str], missing_hard: List[str], salary_status: str):
    strengths = []
    gaps = []
    risks = []
    if matched_must:
        strengths.append(f"匹配 {len(matched_must)} 项 must-have 能力")
    if matched_hard:
        strengths.append(f"满足 {len(matched_hard)} 项硬性条件")
    if candidate.markets:
        strengths.append("简历呈现海外或目标市场相关经历")
    if missing_must:
        gaps.append("未明确体现：" + "、".join(missing_must[:3]))
    if missing_hard:
        risks.append("硬性条件待确认：" + "、".join(missing_hard[:3]))
    if salary_status in {"待确认", "需人工确认", "偏高", "明显偏高"}:
        risks.append(f"薪酬状态：{salary_status}")
    return strengths or ["简历具备可进一步核对的岗位相关信息"], gaps or ["暂无明显缺口，建议结合原简历复核"], risks or ["暂无明显风险，建议面试中验证关键经历"]


def _summary(candidate: CandidateParsedData, target_market: str, total: float) -> str:
    years = f"{candidate.years_experience:g}年" if candidate.years_experience else "未明确年限的"
    market = target_market or (candidate.markets[0] if candidate.markets else "目标市场")
    skills = "、".join(candidate.skills[:3]) if candidate.skills else "岗位相关能力"
    return f"候选人呈现{years}相关经验，简历中可见{skills}等信息，与{market}岗位要求的综合匹配分为{total:g}，建议结合详细分析和原简历继续复核。"


def _snippets(text: str, terms: List[str]) -> List[Dict[str, str]]:
    snippets = []
    lowered = text.lower()
    for term in terms[:4]:
        idx = lowered.find(term.lower())
        if idx >= 0:
            start = max(0, idx - 80)
            end = min(len(text), idx + 180)
            snippets.append({"title": term, "text": text[start:end].strip()})
    if not snippets and text:
        snippets.append({"title": "简历摘录", "text": text[:260]})
    return snippets
