import { useEffect, useState } from "react";

import { DashboardPage } from "./pages/DashboardPage";
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import type { Route } from "./types";

function getRoute(): Route {
  const hash = window.location.hash.slice(1);

  if (hash === "login" || hash === "app") {
    return hash;
  }

  return "landing";
}

export function App() {
  const [route, setRoute] = useState<Route>(getRoute);

  useEffect(() => {
    function handleRouteChange() {
      setRoute(getRoute());
    }

    window.addEventListener("hashchange", handleRouteChange);

    return () => {
      window.removeEventListener("hashchange", handleRouteChange);
    };
  }, []);

  function navigate(nextRoute: Route) {
    window.location.hash = nextRoute;
    setRoute(nextRoute);
  }

  if (route === "app") {
    return <DashboardPage onLogout={() => navigate("landing")} />;
  }

  if (route === "login") {
    return (
      <LoginPage
        onBack={() => navigate("landing")}
        onDemo={() => navigate("app")}
      />
    );
  }

  return (
    <LandingPage
      onStart={() => navigate("login")}
      onLogin={() => navigate("login")}
    />
  );
}
