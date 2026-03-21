"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const onGoogleSignIn = async () => {
    setError(null);
    setLoading(true);
    try {
      const supabase = createClient();
      const redirectTo = `${window.location.origin}/auth/callback`;
      const { error: signInError } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo }
      });
      if (signInError) {
        setError(signInError.message);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "로그인 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: 20 }}>
      <section className="card" style={{ width: "min(560px, 100%)" }}>
        <span className="badge">Step 1. Web UI</span>
        <h1 className="title" style={{ marginTop: 14 }}>
          구글 계정으로 로그인
        </h1>
        <p className="subtitle">
          로그인 후 API 키 입력 페이지와 동작 상태 대시보드를 사용할 수 있습니다.
        </p>

        <div style={{ marginTop: 24 }} className="stack">
          <button className="button" onClick={onGoogleSignIn} disabled={loading}>
            {loading ? "구글 로그인 이동 중..." : "Google로 로그인"}
          </button>
          {error && <p className="error">{error}</p>}
          <p className="muted">
            Supabase Google OAuth가 먼저 설정되어 있어야 동작합니다.
          </p>
        </div>
      </section>
    </main>
  );
}
