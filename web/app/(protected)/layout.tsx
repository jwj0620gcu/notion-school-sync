import Link from "next/link";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { LogoutButton } from "@/components/logout-button";

export default async function ProtectedLayout({
  children
}: Readonly<{ children: React.ReactNode }>) {
  const supabase = createClient();
  const {
    data: { user }
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <main style={{ minHeight: "100vh", padding: "28px 0 48px" }}>
      <div className="container">
        <header
          className="card"
          style={{
            marginBottom: 18,
            display: "flex",
            gap: 12,
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap"
          }}
        >
          <div style={{ display: "grid", gap: 6 }}>
            <strong>Notion School Sync</strong>
            <span className="muted">{user.email}</span>
          </div>

          <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
            <Link className="button secondary" href="/dashboard">
              대시보드
            </Link>
            <Link className="button secondary" href="/settings">
              API 키 입력
            </Link>
            <LogoutButton />
          </div>
        </header>
        {children}
      </div>
    </main>
  );
}
