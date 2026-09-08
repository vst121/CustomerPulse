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

        {action && <div className="shrink-0">{action}</div>}
      </div>
    </header>
  );
}
