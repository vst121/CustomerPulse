import Link from "next/link";
import MetricCard from "@/components/ui/MetricCard";

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
          <Link
            href="/"
            className="flex items-center rounded-lg bg-slate-100 px-4 py-3 text-sm font-medium text-slate-900"
          >
            Dashboard
          </Link>

          <Link
            href="/customers"
            className="flex items-center rounded-lg px-4 py-3 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Customers
          </Link>

          <Link
            href="/transactions"
            className="flex items-center rounded-lg px-4 py-3 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Transactions
          </Link>

          <Link
            href="/recommendations"
            className="flex items-center rounded-lg px-4 py-3 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          >
            Recommendations
          </Link>
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
            <MetricCard
              title="Lifecycle Stage"
              value={customer.lifecycle_stage}
            />

            <MetricCard title="Customer ID" value={customer.id} />

            <MetricCard title="Email" value={customer.email} />

            <MetricCard
              title="Customer Since"
              value={new Date(customer.created_at).toLocaleDateString()}
            />
          </div>{" "}
        </div>
      </section>
    </main>
  );
}
