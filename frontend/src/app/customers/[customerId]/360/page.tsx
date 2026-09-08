"use client";

import { useEffect, useState } from "react";

import { getCustomer360 } from "@/services/api/customers";
import type { Customer360 } from "@/types/customer360";
import Badge from "@/components/ui/Badge";
import TransactionTrendChart from "@/components/transactions/TransactionTrendChart";

type Customer360PageProps = {
  params: Promise<{
    customerId: string;
  }>;
};

export default function Customer360Page({ params }: Customer360PageProps) {
  const [customer, setCustomer] = useState<Customer360 | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCustomer360() {
      try {
        const { customerId } = await params;

        const response = await getCustomer360(customerId);

        setCustomer(response);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load customer 360.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadCustomer360();
  }, [params]);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        {" "}
        <p className="text-sm text-slate-500">Loading customer 360...</p>{" "}
      </main>
    );
  }

  if (error || !customer) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        {" "}
        <div className="rounded-xl border border-red-200 bg-red-50 p-6">
          {" "}
          <h1 className="font-semibold text-red-900">
            Unable to load customer 360{" "}
          </h1>
          <p className="mt-2 text-sm text-red-700">
            {error ?? "Customer not found."}
          </p>
        </div>
      </main>
    );
  }

  const transactionTrend = buildTransactionTrend(customer.transactions);

  const transactionCurrency =
    customer.transactions.find(
      (transaction) => transaction.status === "COMPLETED",
    )?.currency ?? "EUR";

  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}

      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <a
            href={`/customers/${customer.id}`}
            className="text-sm font-medium text-slate-500 hover:text-slate-900"
          >
            ← Customer Profile
          </a>

          <div className="mt-4 flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                {customer.first_name} {customer.last_name}
              </h1>

              <p className="mt-1 text-sm text-slate-500">Customer 360</p>
            </div>

            <Badge className="px-4 py-2 text-sm">
              {customer.lifecycle_stage}
            </Badge>
          </div>
        </div>
      </header>

      <section className="p-8">
        {/* KPI Cards */}

        <div className="grid gap-6 md:grid-cols-3">
          <MetricCard
            title="Customer Value"
            value={`€${customer.value.total_spend}`}
            description="Total spend"
          />

          <MetricCard
            title="Transactions"
            value={String(customer.value.transaction_count)}
            description="Completed transactions"
          />

          <MetricCard
            title="Customer Score"
            value={customer.score.score}
            description="Current customer score"
          />
        </div>

        {/* Customer information */}

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <section className="rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-200 px-6 py-4">
              <h2 className="font-semibold text-slate-900">
                Customer Information
              </h2>
            </div>

            <div className="space-y-4 p-6">
              <InfoRow
                label="Name"
                value={`${customer.first_name} ${customer.last_name}`}
              />

              <InfoRow label="Email" value={customer.email} />

              <InfoRow label="Lifecycle" value={customer.lifecycle_stage} />

              <InfoRow
                label="Customer Since"
                value={new Date(customer.created_at).toLocaleDateString()}
              />
            </div>
          </section>

          {/* Recommendations */}

          <section className="rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-200 px-6 py-4">
              <h2 className="font-semibold text-slate-900">Recommendations</h2>

              <p className="mt-1 text-sm text-slate-500">
                Current recommended actions.
              </p>
            </div>

            <div className="divide-y divide-slate-100">
              {customer.recommendations.map((recommendation) => (
                <div key={recommendation.id} className="p-6">
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                    {recommendation.type}
                  </span>

                  <p className="mt-3 text-sm text-slate-600">
                    {recommendation.reason}
                  </p>
                </div>
              ))}

              {customer.recommendations.length === 0 && (
                <p className="p-6 text-sm text-slate-500">
                  No recommendations available.
                </p>
              )}
            </div>
          </section>
        </div>

        {/* Transaction Activity */}

        <section className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">
              Transaction Activity
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Monthly customer spending based on completed transactions.
            </p>
          </div>

          <div className="p-6">
            <TransactionTrendChart
              data={transactionTrend}
              currency={transactionCurrency}
            />
          </div>
        </section>

        {/* Transactions */}

        <section className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">
              Recent Transactions
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Customer transaction history.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-200 bg-slate-50">
                <tr>
                  <th className="px-6 py-3 font-medium text-slate-500">Date</th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Category
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Amount
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Currency
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Status
                  </th>
                </tr>
              </thead>

              <tbody>
                {customer.transactions.map((transaction) => (
                  <tr
                    key={transaction.id}
                    className="border-b border-slate-100 last:border-0"
                  >
                    <td className="px-6 py-4 text-slate-600">
                      {new Date(transaction.timestamp).toLocaleDateString()}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      {transaction.category}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      {transaction.amount}
                    </td>

                    <td className="px-6 py-4 text-slate-600">
                      {transaction.currency}
                    </td>

                    <td className="px-6 py-4">
                      <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                        {transaction.status}
                      </span>
                    </td>
                  </tr>
                ))}

                {customer.transactions.length === 0 && (
                  <tr>
                    <td
                      colSpan={5}
                      className="px-6 py-12 text-center text-slate-500"
                    >
                      No transactions found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </section>
    </main>
  );
}

type MetricCardProps = {
  title: string;
  value: string;
  description: string;
};

function MetricCard({ title, value, description }: MetricCardProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      {" "}
      <p className="text-sm font-medium text-slate-500">{title}</p>
      <p className="mt-3 text-3xl font-bold tracking-tight text-slate-900">
        {value}
      </p>
      <p className="mt-2 text-sm text-slate-500">{description}</p>
    </div>
  );
}

type InfoRowProps = {
  label: string;
  value: string;
};

function InfoRow({ label, value }: InfoRowProps) {
  return (
    <div className="flex items-center justify-between gap-4">
      {" "}
      <span className="text-sm text-slate-500">{label}</span>
      <span className="text-right text-sm font-medium text-slate-900">
        {value}
      </span>
    </div>
  );
}

function buildTransactionTrend(transactions: Customer360["transactions"]) {
  const monthlyTotals = new Map<
    string,
    {
      amount: number;
      timestamp: number;
    }
  >();

  for (const transaction of transactions) {
    if (transaction.status !== "COMPLETED") {
      continue;
    }

    const date = new Date(transaction.timestamp);

    const month = date.toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    });

    const timestamp = new Date(
      date.getFullYear(),
      date.getMonth(),
      1,
    ).getTime();

    const amount = Number(transaction.amount);

    const existing = monthlyTotals.get(month);

    monthlyTotals.set(month, {
      amount: (existing?.amount ?? 0) + amount,
      timestamp,
    });
  }

  return Array.from(monthlyTotals.entries())
    .map(([month, data]) => ({
      month,
      amount: data.amount,
      timestamp: data.timestamp,
    }))
    .sort((a, b) => a.timestamp - b.timestamp)
    .map(({ month, amount }) => ({
      month,
      amount,
    }));
}
