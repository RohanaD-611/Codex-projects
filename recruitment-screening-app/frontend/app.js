const form = document.getElementById("analysis-form");
const statusPill = document.getElementById("status-pill");
const fileInput = document.getElementById("resumes");
const fileList = document.getElementById("file-list");
const emptyState = document.getElementById("empty-state");
const resultsView = document.getElementById("results-view");
const detailView = document.getElementById("detail-view");
const summaryBar = document.getElementById("summary-bar");
const candidateList = document.getElementById("candidate-list");
const drawer = document.getElementById("interview-drawer");
const exportHtml = document.getElementById("export-html");
const exportCsv = document.getElementById("export-csv");
const exportJson = document.getElementById("export-json");

let currentAnalysis = null;

fileInput.addEventListener("change", () => {
  const files = Array.from(fileInput.files || []);
  fileList.innerHTML = files.length
    ? files.map((file) => `<div>${escapeHtml(file.name)}</div>`).join("")
    : "尚未选择文件";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("分析中");
  const button = document.getElementById("analyze-button");
  button.disabled = true;

  try {
    const data = new FormData(form);
    const response = await fetch("/api/analyze", { method: "POST", body: data });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "分析失败");
    }
    const result = await response.json();
    history.pushState({}, "", result.redirect_url);
    await loadAnalysis(result.analysis_id);
    setStatus("已完成");
  } catch (error) {
    setStatus("分析失败");
    alert(error.message || String(error));
  } finally {
    button.disabled = false;
  }
});

window.addEventListener("popstate", () => route());
document.addEventListener("click", async (event) => {
  const detailLink = event.target.closest("[data-detail-id]");
  if (detailLink) {
    event.preventDefault();
    history.pushState({}, "", `/candidates/${detailLink.dataset.detailId}`);
    await loadCandidate(detailLink.dataset.detailId);
    return;
  }

  const questionButton = event.target.closest("[data-question-level]");
  if (questionButton) {
    const { candidateId, questionLevel } = questionButton.dataset;
    await openQuestions(candidateId, questionLevel);
    return;
  }

  const more = event.target.closest("[data-expand-questions]");
  if (more) {
    drawer.querySelectorAll(".question-card.hidden").forEach((item) => item.classList.remove("hidden"));
    more.remove();
  }
});

async function route() {
  const path = location.pathname;
  if (path.startsWith("/results/")) {
    await loadAnalysis(path.split("/").pop());
    return;
  }
  if (path.startsWith("/candidates/")) {
    await loadCandidate(path.split("/").pop());
    return;
  }
}

async function loadAnalysis(analysisId) {
  const response = await fetch(`/api/analysis/${analysisId}`);
  if (!response.ok) throw new Error("无法读取分析结果");
  currentAnalysis = await response.json();
  renderAnalysis(currentAnalysis);
}

function renderAnalysis(data) {
  emptyState.classList.add("hidden");
  detailView.classList.add("hidden");
  resultsView.classList.remove("hidden");
  setExports(data.analysis_id);
  summaryBar.innerHTML = `
    ${metric("岗位", data.job.title || "-")}
    ${metric("市场", data.job.target_market || "-")}
    ${metric("简历数", data.job.candidate_count ?? data.candidates.length)}
    ${metric("平均分", data.summary.average_score ?? 0)}
  `;
  candidateList.innerHTML = data.candidates.map(renderCandidateCard).join("");
}

function renderCandidateCard(candidate) {
  return `
    <article class="candidate-card">
      <div class="candidate-top">
        <div>
          <a class="candidate-title" href="/candidates/${candidate.candidate_id}" data-detail-id="${candidate.candidate_id}">#${candidate.rank || "-"} ${escapeHtml(candidate.name)}</a>
          <p>${escapeHtml(candidate.summary)}</p>
          <span class="tag">${escapeHtml(candidate.recommendation)}</span>
          <span class="tag">${escapeHtml(candidate.salary_match.status)}</span>
        </div>
        <div class="score-number">${candidate.total_score}</div>
      </div>
      <div class="card-actions">
        <a class="ghost-button" href="${candidate.resume_url}" target="_blank" rel="noreferrer">打开简历</a>
        ${interviewTrigger(candidate.candidate_id)}
      </div>
      ${scoreGroup(candidate.scores)}
      ${insightGrid(candidate)}
    </article>
  `;
}

async function loadCandidate(candidateId) {
  const response = await fetch(`/api/candidates/${candidateId}`);
  if (!response.ok) throw new Error("无法读取候选人详情");
  const candidate = await response.json();
  emptyState.classList.add("hidden");
  resultsView.classList.add("hidden");
  detailView.classList.remove("hidden");
  detailView.innerHTML = renderCandidateDetail(candidate);
}

function renderCandidateDetail(candidate) {
  const profile = candidate.profile || {};
  return `
    <article class="detail-card">
      <div class="candidate-top">
        <div>
          <h2>${escapeHtml(candidate.name)}</h2>
          <p>${escapeHtml(candidate.summary)}</p>
          <span class="tag">${escapeHtml(candidate.recommendation)}</span>
          <span class="tag">${escapeHtml(candidate.salary_match.status)}</span>
        </div>
        <div class="score-number">${candidate.total_score}</div>
      </div>
      <div class="card-actions">
        <a class="ghost-button" href="${candidate.resume_url}" target="_blank" rel="noreferrer">打开原简历</a>
        ${interviewTrigger(candidate.candidate_id)}
        <button class="ghost-button" onclick="history.back()">返回</button>
      </div>
    </article>
    <div class="detail-grid">
      <section class="detail-card">
        <h2>基础信息</h2>
        <p>年限：${profile.years_experience || 0}</p>
        <p>语言：${(profile.languages || []).join("、") || "待确认"}</p>
        <p>市场：${(profile.markets || []).join("、") || "待确认"}</p>
        <p>技能：${(profile.skills || []).join("、") || "待确认"}</p>
      </section>
      <section class="detail-card">
        <h2>分维度评分</h2>
        ${scoreGroup(candidate.scores)}
      </section>
    </div>
    <section class="detail-card">
      <h2>逐项匹配分析</h2>
      ${Object.entries(candidate.match_analysis || {}).map(([key, item]) => `
        <div class="insight-box">
          <strong>${labelFor(key)} ${item.score}</strong>
          <p>已匹配：${(item.matched || []).join("、") || "无"}</p>
          <p>待确认：${(item.missing || []).join("、") || item.note || "无"}</p>
        </div>
      `).join("")}
    </section>
    <section class="detail-card">
      <h2>优势 / 缺口 / 风险</h2>
      ${insightGrid(candidate)}
    </section>
    <section class="detail-card">
      <h2>关键证据摘录</h2>
      ${(candidate.evidence_snippets || []).map((snippet) => `<p><strong>${escapeHtml(snippet.title)}：</strong>${escapeHtml(snippet.text)}</p>`).join("") || "<p>暂无摘录</p>"}
    </section>
  `;
}

async function openQuestions(candidateId, level) {
  const response = await fetch(`/api/candidates/${candidateId}/interview-questions?level=${level}`);
  if (!response.ok) throw new Error("无法读取面试问题");
  const data = await response.json();
  drawer.innerHTML = `
    <div class="drawer-header">
      <div>
        <h2>${escapeHtml(data.candidate_name)}</h2>
        <span class="tag">${escapeHtml(data.display_name)}</span>
      </div>
    </div>
    <div>
      ${data.questions.map((item, index) => `
        <article class="question-card ${index >= data.default_visible_count ? "hidden" : ""}">
          <p><strong>${index + 1}. ${escapeHtml(item.question)}</strong></p>
          <p>提问意图：${escapeHtml(item.intent)}</p>
          <p>对应简历证据：${escapeHtml(item.evidence)}</p>
        </article>
      `).join("")}
      ${data.questions.length > data.default_visible_count ? '<button class="ghost-button" data-expand-questions>展开更多</button>' : ""}
    </div>
  `;
}

function interviewTrigger(candidateId) {
  return `
    <div class="interview-menu">
      <button class="ghost-button" type="button">面试提问</button>
      <div class="interview-options">
        <button type="button" data-candidate-id="${candidateId}" data-question-level="hr">HR面试</button>
        <button type="button" data-candidate-id="${candidateId}" data-question-level="business">业务面试</button>
        <button type="button" data-candidate-id="${candidateId}" data-question-level="executive">管理层面试</button>
      </div>
    </div>
  `;
}

function scoreGroup(scores) {
  return `<div class="score-grid">
    ${scoreRow("硬性条件", scores.hard_requirements)}
    ${scoreRow("岗位技能", scores.skills_match)}
    ${scoreRow("经验相关性", scores.experience_relevance)}
    ${scoreRow("出海/市场", scores.overseas_market_fit)}
    ${scoreRow("语言沟通", scores.language_communication)}
    ${scoreRow("薪酬匹配", scores.salary_match)}
    ${scoreRow("风险", scores.risk)}
  </div>`;
}

function scoreRow(label, value) {
  const safe = Math.max(0, Math.min(100, Number(value) || 0));
  return `<div class="score-row"><span>${label}</span><div class="score-track"><div class="score-fill" style="width:${safe}%"></div></div><strong>${safe}</strong></div>`;
}

function insightGrid(candidate) {
  return `<div class="insight-grid">
    ${insightBox("优势", candidate.strengths)}
    ${insightBox("缺口", candidate.gaps)}
    ${insightBox("风险", candidate.risks)}
  </div>`;
}

function insightBox(title, items) {
  return `<div class="insight-box"><strong>${title}</strong>${(items || []).map((item) => `<p>${escapeHtml(item)}</p>`).join("")}</div>`;
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong></div>`;
}

function labelFor(key) {
  return {
    hard_requirements: "硬性条件",
    must_have: "Must-have",
    nice_to_have: "Nice-to-have",
    salary: "薪酬匹配",
  }[key] || key;
}

function setExports(analysisId) {
  exportHtml.href = `/api/analysis/${analysisId}/export/html`;
  exportCsv.href = `/api/analysis/${analysisId}/export/csv`;
  exportJson.href = `/api/analysis/${analysisId}/export/json`;
  [exportHtml, exportCsv, exportJson].forEach((item) => item.classList.remove("hidden"));
}

function setStatus(text) {
  statusPill.textContent = text;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

route();
