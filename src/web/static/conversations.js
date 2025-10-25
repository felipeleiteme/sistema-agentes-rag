/**
 * Gerenciamento de conversas
 */

class ConversationManager {
  constructor(authManager) {
    this.authManager = authManager;
    this.currentConversationId = null;
  }

  async loadConversations() {
    try {
      const response = await fetch('/api/conversations', {
        headers: this.authManager.getAuthHeader()
      });

      if (!response.ok) throw new Error('Erro ao carregar conversas');

      const data = await response.json();
      return data.conversations || [];
    } catch (error) {
      console.error('Erro ao carregar conversas:', error);
      return [];
    }
  }

  async createConversation() {
    try {
      const response = await fetch('/api/conversations', {
        method: 'POST',
        headers: {
          ...this.authManager.getAuthHeader(),
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Erro ao criar conversa');

      const data = await response.json();
      this.currentConversationId = data.conversation.id;
      return data.conversation;
    } catch (error) {
      console.error('Erro ao criar conversa:', error);
      return null;
    }
  }

  async getConversation(conversationId) {
    try {
      const response = await fetch(`/api/conversations/${conversationId}`, {
        headers: this.authManager.getAuthHeader()
      });

      if (!response.ok) throw new Error('Erro ao carregar conversa');

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erro ao carregar conversa:', error);
      return null;
    }
  }

  async updateConversationTitle(conversationId, title) {
    try {
      const response = await fetch(`/api/conversations/${conversationId}?title=${encodeURIComponent(title)}`, {
        method: 'PUT',
        headers: {
          ...this.authManager.getAuthHeader(),
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Erro ao atualizar conversa');

      const data = await response.json();
      return data.conversation;
    } catch (error) {
      console.error('Erro ao atualizar conversa:', error);
      return null;
    }
  }

  async deleteConversation(conversationId) {
    try {
      const response = await fetch(`/api/conversations/${conversationId}`, {
        method: 'DELETE',
        headers: this.authManager.getAuthHeader()
      });

      if (!response.ok) throw new Error('Erro ao deletar conversa');

      return true;
    } catch (error) {
      console.error('Erro ao deletar conversa:', error);
      return false;
    }
  }

  async saveMessage(conversationId, role, content) {
    try {
      const response = await fetch(`/api/conversations/${conversationId}/messages?role=${role}&content=${encodeURIComponent(content)}`, {
        method: 'POST',
        headers: {
          ...this.authManager.getAuthHeader(),
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Erro ao salvar mensagem');

      const data = await response.json();
      return data.message;
    } catch (error) {
      console.error('Erro ao salvar mensagem:', error);
      return null;
    }
  }

  getCurrentConversationId() {
    return this.currentConversationId;
  }

  setCurrentConversationId(id) {
    this.currentConversationId = id;
  }

  async renderConversationsList(containerElement) {
    const conversations = await this.loadConversations();

    if (conversations.length === 0) {
      containerElement.innerHTML = `
        <div style="padding: 1rem; text-align: center; color: #9ca3af;">
          <p>Nenhuma conversa ainda</p>
          <p style="font-size: 0.875rem; margin-top: 0.5rem;">Inicie uma nova conversa</p>
        </div>
      `;
      return;
    }

    containerElement.innerHTML = conversations.map(conv => {
      const date = new Date(conv.updated_at || conv.created_at);
      const dateStr = date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });

      return `
        <div class="conversation-item" data-id="${conv.id}">
          <div class="conversation-info">
            <div class="conversation-title">${conv.title}</div>
            <div class="conversation-date">${dateStr}</div>
          </div>
          <button class="conversation-delete" data-id="${conv.id}" title="Deletar conversa">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M6 6L18 18M6 18L18 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      `;
    }).join('');

    // Adicionar event listeners
    containerElement.querySelectorAll('.conversation-item').forEach(item => {
      item.addEventListener('click', async (e) => {
        if (e.target.closest('.conversation-delete')) return;

        const convId = item.dataset.id;
        await this.loadConversationMessages(convId);
      });
    });

    containerElement.querySelectorAll('.conversation-delete').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.stopPropagation();

        if (!confirm('Deseja realmente deletar esta conversa?')) return;

        const convId = btn.dataset.id;
        const success = await this.deleteConversation(convId);

        if (success) {
          await this.renderConversationsList(containerElement);
        }
      });
    });
  }

  async loadConversationMessages(conversationId) {
    const data = await this.getConversation(conversationId);

    if (!data) return;

    this.currentConversationId = conversationId;

    // Limpar chat
    const chatHistory = document.getElementById('chat-history');
    const emptyState = document.getElementById('empty-state');

    if (emptyState) {
      emptyState.style.display = 'none';
    }

    chatHistory.innerHTML = '';

    // Renderizar mensagens
    data.messages.forEach(msg => {
      this.appendMessageToChat(msg.role, msg.content);
    });
  }

  appendMessageToChat(role, content) {
    const chatHistory = document.getElementById('chat-history');
    const emptyState = document.getElementById('empty-state');

    if (emptyState) {
      emptyState.style.display = 'none';
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message message--${role}`;
    messageDiv.innerHTML = `
      <div class="message__content">
        <div class="message__text">${this.formatMessage(content)}</div>
      </div>
    `;

    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  formatMessage(text) {
    // Converter markdown básico para HTML
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  }
}

export default ConversationManager;
