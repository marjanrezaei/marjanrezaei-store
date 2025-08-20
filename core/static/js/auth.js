const Auth = {
  setTokens(access, refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
  },

  getAccessToken() {
    return localStorage.getItem("access_token");
  },

  getRefreshToken() {
    return localStorage.getItem("refresh_token");
  },

  setUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
  },

  getUser() {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  },

  clear() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  },

  async refreshToken() {
    const refresh = this.getRefreshToken();
    if (!refresh) return null;

    const response = await fetch("/api/accounts/token/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh })
    });

    if (response.ok) {
      const data = await response.json();
      this.setTokens(data.access, refresh);
      return data.access;
    } else {
      this.clear();
      return null;
    }
  }
};

