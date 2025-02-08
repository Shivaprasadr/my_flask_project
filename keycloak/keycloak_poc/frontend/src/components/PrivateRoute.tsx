import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import KeycloakContext from "./AuthProvider";

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { authenticated } = useContext(KeycloakContext);

  if (!authenticated) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};

export default PrivateRoute;
