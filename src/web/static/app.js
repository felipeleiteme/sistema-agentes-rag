const form = document.querySelector("#chat-form");
const textarea = document.querySelector("#question");
const submitButton = document.querySelector("#submit-button");
const chatHistory = document.querySelector("#chat-history");
const emptyState = document.querySelector("#empty-state");
const appStatus = document.querySelector("#app-status");

const formatAgentLabel = (agent, usedContext) => {
  if (agent === "rh") {
    return usedContext ? "Agente RH · Base consultada" : "Agente RH";
  }
  if (agent === "general") {
    return "Assistente Geral";
  }
  return "Sistema";
};

const buildMessage = ({ question, answer, agent, used_context: usedContext, error }) => {
  const container = document.createElement("article");
  container.className = "chat-message";

  const agentTagClass = agent === "general" ? "chat-message__tag chat-message__tag--general" : "chat-message__tag";
  const agentLabel = formatAgentLabel(agent, usedContext);

  const svgIcon =
    agent === "general"
      ? '<svg viewBox="0 0 24 24"><path d="M12 21C12 21 5 14.36 5 9C5 6.24 7.24 4 10 4C11.54 4 13.04 4.71 14 5.88C14.96 4.71 16.46 4 18 4C20.76 4 23 6.24 23 9C23 14.36 16 21 16 21H12Z"/></svg>'
      : '<svg viewBox="0 0 24 24"><path d="M12 12C15.315 12 18 9.315 18 6C18 2.685 15.315 0 12 0C8.685 0 6 2.685 6 6C6 9.315 8.685 12 12 12ZM12 14.25C7.995 14.25 0 16.26 0 20.25V22.5H24V20.25C24 16.26 16.005 14.25 12 14.25Z"/></svg>';

  container.innerHTML = `
    <div class="chat-message__meta">
      <span class="chat-message__role">${svgIcon}${agentLabel}</span>
      <span class="${agentTagClass}">${usedContext ? "Base de Conhecimento" : agent === "general" ? "Assistente" : "Sistema"}</span>
    </div>
    <p class="chat-message__question"><strong>Você:</strong> ${question}</p>
    <p class="chat-message__answer">${answer}</p>
    ${error ? `<p class="chat-message__context">${error}</p>` : ""}
  `;

  return container;
};

const setLoading = (isLoading) => {
  submitButton.disabled = isLoading;
  appStatus.textContent = isLoading ? "Processando" : "Pronto";
};

const scrollToBottom = () => {
  requestAnimationFrame(() => {
    chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: "smooth" });
  });
};

const sanitize = (value) => {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = textarea.value.trim();
  if (!question) {
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const payload = await response.json();
    const normalized = {
      question: sanitize(payload.question ?? question),
      answer: sanitize(payload.answer ?? ""),
      agent: payload.agent ?? "error",
      used_context: payload.used_context ?? false,
      error: payload.error ? sanitize(payload.error) : "",
    };

    if (emptyState) {
      emptyState.remove();
    }

    const message = buildMessage(normalized);
    chatHistory.appendChild(message);
    scrollToBottom();

    if (!response.ok) {
      appStatus.textContent = "Requisição com alerta";
    }
  } catch (error) {
    const fallback = {
      question: sanitize(question),
      answer: "Não foi possível processar sua solicitação. Verifique o servidor e tente novamente.",
      agent: "error",
      used_context: false,
      error: error instanceof Error ? sanitize(error.message) : "Erro desconhecido.",
    };
    if (emptyState) {
      emptyState.remove();
    }
    chatHistory.appendChild(buildMessage(fallback));
  } finally {
    setLoading(false);
    textarea.value = "";
    textarea.focus();
  }
});
