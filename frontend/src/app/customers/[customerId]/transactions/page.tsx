"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import Badge from "@/components/ui/Badge";
import Card, { CardContent, CardHeader } from "@/components/ui/Card";
import ErrorState from "@/components/ui/ErrorState";
import LoadingState from "@/components/ui/LoadingState";
import { getCustomer } from "@/services/api/customers";
import { getCustomerTransactions } from "@/services/api/transactions";
import type { Customer } from "@/types/customer";
import type {
  Transaction,
  TransactionCategory,
  TransactionStatus,
} from "@/types/transaction";

const PAGE_SIZE = 10;

function formatAmount(amount: string, currency: string): string {
  const value = Number(amount);

  if (Number.isNaN(value)) {
    return `${amount} ${currency}`;
  }

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(value);
}

function formatDate(timestamp: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(timestamp));
}

function getStatusClassName(status: TransactionStatus): string {
  switch (status) {
    case "COMPLETED":
      return "bg-green-100 text-green-700";

    case "PENDING":
      return "bg-yellow-100 text-yellow-700";

    case "FAILED":
      return "bg-red-100 text-red-700";

    case "REVERSED":
      return "bg-slate-200 text-slate-700";
  }
}

function getCategoryLabel(category: TransactionCategory): string {
  return category.charAt(0) + category.slice(1).toLowerCase();
}

export default function CustomerTransactionsPage({
  params,
}: {
  params: Promise<{ customerId: string }>;
}) {
  const [customer, setCustomer] = useState<Customer | null>(null);

  const [transactions, setTransactions] = useState<Transaction[]>([]);

  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoading(true);
        setError(null);

        const { customerId } = await params;

        const [customerResponse, transactionResponse] = await Promise.all([
          getCustomer(customerId),
          getCustomerTransactions(customerId, {
            page,
            page_size: PAGE_SIZE,
          }),
        ]);

        if (cancelled) {
          return;
        }

        setCustomer(customerResponse);
        setTransactions(transactionResponse.items);
        setTotal(transactionResponse.total);
      } catch (err) {
        if (cancelled) {
          return;
        }

        setError(
          err instanceof Error ? err.message : "Failed to load transactions.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadData();

    return () => {
      cancelled = true;
    };
  }, [params, page]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  if (loading) {
    return <LoadingState message="Loading transactions..." />;
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <ErrorState title="Unable to load transactions" message={error} />
      </main>
    );
  }

  if (!customer) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <ErrorState
          title="Customer not found"
          message="The requested customer could not be found."
        />
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <div className="flex items-center gap-3">
            <Link
              href="/customers"
              className="text-sm font-medium text-slate-500 hover:text-slate-900"
            >
              Customers
            </Link>

            <span className="text-slate-300">/</span>

            <Link
              href={`/customers/${customer.id}`}
              className="text-sm font-medium text-slate-500 hover:text-slate-900"
            >
              {customer.first_name} {customer.last_name}
            </Link>

            <span className="text-slate-300">/</span>

            <span className="text-sm text-slate-500">Transactions</span>
          </div>

          <div className="mt-4 flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                Transactions
              </h1>

              <p className="mt-1 text-sm text-slate-500">
                Transaction history for {customer.first_name}{" "}
                {customer.last_name}.
              </p>
            </div>

            <Link
              href={`/customers/${customer.id}/transactions/new`}
              className="rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-800"
            >
              Add Transaction
            </Link>
          </div>
        </div>
      </header>

      <section className="p-8">
        <div className="mx-auto max-w-7xl">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="font-semibold text-slate-900">
                    Transaction History
                  </h2>

                  <p className="mt-1 text-sm text-slate-500">
                    {total} transaction
                    {total === 1 ? "" : "s"}
                  </p>
                </div>
              </div>
            </CardHeader>

            <CardContent className="p-0">
              {transactions.length === 0 ? (
                <div className="px-6 py-12 text-center">
                  <p className="font-medium text-slate-900">
                    No transactions found
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    This customer does not have any transactions yet.
                  </p>
                </div>
              ) : (
                <>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                      <thead className="border-b border-slate-200 bg-slate-50">
                        <tr>
                          <th className="px-6 py-3 font-medium text-slate-500">
                            Date
                          </th>

                          <th className="px-6 py-3 font-medium text-slate-500">
                            Category
                          </th>

                          <th className="px-6 py-3 font-medium text-slate-500">
                            Amount
                          </th>

                          <th className="px-6 py-3 font-medium text-slate-500">
                            Status
                          </th>

                          <th className="px-6 py-3 font-medium text-slate-500">
                            Transaction ID
                          </th>
                        </tr>
                      </thead>

                      <tbody className="divide-y divide-slate-100">
                        {transactions.map((transaction) => (
                          <tr
                            key={transaction.id}
                            className="hover:bg-slate-50"
                          >
                            <td className="whitespace-nowrap px-6 py-4 text-slate-700">
                              {formatDate(transaction.timestamp)}
                            </td>

                            <td className="px-6 py-4">
                              <span className="font-medium text-slate-900">
                                {getCategoryLabel(transaction.category)}
                              </span>
                            </td>

                            <td className="whitespace-nowrap px-6 py-4 font-medium text-slate-900">
                              {formatAmount(
                                transaction.amount,
                                transaction.currency,
                              )}
                            </td>

                            <td className="px-6 py-4">
                              <Badge
                                className={getStatusClassName(
                                  transaction.status,
                                )}
                              >
                                {transaction.status}
                              </Badge>
                            </td>

                            <td className="px-6 py-4 font-mono text-xs text-slate-500">
                              {transaction.id}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <div className="flex items-center justify-between border-t border-slate-200 px-6 py-4">
                    <p className="text-sm text-slate-500">
                      Page {page} of {Math.max(totalPages, 1)}
                    </p>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        disabled={page === 1}
                        onClick={() =>
                          setPage((current) => Math.max(current - 1, 1))
                        }
                        className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        Previous
                      </button>

                      <button
                        type="button"
                        disabled={page >= totalPages || totalPages === 0}
                        onClick={() =>
                          setPage((current) =>
                            Math.min(current + 1, totalPages),
                          )
                        }
                        className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>
      </section>
    </main>
  );
}
