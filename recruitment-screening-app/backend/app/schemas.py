from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import BaseModel, Field


AnalysisMode = Literal["single", "batch"]
SalaryPeriod = Literal["year", "month", "day", "hour"]
InterviewLevel = Literal["hr", "business", "executive"]


class SalaryBudget(BaseModel):
    currency: str = "SGD"
    period: SalaryPeriod = "year"
    min: Optional[float] = None
    max: Optional[float] = None


class SalaryExpectation(BaseModel):
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    currency: Optional[str] = None
    period: Optional[SalaryPeriod] = None
    source: str = "not_found"


class SalaryMatchResult(BaseModel):
    status: str
    score: float
    reason: str


class CandidateParsedData(BaseModel):
    candidate_id: str
    name: str
    resume_file_name: str
    resume_file_path: str
    resume_url: str
    resume_text: str
    email: Optional[str] = None
    phone: Optional[str] = None
    current_location: Optional[str] = None
    years_experience: float = 0
    languages: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    markets: List[str] = Field(default_factory=list)
    salary_expectation: SalaryExpectation = Field(default_factory=SalaryExpectation)


class CandidateScoreBreakdown(BaseModel):
    hard_requirements: float
    skills_match: float
    experience_relevance: float
    overseas_market_fit: float
    language_communication: float
    salary_match: float
    risk: float


class MatchSection(BaseModel):
    score: float
    matched: List[str] = Field(default_factory=list)
    missing: List[str] = Field(default_factory=list)
    note: Optional[str] = None


class CandidateAnalysisResult(BaseModel):
    candidate_id: str
    analysis_id: str
    rank: Optional[int] = None
    name: str
    resume_file_name: str
    resume_url: str
    detail_url: str
    total_score: float
    recommendation: str
    summary: str
    scores: CandidateScoreBreakdown
    salary_match: SalaryMatchResult
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    profile: Dict = Field(default_factory=dict)
    match_analysis: Dict[str, MatchSection] = Field(default_factory=dict)
    evidence_snippets: List[Dict[str, str]] = Field(default_factory=list)


class AnalysisRecord(BaseModel):
    analysis_id: str
    mode: AnalysisMode
    job: Dict
    summary: Dict
    candidates: List[CandidateAnalysisResult]


class AnalyzeResponse(BaseModel):
    analysis_id: str
    mode: AnalysisMode
    candidate_count: int
    top_n: int
    redirect_url: str


class InterviewQuestion(BaseModel):
    id: str
    question: str
    intent: str
    evidence: str


class InterviewQuestionResponse(BaseModel):
    candidate_id: str
    candidate_name: str
    level: InterviewLevel
    display_name: str
    default_visible_count: int = 8
    questions: List[InterviewQuestion]
