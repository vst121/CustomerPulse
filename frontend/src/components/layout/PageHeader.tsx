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
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="flex min-h-16 items-center justify-between gap-4 px-8 py-4">
        <div>
          <h1 className="text-lg font-semibold text-slate-900">{title}</h1>

          {description && (
            <p className="mt-1 text-sm text-slate-500">{description}</p>
          )}
        </div>

        <div className="flex items-center gap-4">
          {action && <div>{action}</div>}

          <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-700">
              VS
            </div>

            <div className="hidden sm:block">
              <p className="text-sm font-medium text-slate-900">Vahid Saadat</p>

              <p className="text-xs text-slate-500">Administrator</p>
            </div>
          </div>

          <button
            type="button"
            aria-label="Switch theme"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 transition hover:bg-slate-50 hover:text-slate-900"
          >
            <span aria-hidden="true" className="text-base">
              ☀
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
