"use client";

import { useEffect, useState } from "react";
import { getMySettings, syncCurrentUser } from "@/lib/backend/api";

export function LocalSettingsStatusCard() {
  const [summary, setSummary] = useState("확인 중...");

  useEffect(() => {
    const run = async () => {
      try {
        await syncCurrentUser();
        const settings = await getMySettings();
        const filledCount = [
          settings.has_notion_token,
          Boolean(settings.notion_page_id),
          settings.has_school_api_key,
          settings.has_gemini_api_key
        ].filter(Boolean).length;
        const updated = settings.updated_at
          ? ` (마지막 저장: ${new Date(settings.updated_at).toLocaleString()})`
          : "";
        setSummary(`${filledCount}/4 항목 입력됨${updated}`);
      } catch (error) {
        setSummary(error instanceof Error ? `조회 실패: ${error.message}` : "조회 실패");
      }
    };
    run();
  }, []);

  return (
    <article className="card">
      <h2 style={{ marginTop: 0, marginBottom: 8 }}>연동 키 입력 상태</h2>
      <p className="subtitle">{summary}</p>
      <p className="muted" style={{ marginTop: 8 }}>
        2단계 기준으로 백엔드 암호화 저장 상태를 표시합니다.
      </p>
    </article>
  );
}
