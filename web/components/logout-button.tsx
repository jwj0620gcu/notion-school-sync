"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";

export function LogoutButton() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const onSignOut = async () => {
    setLoading(true);
    const supabase = createClient();
    await supabase.auth.signOut();
    router.replace("/login");
    router.refresh();
    setLoading(false);
  };

  return (
    <button className="button secondary" onClick={onSignOut} disabled={loading}>
      {loading ? "로그아웃 중..." : "로그아웃"}
    </button>
  );
}
