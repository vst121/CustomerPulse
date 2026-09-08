import type { Metadata } from "next";
import "./globals.css";

import Sidebar from "@/components/layout/Sidebar";
import { ThemeProvider } from "@/components/layout/ThemeProvider";

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
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased dark:bg-slate-950 dark:text-slate-100">
        <ThemeProvider>
          <div className="flex min-h-screen">
            <Sidebar />

            <div className="min-w-0 flex-1">{children}</div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
