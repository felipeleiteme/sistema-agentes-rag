const form = document.querySelector("#chat-form");
const textarea = document.querySelector("#message");
const submitButton = document.querySelector("#submit-button");
const chatHistory = document.querySelector("#chat-history");
const emptyState = document.querySelector("#empty-state");
const statusButton = document.querySelector("#status-button");
const themeToggle = document.querySelector("#theme-toggle");
const completeButton = document.querySelector("#complete-button");

// History sidebar elements
const historyToggle = document.querySelector("#history-toggle");
const historySidebar = document.querySelector("#history-sidebar");
const closeSidebar = document.querySelector("#close-sidebar");
const newChatButton = document.querySelector("#new-chat-button");
const historyList = document.querySelector("#history-list");

// Current conversation ID
let currentConversationId = null;

// Function to update the visibility and state of the complete button based on current GEM
const updateCompleteButton = async () => {
  try {
    const response = await fetch('/api/gems');
    const data = await response.json();
    
    const currentGem = data.current_gem;
    
    if (completeButton) {
      if (currentGem) {
        // Show and enable the button if there's an active GEM
        completeButton.style.display = 'block';
        completeButton.disabled = false;
      } else {
        // Hide the button if no GEM is active
        completeButton.style.display = 'none';
        completeButton.disabled = true;
      }
    }
  } catch (error) {
    console.error('Error checking GEM status:', error);
    // In case of error, show the button to maintain functionality
    if (completeButton) {
      completeButton.style.display = 'block';
      completeButton.disabled = false;
    }
  }
};

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

  const answerElement = container.querySelector('.chat-message__answer');

  if (answer && answerElement) {
    const actions = document.createElement('div');
    actions.className = 'chat-message__actions';

    const copyButton = document.createElement('button');
    copyButton.type = 'button';
    copyButton.className = 'chat-message__copy';
    copyButton.title = 'Copiar resposta';
    copyButton.innerHTML = `
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M16 1H4C2.895 1 2 1.895 2 3V17H4V3H16V1Z" />
        <path d="M19 5H8C6.895 5 6 5.895 6 7V21C6 22.105 6.895 23 8 23H19C20.105 23 21 22.105 21 21V7C21 5.895 20.105 5 19 5ZM8 21V7H19L19.002 21H8Z" />
      </svg>
      <span>Copiar</span>
    `;

    copyButton.addEventListener('click', async () => {
      const text = answerElement.innerText.trim();
      if (!text) return;

      try {
        if (!navigator.clipboard || typeof navigator.clipboard.writeText !== 'function') {
          throw new Error('API de clipboard indisponível');
        }

        await navigator.clipboard.writeText(text);
        copyButton.classList.add('chat-message__copy--success');
        copyButton.querySelector('span').textContent = 'Copiado!';
        setTimeout(() => {
          copyButton.classList.remove('chat-message__copy--success');
          copyButton.querySelector('span').textContent = 'Copiar';
        }, 2000);
      } catch (err) {
        console.error('Não foi possível copiar o conteúdo:', err);
        copyButton.classList.add('chat-message__copy--error');
        copyButton.querySelector('span').textContent = 'Erro';
        setTimeout(() => {
          copyButton.classList.remove('chat-message__copy--error');
          copyButton.querySelector('span').textContent = 'Copiar';
        }, 2000);
      }
    });

    actions.appendChild(copyButton);
    container.appendChild(actions);
  }

  return container;
};

// Estado de loading
let loadingMessage = null;
let loadingInterval = null;
let loadingMessageIndex = 0;

const loadingMessages = [
  "Pensando na melhor resposta",
  "Analisando informações",
  "Organizando ideias",
  "Conectando conceitos",
  "Preparando resposta",
  "Processando contexto"
];

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
          <span class="loading-text">${loadingMessages[0]}<span class="loading-dots">...</span></span>
        </div>
      `;
      chatHistory.appendChild(loadingMessage);
      scrollToBottom();
    }

    // Rotaciona as mensagens
    loadingMessageIndex = 0;
    loadingInterval = setInterval(() => {
      loadingMessageIndex = (loadingMessageIndex + 1) % loadingMessages.length;
      const textEl = loadingMessage?.querySelector('.loading-text');
      if (textEl) {
        textEl.innerHTML = `${loadingMessages[loadingMessageIndex]}<span class="loading-dots">...</span>`;
      }
    }, 2000);

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

// Handler para streaming de resposta
const handleStreamingResponse = async (message, options = {}) => {
  const displayMessage = typeof options.displayMessage === 'string' ? options.displayMessage : message;

  if (emptyState) {
    emptyState.remove();
  }

  // Cria container de resposta vazio
  const responseContainer = document.createElement("article");
  responseContainer.className = "chat-message";
  chatHistory.appendChild(responseContainer);

  let accumulated = "";
  let gemName = null;
  let isOrchestrator = false;
  let buffer = ""; // Buffer para acumular chunks incompletos

  try {
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      buffer += chunk;
      const lines = buffer.split('\n');

      // Mantém a última linha no buffer se não terminar com \n
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const jsonStr = line.slice(6).trim();
            if (!jsonStr) continue; // Ignora linhas vazias
            const data = JSON.parse(jsonStr);

          if (data.type === 'start') {
            // Mostra indicador de digitação
            responseContainer.innerHTML = `
              <div class="loading-indicator">
                <div class="loading-content">
                  <div class="loading-spinner"></div>
                  <span class="loading-text">Pensando...</span>
                </div>
              </div>
            `;
            scrollToBottom();
          } else if (data.type === 'chunk') {
            accumulated = data.accumulated;
            gemName = data.gem_name;
            isOrchestrator = data.is_orchestrator;

            // Atualiza a resposta em tempo real
            const gemLabel = formatGemLabel(gemName, isOrchestrator);
            const tagClass = isOrchestrator ? "chat-message__tag chat-message__tag--system" : "chat-message__tag";
            const tagText = isOrchestrator ? "Orquestrador" : gemName || "GEM";
            const svgIcon = isOrchestrator
              ? '<svg viewBox="0 0 24 24"><path d="M12 2L2 7L12 12L22 7L12 2Z"/><path d="M2 17L12 22L22 17V12L12 17L2 12V17Z"/></svg>'
              : '<svg viewBox="0 0 24 24"><path d="M12 12C15.315 12 18 9.315 18 6C18 2.685 15.315 0 12 0C8.685 0 6 2.685 6 6C6 9.315 8.685 12 12 12ZM12 14.25C7.995 14.25 0 16.26 0 20.25V22.5H24V20.25C24 16.26 16.005 14.25 12 14.25Z"/></svg>';

            const formattedAnswer = accumulated
              .replace(/\n/g, '<br>')
              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
              .replace(/`(.*?)`/g, '<code>$1</code>');

            responseContainer.innerHTML = `
              <div class="chat-message__meta">
                <span class="chat-message__role">${svgIcon}${gemLabel}</span>
                <span class="${tagClass}">${tagText}</span>
              </div>
              ${displayMessage !== null ? `<p class="chat-message__question">${sanitize(displayMessage)}</p>` : ''}
              <div class="chat-message__answer streaming">${formattedAnswer}<span class="typing-cursor">▊</span></div>
            `;
            scrollToBottom();
          } else if (data.type === 'done') {
            // Remove cursor de digitação e mostra resposta final
            const normalized = {
              message: displayMessage !== null ? displayMessage : '', // Use empty string if null
              answer: data.answer ?? "",
              gem_name: data.gem_name,
              is_orchestrator: data.is_orchestrator ?? false,
              error: data.error ? sanitize(data.error) : "",
            };

            // Replace container with the full message if displayMessage is not null, otherwise just update the sidebar
            if (displayMessage !== null) {
              // Remove the streaming class before replacing
              const answerElement = responseContainer.querySelector('.chat-message__answer');
              if (answerElement) {
                answerElement.classList.remove('streaming');
              }
              // Adiciona animação de conclusão
              responseContainer.style.transition = 'all 0.3s ease-out';
              responseContainer.replaceWith(buildMessage(normalized));
              scrollToBottom();
            } else {
              // For commands that shouldn't be shown in chat, just update sidebar and remove loading indicator
              responseContainer.remove();
            }

            // Atualiza sidebar se existir
            if (window.updateGemsSidebar) {
              window.updateGemsSidebar();
            }
          } else if (data.type === 'error') {
            throw new Error(data.error);
          }
          } catch (parseError) {
            // Ignora erros de parsing de JSON incompleto
            console.warn('Erro ao fazer parse de linha SSE:', line, parseError);
          }
        }
      }
    }
  } catch (error) {
    console.error('Erro no streaming:', error);

    // Determina a mensagem de erro apropriada
    let errorMessage = "Não foi possível processar sua solicitação.";
    if (error.message.includes('fetch') || error.message.includes('network')) {
      errorMessage = "Erro de conexão. Verifique se o servidor está rodando.";
    } else if (error.message.includes('timeout')) {
      errorMessage = "A requisição demorou muito. Tente novamente.";
    } else if (error.message.includes('Ollama')) {
      errorMessage = "Erro ao conectar com o Ollama. Verifique se está rodando (ollama serve).";
    }

    const fallback = {
      message: displayMessage !== null ? displayMessage : '', // Use empty string if null
      answer: errorMessage,
      gem_name: null,
      is_orchestrator: true,
      error: error instanceof Error ? sanitize(error.message) : "Erro desconhecido",
    };

    if (displayMessage !== null) {
      // Remove the streaming class before replacing
      const answerElement = responseContainer.querySelector('.chat-message__answer');
      if (answerElement) {
        answerElement.classList.remove('streaming');
      }
      responseContainer.replaceWith(buildMessage(fallback));
    } else {
      // For commands that shouldn't be shown in chat, just update sidebar and remove loading indicator
      responseContainer.remove();
      console.error('Error processing command:', error);
    }
  }
};

const sendMessage = async (message, options = {}) => {
  const trimmed = message.trim();
  if (!trimmed || isProcessing) {
    return;
  }

  // Mostra input wrapper se for o primeiro envio
  showInputWrapper();

  isProcessing = true;
  setLoading(true);

  // Disable complete button during processing
  if (completeButton) {
    completeButton.disabled = true;
  }

  try {
    await handleStreamingResponse(trimmed, options);
  } finally {
    setLoading(false);
    isProcessing = false;

    // Re-enable complete button after processing
    if (completeButton) {
      completeButton.disabled = false;
    }

    if (!options.preserveTextarea) {
      textarea.value = "";
      textarea.style.height = 'auto';
    }

    // Save conversation after each message
    const messages = getCurrentMessages();
    if (messages.length > 0) {
      saveConversation(currentConversationId, messages);
    }

    textarea.focus();
  }
};

// Handler para o formulário principal
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await sendMessage(textarea.value);
});

if (completeButton) {
  completeButton.addEventListener('click', async () => {
    await sendMessage('/concluir', {
      displayMessage: null, // Don't show the command in chat
      preserveTextarea: true,
    });
  });
}

// Botão de status removido (não mais necessário)

// Handler para botão de reset
// ========================================
// HISTORY SIDEBAR MANAGEMENT
// ========================================

// Load conversations list from localStorage
const loadConversationsList = () => {
  const conversations = JSON.parse(localStorage.getItem('conversations') || '[]');
  return conversations.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
};

// Save conversation to localStorage
const saveConversation = (conversationId, messages) => {
  const conversations = loadConversationsList();
  const existingIndex = conversations.findIndex(c => c.id === conversationId);

  const conversationData = {
    id: conversationId,
    messages: messages,
    updatedAt: new Date().toISOString(),
    title: messages.length > 0 ? messages[0].message.substring(0, 50) : 'Nova Conversa'
  };

  if (existingIndex >= 0) {
    conversations[existingIndex] = conversationData;
  } else {
    conversations.unshift(conversationData);
  }

  localStorage.setItem('conversations', JSON.stringify(conversations));
  renderHistoryList();
};

// Get current conversation messages
const getCurrentMessages = () => {
  const messageElements = chatHistory.querySelectorAll('.chat-message');
  return Array.from(messageElements).map(el => {
    const question = el.querySelector('.chat-message__question')?.textContent || '';
    const answer = el.querySelector('.chat-message__answer')?.textContent || '';
    const gemName = el.querySelector('.chat-message__role')?.textContent || '';

    return { message: question, answer: answer, gem_name: gemName };
  });
};

// Load conversation by ID
const loadConversation = (conversationId) => {
  const conversations = loadConversationsList();
  const conversation = conversations.find(c => c.id === conversationId);

  if (conversation) {
    currentConversationId = conversationId;
    chatHistory.innerHTML = '';

    conversation.messages.forEach(msg => {
      chatHistory.appendChild(buildMessage(msg));
    });

    scrollToBottom();
    renderHistoryList();
    toggleSidebar(false);
  }
};

// Create new conversation
const createNewConversation = () => {
  currentConversationId = 'conv-' + Date.now();
  chatHistory.innerHTML = '';

  if (emptyState) {
    chatHistory.appendChild(emptyState);
  }

  renderHistoryList();
  toggleSidebar(false);
};

// Render history list
const renderHistoryList = () => {
  const conversations = loadConversationsList();

  if (conversations.length === 0) {
    historyList.innerHTML = '<div class="history-empty">Nenhuma conversa ainda</div>';
    return;
  }

  historyList.innerHTML = conversations.map(conv => {
    const date = new Date(conv.updatedAt);
    const formattedDate = date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'short'
    });
    const formattedTime = date.toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    });

    const isActive = conv.id === currentConversationId;

    return `
      <div class="history-item ${isActive ? 'active' : ''}" data-conversation-id="${conv.id}">
        <div class="history-item-title">${conv.title}</div>
        <div class="history-item-meta">
          <span>${formattedDate}</span>
          <span>•</span>
          <span>${formattedTime}</span>
        </div>
      </div>
    `;
  }).join('');

  // Add click handlers
  historyList.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
      const convId = item.getAttribute('data-conversation-id');
      loadConversation(convId);
    });
  });
};

// Toggle sidebar
const toggleSidebar = (open = null) => {
  if (open === null) {
    historySidebar.classList.toggle('open');
  } else if (open) {
    historySidebar.classList.add('open');
  } else {
    historySidebar.classList.remove('open');
  }
};

// Event listeners for history sidebar
if (historyToggle) {
  historyToggle.addEventListener('click', () => {
    toggleSidebar();
  });
}

if (closeSidebar) {
  closeSidebar.addEventListener('click', () => {
    toggleSidebar(false);
  });
}

if (newChatButton) {
  newChatButton.addEventListener('click', createNewConversation);
}

// Initialize: Create first conversation if none exists
if (!currentConversationId) {
  const conversations = loadConversationsList();
  if (conversations.length > 0) {
    currentConversationId = conversations[0].id;
  } else {
    currentConversationId = 'conv-' + Date.now();
  }
}

// Render initial history list
renderHistoryList();

// Auto-focus no textarea
textarea.focus();

// Enter para enviar, Shift+Enter para quebra de linha
textarea.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    form.requestSubmit();
  }
});

// Theme toggle functionality
const applyTheme = (theme) => {
  if (theme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
  } else {
    document.documentElement.removeAttribute('data-theme');
  }
  localStorage.setItem('theme', theme);
};

const toggleTheme = () => {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  applyTheme(newTheme);
};

// Initialize theme from localStorage or system preference
const initializeTheme = () => {
  const savedTheme = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme) {
    applyTheme(savedTheme);
  } else {
    // Default to dark theme, but respect system preference
    applyTheme(systemPrefersDark ? 'dark' : 'light');
  }
};

// Add event listener for theme toggle button
if (themeToggle) {
  themeToggle.addEventListener('click', toggleTheme);
}

// ===== HISTORY RESTORATION =====

// Função para restaurar histórico de conversas
const restoreHistory = async () => {
  try {
    const response = await fetch('/api/history');
    const data = await response.json();

    const { current_gem, active_history, completed_gems } = data;

    // Se não há GEM ativo e nem histórico, não precisa restaurar
    if (!current_gem && (!completed_gems || completed_gems.length === 0)) {
      return;
    }

    // Se há histórico, mostrar opção de continuar ou resetar
    if (active_history && active_history.length > 0) {
      const shouldRestore = await showRestoreDialog();

      if (shouldRestore) {
        // Oculta welcome screen
        if (emptyState) {
          emptyState.style.display = 'none';
        }

        // Mostra input wrapper
        showInputWrapper();

        // Restaura as mensagens do histórico
        for (const msg of active_history) {
          if (msg.role === 'user') {
            // Mensagem do usuário (não mostramos separadamente no nosso UI)
            continue;
          } else if (msg.role === 'assistant') {
            const messageData = {
              message: '', // Não mostramos a pergunta separadamente
              answer: msg.content,
              gem_name: current_gem ? getGemNameFromId(current_gem) : null,
              is_orchestrator: false,
              error: ''
            };
            chatHistory.appendChild(buildMessage(messageData));
          } else if (msg.role === 'system') {
            // System messages são as instruções, não mostramos no chat
            continue;
          }
        }

        scrollToBottom();

        // Atualiza sidebar
        if (window.updateGemsSidebar) {
          window.updateGemsSidebar();
        }
      } else {
        // Usuário escolheu resetar
        await resetJourney();
      }
    }
  } catch (error) {
    console.error('Erro ao restaurar histórico:', error);
    // Se der erro, apenas continua normalmente
  }
};

// Função auxiliar para obter nome do GEM pelo ID
const getGemNameFromId = (gemId) => {
  const gemNames = {
    'gem1_mestre_mapeamento': 'Mestre do Mapeamento',
    'gem2_diagnosticador_foco': 'Diagnosticador F.O.C.O.',
    'gem3_validador_estrategico': 'Validador Estratégico',
    'gem4_laboratorio_cientifico': 'Laboratório Científico',
    'gem5_tutor_socratico': 'Tutor Socrático',
    'gem6_arquiteto_implementacao': 'Arquiteto de Implementação',
    'gem7_construtor_sistemas': 'Construtor de Sistemas'
  };
  return gemNames[gemId] || 'GEM';
};

// Mostra dialog para escolher entre continuar ou resetar
const showRestoreDialog = () => {
  return new Promise((resolve) => {
    const dialog = document.createElement('div');
    dialog.className = 'restore-dialog';
    dialog.innerHTML = `
      <div class="restore-dialog__overlay"></div>
      <div class="restore-dialog__content">
        <h2 class="restore-dialog__title">💎 Bem-vindo de volta!</h2>
        <p class="restore-dialog__message">
          Encontramos uma conversa anterior em andamento.
          Deseja continuar de onde parou ou começar uma nova jornada?
        </p>
        <div class="restore-dialog__actions">
          <button class="btn btn--secondary" id="restore-reset">
            🔄 Começar do Zero
          </button>
          <button class="btn btn--primary" id="restore-continue">
            ▶️ Continuar
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(dialog);

    const continueBtn = dialog.querySelector('#restore-continue');
    const resetBtn = dialog.querySelector('#restore-reset');

    const cleanup = () => {
      dialog.remove();
    };

    continueBtn.addEventListener('click', () => {
      cleanup();
      resolve(true);
    });

    resetBtn.addEventListener('click', () => {
      cleanup();
      resolve(false);
    });
  });
};

// Função para resetar jornada
const resetJourney = async () => {
  try {
    const response = await fetch("/api/reset", { method: "POST" });
    const payload = await response.json();

    // Limpa o histórico visual
    chatHistory.innerHTML = '';

    // Mostra welcome screen novamente
    if (emptyState) {
      emptyState.style.display = 'flex';
    }

    // Esconde input wrapper
    hideInputWrapper();

    // Atualiza sidebar
    if (window.updateGemsSidebar) {
      window.updateGemsSidebar();
    }
  } catch (error) {
    console.error("Erro ao resetar:", error);
  }
};

// Initialize theme on page load
initializeTheme();

// Restaura histórico ao carregar a página
restoreHistory();

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem('theme')) {
    applyTheme(e.matches ? 'dark' : 'light');
  }
});

// ===== GEMS SIDEBAR NAVIGATION =====

// Cria a sidebar com todos os GEMs
const createGemsSidebar = () => {
  const sidebar = document.createElement('aside');
  sidebar.className = 'gems-sidebar gems-sidebar--collapsed'; // Inicia colapsada
  sidebar.id = 'gems-sidebar';
  sidebar.innerHTML = `
    <div class="gems-sidebar__header">
      <h3 class="gems-sidebar__title">GEMs Disponíveis</h3>
      <button class="gems-sidebar__toggle" id="sidebar-toggle" aria-label="Alternar sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
    <div class="gems-sidebar__content" id="gems-list">
      <div class="gems-sidebar__loading">Carregando...</div>
    </div>
    <div class="gems-sidebar__actions">
      <button class="gems-sidebar__action" id="export-journey-button" type="button">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M5 19H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
        <span>Exportar Jornada</span>
      </button>
    </div>
  `;
  document.body.appendChild(sidebar);

  // Toggle button
  const toggleBtn = document.getElementById('sidebar-toggle');
  toggleBtn?.addEventListener('click', () => {
    sidebar.classList.toggle('gems-sidebar--collapsed');
  });

  const exportButton = sidebar.querySelector('#export-journey-button');
  exportButton?.addEventListener('click', () => {
    window.open('/api/export', '_blank');
  });

  return sidebar;
};

// Atualiza a lista de GEMs
const updateGemsSidebar = async () => {
  try {
    const response = await fetch('/api/gems');
    const data = await response.json();

    window.gemsInfo = data;

    const gemsList = document.getElementById('gems-list');
    if (!gemsList) return;

    // Calcula progresso (quantos GEMs já foram visitados/completados)
    const currentIndex = data.gems.findIndex(g => g.id === data.current_gem);
    const progress = currentIndex >= 0 ? ((currentIndex) / data.gems.length) * 100 : 0;

    // Adiciona indicador de progresso
    const progressHTML = `
      <div class="gems-progress">
        <div class="gems-progress__header">
          <span class="gems-progress__label">Progresso da Jornada</span>
          <span class="gems-progress__percentage">${Math.round(progress)}%</span>
        </div>
        <div class="gems-progress__bar">
          <div class="gems-progress__fill" style="width: ${progress}%"></div>
        </div>
        <div class="gems-progress__info">
          ${currentIndex >= 0 ? `GEM ${currentIndex + 1} de ${data.gems.length}` : 'Não iniciado'}
        </div>
      </div>
    `;

    const gemsHTML = data.gems.map((gem, index) => {
      const isActive = gem.id === data.current_gem;
      const isCompleted = index < currentIndex;
      const activeClass = isActive ? 'gems-sidebar__item--active' : '';
      const completedClass = isCompleted ? 'gems-sidebar__item--completed' : '';

      return `
        <button
          class="gems-sidebar__item ${activeClass} ${completedClass}"
          data-gem-id="${gem.id}"
          title="${gem.specialty}"
        >
          <div class="gems-sidebar__item-number">${index + 1}</div>
          <div class="gems-sidebar__item-emoji">${gem.emoji}</div>
          <div class="gems-sidebar__item-info">
            <div class="gems-sidebar__item-name">${gem.name}</div>
            <div class="gems-sidebar__item-role">${gem.role}</div>
          </div>
          ${isActive ? '<div class="gems-sidebar__item-badge">Atual</div>' : ''}
          ${isCompleted ? '<div class="gems-sidebar__item-check">✓</div>' : ''}
        </button>
      `;
    }).join('');

    gemsList.innerHTML = progressHTML + gemsHTML;

    // Adiciona event listeners aos botões
    gemsList.querySelectorAll('.gems-sidebar__item').forEach(btn => {
      btn.addEventListener('click', async () => {
        const gemId = btn.dataset.gemId;
        await activateGem(gemId);
      });
    });

    // Update the complete button after updating the sidebar
    updateCompleteButton();
    
    return data;

  } catch (error) {
    console.error('Erro ao carregar GEMs:', error);
    const gemsList = document.getElementById('gems-list');
    if (gemsList) {
      gemsList.innerHTML = '<div class="gems-sidebar__error">Erro ao carregar GEMs</div>';
    }
  }
};

// Ativa um GEM específico
const activateGem = async (gemId) => {
  try {
    const response = await fetch(`/api/gems/${gemId}/activate`, {
      method: 'POST',
    });

    const data = await response.json();

    if (response.ok) {
      // Mostra mensagem de confirmação
      const confirmMessage = {
        message: "",
        answer: data.message,
        gem_name: data.gem_name,
        is_orchestrator: false,
        error: "",
      };

      if (emptyState) {
        emptyState.remove();
      }

      chatHistory.appendChild(buildMessage(confirmMessage));
      scrollToBottom();

      // Atualiza a sidebar
      await updateGemsSidebar();
      
      // Carrega o histórico do GEM ativado
      await loadHistory();
    } else {
      console.error('Erro ao ativar GEM:', data.error);
    }
  } catch (error) {
    console.error('Erro ao ativar GEM:', error);
  }
};

// Exporta função para ser usada em outros lugares
window.updateGemsSidebar = updateGemsSidebar;

// Gerencia visibilidade do input wrapper
const inputWrapper = document.getElementById('input-wrapper');
let journeyStarted = false;

const showInputWrapper = () => {
  if (inputWrapper && !journeyStarted) {
    inputWrapper.classList.remove('hidden');
    journeyStarted = true;
    textarea.focus();
  }
};

const hideInputWrapper = () => {
  if (inputWrapper) {
    inputWrapper.classList.add('hidden');
  }
};

// Inicializa a sidebar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
  // Esconde input wrapper inicialmente
  hideInputWrapper();

  createGemsSidebar();
  updateGemsSidebar().then(loadHistory).then(() => {
    updateCompleteButton();
    // Se já tem histórico, mostra o input
    if (chatHistory.children.length > 1) {
      showInputWrapper();
    }
  });
});

// Cria o botão mobile
createSidebarButton();

// Update the complete button after loading history and when GEMs sidebar is updated
window.updateGemsSidebar = async () => {
  try {
    const response = await fetch('/api/gems');
    const data = await response.json();

    const gemsList = document.getElementById('gems-list');
    if (!gemsList) return;

    window.gemsInfo = data;

    // ... existing code for updating gems list ...
    // (keeping the existing implementation of updateGemsSidebar)
    
    // After updating the sidebar, also update the complete button
    updateCompleteButton();

    return data;

  } catch (error) {
    console.error('Erro ao carregar GEMs:', error);
    const gemsList = document.getElementById('gems-list');
    if (gemsList) {
      gemsList.innerHTML = '<div class="gems-sidebar__error">Erro ao carregar GEMs</div>';
    }
  }
};

// Adiciona botão para abrir sidebar (mobile)
const createSidebarButton = () => {
  const btn = document.createElement('button');
  btn.className = 'gems-sidebar-btn';
  btn.id = 'open-sidebar-btn';
  btn.title = 'Ver GEMs disponíveis';
  btn.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
  `;
  document.body.appendChild(btn);

  btn.addEventListener('click', () => {
    const sidebar = document.getElementById('gems-sidebar');
    sidebar?.classList.toggle('gems-sidebar--collapsed');
  });
};

let historyLoaded = false;

const appendConversationHistory = (history, gemId) => {
  if (!Array.isArray(history)) {
    return;
  }

  const gemsMap = new Map();
  if (window.gemsInfo?.gems) {
    window.gemsInfo.gems.forEach((gem) => {
      gemsMap.set(gem.id, gem);
    });
  }

  let pendingUser = null;

  history.forEach((entry) => {
    if (!entry || !entry.role) {
      return;
    }

    if (entry.role === 'user') {
      pendingUser = entry.content || '';
    } else if (entry.role === 'assistant') {
      const gemInfo = gemsMap.get(gemId);
      const payload = {
        message: pendingUser || '',
        answer: entry.content || '',
        gem_name: gemInfo?.name || null,
        is_orchestrator: false,
        error: '',
      };
      chatHistory.appendChild(buildMessage(payload));
      pendingUser = null;
    }
  });
};

const loadHistory = async () => {
  if (historyLoaded) {
    return;
  }

  try {
    const response = await fetch('/api/history');
    if (!response.ok) {
      return;
    }

    const data = await response.json();
    const { conversations, current_gem: currentGem, active_history: activeHistory, completed_gems: completedGems } = data;

    if (completedGems && completedGems.length) {
      completedGems.forEach((gemId) => {
        appendConversationHistory(conversations?.[gemId], gemId);
      });
    }

    if (currentGem && activeHistory) {
      appendConversationHistory(activeHistory, currentGem);
    }

    if (chatHistory.children.length && emptyState) {
      emptyState.remove();
    }

    if (chatHistory.children.length) {
      scrollToBottom();
    }

    historyLoaded = true;

  } catch (error) {
    console.error('Erro ao carregar histórico:', error);
  }
};
