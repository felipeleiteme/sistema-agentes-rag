/**
 * Gerenciamento de autenticação
 */

class AuthManager {
  constructor() {
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
    this.userId = localStorage.getItem('user_id');
    this.userEmail = localStorage.getItem('user_email');
  }

  isAuthenticated() {
    return !!this.accessToken;
  }

  getAuthHeader() {
    if (!this.accessToken) return {};
    return {
      'Authorization': `Bearer ${this.accessToken}`
    };
  }

  async checkAuth() {
    if (!this.isAuthenticated()) {
      // Redirecionar para login se não estiver em uma página pública
      const publicPages = ['/login', '/register'];
      if (!publicPages.includes(window.location.pathname)) {
        window.location.href = '/login';
      }
      return false;
    }

    // Verificar se token é válido
    try {
      const response = await fetch('/api/auth/me', {
        headers: this.getAuthHeader()
      });

      if (!response.ok) {
        // Token inválido, fazer logout
        this.logout();
        return false;
      }

      const data = await response.json();
      this.userId = data.user_id;
      this.userEmail = data.email;

      return data;
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error);
      return false;
    }
  }

  logout() {
    // Limpar localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');

    this.accessToken = null;
    this.refreshToken = null;
    this.userId = null;
    this.userEmail = null;

    // Redirecionar para login
    window.location.href = '/login';
  }

  getUserInfo() {
    return {
      userId: this.userId,
      email: this.userEmail
    };
  }
}

// Criar instância global
window.authManager = new AuthManager();

export default AuthManager;
