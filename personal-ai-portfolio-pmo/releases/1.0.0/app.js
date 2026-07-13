const answers = [
  {
    question: "你是谁？",
    answer:
      "我是 Yamu Deng，马来名 Rohana。我的经历横跨马来语信息处理、海外项目管理、MBA 商业分析、出海业务探索和 AI 工作流实践。现在主要关注 AI、出海项目、跨文化管理以及人与系统如何更好协作。",
  },
  {
    question: "你为什么关注 AI 和出海管理？",
    answer:
      "因为中国企业出海的很多问题并不只是语言问题，而是总部制度、业务流程、当地文化和实际执行之间的错位。AI 可以帮助拆解制度、整理信息、改写 SOP、做差距分析和沉淀经验，成为管理系统里更轻的协作层。",
  },
  {
    question: "你做过哪些 AI 实战案例？",
    answer:
      "目前重点案例包括属地化运营 / 跨文化 SOP 分析 Skill、Idea Coach Skill、Writing Style Skill，以及候选人与招聘需求匹配分析 Skill。它们分别对应出海制度落地、想法澄清、个人表达和海外招聘筛选场景。",
  },
  {
    question: "什么是属地化运营 / 跨文化 SOP 分析 Skill？",
    answer:
      "这是一个用于预检总部 SOP、KPI、政策和管理规则在东南亚落地风险的 Skill。它会做条款级拆解，识别可能的文化摩擦、执行阻力、沟通误差和信任风险，并给出红黄绿风险判断、双语改写和管理者落地提醒。",
  },
  {
    question: "你的海外管理模型是什么？",
    answer:
      "我把出海管理理解为一个系统：业务主链负责准入、供应、销售和回款；横切层负责组织、流程、IT 和总部海外协同；底线层负责合规、风险、公共关系和退出机制；AI 协助层则用于分析、执行和治理支持。",
  },
  {
    question: "你适合什么类型的合作？",
    answer:
      "比较适合围绕 AI 工作流、出海项目支持、跨文化 SOP 分析、内容系统搭建、个人知识库和招聘匹配分析等方向合作。我更擅长把复杂信息拆成结构，把模糊问题收敛成可执行方案。",
  },
  {
    question: "如何联系你？",
    answer:
      "可以通过邮箱 yamu.deng@outlook.com 联系，也可以添加微信 M_Kisann，或关注公众号「她与AI时代」。手机号暂不公开展示。",
  },
];

const chatToggle = document.querySelector("#chatToggle");
const chatPanel = document.querySelector("#chatPanel");
const chatClose = document.querySelector("#chatClose");
const chatQuestions = document.querySelector("#chatQuestions");
const chatAnswer = document.querySelector("#chatAnswer");

function setPanelOpen(isOpen) {
  chatPanel.classList.toggle("open", isOpen);
  chatToggle.setAttribute("aria-expanded", String(isOpen));
}

answers.forEach((item, index) => {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = item.question;
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".chat-questions button")
      .forEach((node) => node.classList.remove("active"));
    button.classList.add("active");
    chatAnswer.textContent = item.answer;
  });
  if (index === 0) {
    button.classList.add("active");
    chatAnswer.textContent = item.answer;
  }
  chatQuestions.append(button);
});

chatToggle.addEventListener("click", () => {
  setPanelOpen(!chatPanel.classList.contains("open"));
});

chatClose.addEventListener("click", () => {
  setPanelOpen(false);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setPanelOpen(false);
  }
});
