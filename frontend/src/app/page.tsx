export default function HomePage() {
  return (
    <main className="flex min-h-screen">
      <aside className="w-64 border-r border-slate-200 bg-white">
        <div className="flex h-16 items-center border-b border-slate-200 px-6">
          <h1 className="text-xl font-bold tracking-tight text-slate-900">
            CustomerPulse
          </h1>
        </div>

        <nav className="space-y-1 p-4">
          <a
            href="/"
            className="flex items-center rounded-lg bg-slate-100 px-4 py-3 text-sm font-medium text-slate-900"
          >
            Dashboard
          </a>

          <a
            href="/customers"
            className="flex items-center rounded-lg px-4 py-3 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Customers
          </a>

          <a
            href="/transactions"
            className="flex items-center rounded-lg px-4 py-3 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Transactions
          </a>

          <a
            href="/recommendations"
            className="flex items-center rounded-lg px-4 py-3 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Recommendations
          </a>
        </nav>
      </aside>

      <section className="flex-1">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-8">
          <div>
            <h2 className="text-lg font-semibold">Dashboard</h2>
            <p className="text-sm text-slate-500">
              Customer lifecycle and value management
            </p>
          </div>

          <div className="text-sm text-slate-600">CustomerPulse</div>
        </header>

        <div className="p-8">
          <div className="mb-8">
            <h3 className="text-2xl font-bold tracking-tight">
              Welcome to CustomerPulse
            </h3>

            <p className="mt-2 text-slate-600">
              Understand your customers, predict their behavior, and choose the
              next best action.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            <DashboardCard
              title="Customers"
              value="—"
              description="Total customers"
            />

            <DashboardCard
              title="Active"
              value="—"
              description="Active customers"
            />

            <DashboardCard
              title="Churn Risk"
              value="—"
              description="High-risk customers"
            />

            <DashboardCard
              title="Recommendations"
              value="—"
              description="Pending actions"
            />
          </div>
        </div>
      </section>
    </main>
  );
}

type DashboardCardProps = {
  title: string;
  value: string;
  description: string;
};

function DashboardCard({ title, value, description }: DashboardCardProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{title}</p>

      <p className="mt-3 text-3xl font-bold tracking-tight">{value}</p>

      <p className="mt-2 text-sm text-slate-500">{description}</p>
    </div>
  );
}
