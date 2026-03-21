import { BackendStatusCard } from "@/components/backend-status";
import { LocalSettingsStatusCard } from "@/components/local-settings-status";
import { SchedulerControlsCard } from "@/components/scheduler-controls-card";
import { UserStateCard } from "@/components/user-state-card";

export default function DashboardPage() {
  return (
    <section className="stack">
      <article className="card">
        <h1 className="title" style={{ marginBottom: 10 }}>
          동작 상태 대시보드
        </h1>
        <p className="subtitle">
          스케줄러 실행 상태와 최근 동기화 이력을 백엔드에서 조회합니다.
        </p>
      </article>

      <div className="grid-2">
        <BackendStatusCard />
        <LocalSettingsStatusCard />
        <UserStateCard />
        <SchedulerControlsCard />
      </div>
    </section>
  );
}
