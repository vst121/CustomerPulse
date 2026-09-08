"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const isDashboard = pathname === "/";
  const isCustomers = pathname.startsWith("/customers");

  return (
    <aside className="w-64 shrink-0 border-r border-slate-200 bg-white">
      <div className="flex h-16 items-center border-b border-slate-200 px-6">
        <h1 className="text-xl font-bold tracking-tight text-slate-900">
          CustomerPulse
        </h1>
      </div>

      <nav className="space-y-1 p-4">
        <Link
          href="/"
          className={`flex items-center rounded-lg px-4 py-3 text-sm font-medium ${
            isDashboard
              ? "bg-slate-100 text-slate-900"
              : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          }`}
        >
          Dashboard
        </Link>

        <Link
          href="/customers"
          className={`flex items-center rounded-lg px-4 py-3 text-sm font-medium ${
            isCustomers
              ? "bg-slate-100 text-slate-900"
              : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          }`}
        >
          Customers
        </Link>
      </nav>
    </aside>
  );
}
