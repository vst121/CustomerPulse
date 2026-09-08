import type { Metadata } from "next";
import "./globals.css";

import Sidebar from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "Customer Pulse",
  description: "AI-powered Customer Lifecycle & Value Management Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <div className="flex min-h-screen">
          <Sidebar />

          <div className="min-w-0 flex-1">{children}</div>
        </div>
      </body>
    </html>
  );
}