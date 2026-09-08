"use client";

import { useTheme } from "./ThemeProvider";

type PageHeaderProps = {
  title: string;
  description?: string;
  action?: React.ReactNode;
};

export default function PageHeader({
  title,
  description,
  action,
}: PageHeaderProps) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
      <div className="flex min-h-16 items-center justify-between gap-4 px-8 py-4">
        <div>
          <h1 className="text-lg font-semibold text-slate-900 dark:text-white">
            {title}
          </h1>

          {description && (
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              {description}
            </p>
          )}
        </div>

        <div className="flex items-center gap-4">
          {action && <div>{action}</div>}

          <div className="flex items-center gap-3 border-l border-slate-200 pl-4 dark:border-slate-800">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-700 dark:bg-slate-800 dark:text-slate-200">
              VS
            </div>

            <div className="hidden sm:block">
              <p className="text-sm font-medium text-slate-900 dark:text-white">
                Vahid Saadat
              </p>

              <p className="text-xs text-slate-500 dark:text-slate-400">
                Administrator
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={toggleTheme}
            aria-label={`Switch to ${
              theme === "light" ? "dark" : "light"
            } mode`}
            className="flex h-9 w-9 items-center justify-center border-l border-slate-200 text-slate-500 transition-colors hover:bg-slate-50 hover:text-slate-900 dark:border-slate-800 dark:text-slate-400 dark:hover:bg-slate-900 dark:hover:text-white"
          >
            <span aria-hidden="true" className="text-base">
              {theme === "light" ? "☀" : "☾"}
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
