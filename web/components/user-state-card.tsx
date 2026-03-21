"use client";

import { useEffect, useState } from "react";
import { getMyDashboard, syncCurrentUser } from "@/lib/backend/api";

function formatTime(input: string | null) {
  if (!input) {
    return "-";
  }
  return new Date(input).toLocaleString();
}

export function UserStateCard() {
  const [message, setMessage] = useState("확인 중...");

  useEffect(() => {
    const run = async () => {
      try {
        await syncCurrentUser();
        const data = await getMyDashboard();
        if (!data.state) {
          setMessage("스케줄러 실행 이력이 아직 없습니다.");
          return;
        }
        setMessage(
          [
            `최근 상태: ${data.state.last_status ?? "-"}`,
            `10분 체크: ${formatTime(data.state.last_notion_check_at)}`,
            `최근 동기화: ${formatTime(data.state.last_notion_sync_at)}`,
            `주간 리포트: ${formatTime(data.state.last_weekly_report_at)}`,
            `월간 리포트: ${formatTime(data.state.last_monthly_report_at)}`,
            `최근 오류: ${data.state.last_error ?? "-"}`
          ].join("\n")
        );
      } catch (error) {
        setMessage(error instanceof Error ? `조회 실패: ${error.message}` : "조회 실패");
      }
    };
    run();
  }, []);

  return (
    <article className="card">
      <h2 style={{ marginTop: 0, marginBottom: 8 }}>스케줄러 실행 상태</h2>
      <pre
        style={{
          margin: 0,
          whiteSpace: "pre-wrap",
          font: "inherit",
          color: "var(--muted)"
        }}
      >
        {message}
      </pre>
    </article>
  );
}
