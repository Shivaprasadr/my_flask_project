import React, { createContext, useState, useEffect } from "react";
import Keycloak from "keycloak-js";

const KeycloakContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const keycloakInstance = Keycloak({
      url: process.env.VITE_KEYCLOAK_URL,
      realm: process.env.VITE_KEYCLOAK_REALM,
      clientId: process.env.VITE_KEYCLOAK_CLIENT,
    });

    keycloakInstance
      .init({ onLoad: "login-required" })
      .then((auth) => {
        setKeycloak(keycloakInstance);
        setAuthenticated(auth);
      })
      .catch((err) => console.error("Keycloak init failed", err));
  }, []);

  return (
    <KeycloakContext.Provider value={{ keycloak, authenticated }}>
      {children}
    </KeycloakContext.Provider>
  );
};

export default KeycloakContext;
