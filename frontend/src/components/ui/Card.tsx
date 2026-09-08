import type { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  className?: string;
};

export default function Card({
  children,
  className = "",
}: CardProps) {
  return (
    <div
      className={`rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900 ${className}`}
    >
      {children}
    </div>
  );
}

type CardHeaderProps = {
  children: ReactNode;
};

export function CardHeader({ children }: CardHeaderProps) {
  return (
    <div className="border-b border-slate-200 px-6 py-4 dark:border-slate-800">
      {children}
    </div>
  );
}

type CardContentProps = {
  children: ReactNode;
  className?: string;
};

export function CardContent({
  children,
  className = "",
}: CardContentProps) {
  return (
    <div className={`p-6 ${className}`}>
      {children}
    </div>
  );
}