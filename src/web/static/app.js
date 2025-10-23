const form = document.querySelector("#chat-form");
const textarea = document.querySelector("#message");
const submitButton = document.querySelector("#submit-button");
const chatHistory = document.querySelector("#chat-history");
const emptyState = document.querySelector("#empty-state");
const statusButton = document.querySelector("#status-button");
const resetButton = document.querySelector("#reset-button");

const formatGemLabel = (gemName, isOrchestrator) => {
  if (isOrchestrator) {
    return "Sistema";
  }
  return gemName || "GEM";
};

const buildMessage = ({ message, answer, gem_name: gemName, is_orchestrator: isOrchestrator, error }) => {
  const container = document.createElement("article");
  container.className = "chat-message";

  const gemLabel = formatGemLabel(gemName, isOrchestrator);
  const tagClass = isOrchestrator ? "chat-message__tag chat-message__tag--system" : "chat-message__tag";
  const tagText = isOrchestrator ? "Orquestrador" : gemName || "GEM";

  const svgIcon = isOrchestrator
    ? '<svg viewBox="0 0 24 24"><path d="M12 2L2 7L12 12L22 7L12 2Z"/><path d="M2 17L12 22L22 17V12L12 17L2 12V17Z"/></svg>'
    : '<svg viewBox="0 0 24 24"><path d="M12 12C15.315 12 18 9.315 18 6C18 2.685 15.315 0 12 0C8.685 0 6 2.685 6 6C6 9.315 8.685 12 12 12ZM12 14.25C7.995 14.25 0 16.26 0 20.25V22.5H24V20.25C24 16.26 16.005 14.25 12 14.25Z"/></svg>';

  // Preserva quebras de linha e formatação
  const formattedAnswer = answer
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>');

  container.innerHTML = `
    <div class="chat-message__meta">
      <span class="chat-message__role">${svgIcon}${gemLabel}</span>
      <span class="${tagClass}">${tagText}</span>
    </div>
    ${message ? `<p class="chat-message__question">${sanitize(message)}</p>` : ''}
    <div class="chat-message__answer">${formattedAnswer}</div>
    ${error ? `<p class="chat-message__error">⚠️ ${error}</p>` : ""}
  `;

  return container;
};

// Estado de loading
let loadingMessage = null;
let loadingDots = 0;
let loadingInterval = null;

const setLoading = (isLoading) => {
  submitButton.disabled = isLoading;
  textarea.disabled = isLoading;

  if (isLoading) {
    submitButton.classList.add("loading");
    textarea.classList.add("loading");

    // Cria mensagem de loading
    if (!loadingMessage) {
      loadingMessage = document.createElement("div");
      loadingMessage.className = "loading-indicator";
      loadingMessage.innerHTML = `
        <div class="loading-content">
          <div class="loading-spinner"></div>
          <span class="loading-text">Processando<span class="loading-dots"></span></span>
        </div>
      `;
      chatHistory.appendChild(loadingMessage);
      scrollToBottom();
    }

    // Anima os pontos
    loadingDots = 0;
    loadingInterval = setInterval(() => {
      loadingDots = (loadingDots + 1) % 4;
      const dots = '.'.repeat(loadingDots);
      const dotsEl = loadingMessage?.querySelector('.loading-dots');
      if (dotsEl) dotsEl.textContent = dots;
    }, 500);

  } else {
    submitButton.classList.remove("loading");
    textarea.classList.remove("loading");

    // Remove mensagem de loading
    if (loadingMessage) {
      loadingMessage.remove();
      loadingMessage = null;
    }

    // Para animação
    if (loadingInterval) {
      clearInterval(loadingInterval);
      loadingInterval = null;
    }
  }
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

// Previne submissões duplicadas
let isProcessing = false;

// Auto-resize textarea
textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
});

// Handler para o formulário principal
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = textarea.value.trim();

  // Previne submissão se já estiver processando
  if (!message || isProcessing) {
    return;
  }

  isProcessing = true;
  setLoading(true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const payload = await response.json();
    const normalized = {
      message: message,
      answer: payload.answer ?? "",
      gem_name: payload.gem_name,
      is_orchestrator: payload.is_orchestrator ?? false,
      error: payload.error ? sanitize(payload.error) : "",
    };

    if (emptyState) {
      emptyState.remove();
    }

    const messageEl = buildMessage(normalized);
    chatHistory.appendChild(messageEl);
    scrollToBottom();

  } catch (error) {
    const fallback = {
      message: message,
      answer: "Não foi possível processar sua solicitação. Verifique se o Ollama está rodando.",
      gem_name: null,
      is_orchestrator: true,
      error: error instanceof Error ? sanitize(error.message) : "Erro desconhecido",
    };
    if (emptyState) {
      emptyState.remove();
    }
    chatHistory.appendChild(buildMessage(fallback));
  } finally {
    setLoading(false);
    isProcessing = false;
    textarea.value = "";
    textarea.style.height = 'auto';
    textarea.focus();
  }
});

// Handler para botão de status
if (statusButton) {
  statusButton.addEventListener("click", async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/status");
      const payload = await response.json();

      const statusMessage = {
        message: "",
        answer: payload.status,
        gem_name: null,
        is_orchestrator: true,
        error: "",
      };

      if (emptyState) {
        emptyState.remove();
      }

      chatHistory.appendChild(buildMessage(statusMessage));
      scrollToBottom();
    } catch (error) {
      console.error("Erro ao buscar status:", error);
    } finally {
      setLoading(false);
    }
  });
}

// Handler para botão de reset
if (resetButton) {
  resetButton.addEventListener("click", async () => {
    if (!confirm("Deseja reiniciar sua jornada? O progresso será mantido em backup.")) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("/api/reset", { method: "POST" });
      const payload = await response.json();

      // Limpa o histórico visual
      chatHistory.innerHTML = "";

      const resetMessage = {
        message: "",
        answer: payload.message,
        gem_name: null,
        is_orchestrator: true,
        error: "",
      };

      chatHistory.appendChild(buildMessage(resetMessage));
      scrollToBottom();
    } catch (error) {
      console.error("Erro ao reiniciar:", error);
    } finally {
      setLoading(false);
    }
  });
}

// Auto-focus no textarea
textarea.focus();

// Enter para enviar, Shift+Enter para quebra de linha
textarea.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    form.requestSubmit();
  }
});
