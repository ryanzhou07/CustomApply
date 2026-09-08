import { useState } from "react";
import { createClient } from "@supabase/supabase-js";

import { Logo } from "../components/Logo";

interface LoginPageProps {
  onBack: () => void;
  onDemo: () => void;
}

export function LoginPage({ onBack, onDemo }: LoginPageProps) {
  const [loading, setLoading] = useState(false);

  async function signInWithGoogle() {
    const url = import.meta.env.VITE_SUPABASE_URL;
    const key =
      import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY ??
      import.meta.env.VITE_SUPABASE_ANON_KEY;

    if (!url || !key) {
      setLoading(true);
      window.setTimeout(onDemo, 650);
      return;
    }

    const supabase = createClient(url, key);

    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}#app`,
      },
    });
  }

  return (
    <div className="login-page">
      <button className="back" onClick={onBack}>
        ← Back
      </button>

      <div className="login-art">
        <Logo light />

        <div>
          <p>
            “A job search should feel like progress,
            <br />
            not paperwork.”
          </p>
          <small>Built to help you focus on what comes next.</small>
        </div>
      </div>

      <div className="login-panel">
        <div className="login-card">
          <Logo />

          <div className="login-copy">
            <p className="kicker">WELCOME TO YOUR WORKSPACE</p>
            <h1>Let’s get to work.</h1>
            <p>
              Sign in to organize your search and keep every opportunity moving
              forward.
            </p>
          </div>

          <button
            className="google-button"
            onClick={signInWithGoogle}
            disabled={loading}
          >
            <span className="google-g">G</span>
            {loading ? "Opening your workspace…" : "Continue with Google"}
          </button>

          <div className="divider">
            <span />
            secure sign in
            <span />
          </div>

          <p className="legal">
            By continuing, you agree to our Terms of Service and Privacy Policy.
          </p>
        </div>
      </div>
    </div>
  );
}
