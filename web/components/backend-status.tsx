"use client";

import { useEffect, useState } from "react";

type HealthResponse = {
  status?: string;
  detail?: string;
  scheduler_running?: boolean;
  timestamp?: string;
};

export function BackendStatusCard() {
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("확인 중...");

  useEffect(() => {
    const backendBase = process.env.NEXT_PUBLIC_BACKEND_API_URL;
    if (!backendBase) {
      setMessage("NEXT_PUBLIC_BACKEND_API_URL 미설정");
      setLoading(false);
      return;
    }

    const run = async () => {
      try {
        const res = await fetch(`${backendBase}/health`, { cache: "no-store" });
        if (!res.ok) {
          setMessage(`백엔드 응답 오류 (${res.status})`);
          return;
        }
        const data = (await res.json()) as HealthResponse;
        if (!data.status) {
          setMessage("정상");
          return;
        }
        const scheduler = data.scheduler_running ? "ON" : "OFF";
        const timeText = data.timestamp ? new Date(data.timestamp).toLocaleString() : "-";
        setMessage(`정상 (${data.status}) / Scheduler: ${scheduler} / ${timeText}`);
      } catch {
        setMessage("백엔드 연결 실패 (FastAPI 미실행 또는 CORS 미설정)");
      } finally {
        setLoading(false);
      }
    };

    run();
  }, []);

  return (
    <article className="card">
      <h2 style={{ marginTop: 0, marginBottom: 8 }}>백엔드 상태</h2>
      <p className="subtitle">
        {loading ? "상태 확인 중..." : message}
      </p>
    </article>
  );
}
