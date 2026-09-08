"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import Card, { CardContent, CardHeader } from "@/components/ui/Card";
import ErrorState from "@/components/ui/ErrorState";
import { createTransaction } from "@/services/api/transactions";
import type {
  TransactionCategory,
  TransactionStatus,
} from "@/types/transaction";

const CATEGORIES: TransactionCategory[] = [
  "GROCERIES",
  "RESTAURANT",
  "TRAVEL",
  "SHOPPING",
  "UTILITIES",
  "ENTERTAINMENT",
  "OTHER",
];

const STATUSES: TransactionStatus[] = [
  "PENDING",
  "COMPLETED",
  "FAILED",
  "REVERSED",
];

function createIdempotencyKey(): string {
  return crypto.randomUUID();
}

export default function NewTransactionPage() {
  const router = useRouter();
  const params = useParams<{ customerId: string }>();

  const customerId = params.customerId;

  const [amount, setAmount] = useState("");
  const [currency, setCurrency] = useState("EUR");
  const [category, setCategory] = useState<TransactionCategory>("SHOPPING");
  const [status, setStatus] = useState<TransactionStatus>("COMPLETED");

  const [timestamp, setTimestamp] = useState(() => {
    const now = new Date();

    const offset = now.getTimezoneOffset();
    const localDate = new Date(now.getTime() - offset * 60 * 1000);

    return localDate.toISOString().slice(0, 16);
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      setLoading(true);
      setError(null);

      const transaction = await createTransaction(
        customerId,
        createIdempotencyKey(),
        {
          amount: amount.trim(),
          currency: currency.trim().toUpperCase(),
          category,
          status,
          timestamp: new Date(timestamp).toISOString(),
        },
      );

      router.push(`/customers/${customerId}/transactions`);

      void transaction;
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create transaction.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <header className="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
        <div className="px-8 py-6">
          <div className="flex items-center gap-3">
            <Link
              href={`/customers/${customerId}`}
              className="text-sm font-medium text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
            >
              Customer
            </Link>

            <span className="text-slate-300 dark:text-slate-700">/</span>

            <Link
              href={`/customers/${customerId}/transactions`}
              className="text-sm font-medium text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
            >
              Transactions
            </Link>

            <span className="text-slate-300 dark:text-slate-700">/</span>

            <span className="text-sm text-slate-500 dark:text-slate-400">
              Add Transaction
            </span>
          </div>

          <h1 className="mt-3 text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            Add Transaction
          </h1>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Create a new transaction for this customer.
          </p>
        </div>
      </header>

      <section className="p-8">
        <div className="mx-auto max-w-2xl">
          <Card>
            <CardHeader>
              <h2 className="font-semibold text-slate-900 dark:text-white">
                Transaction Information
              </h2>

              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Enter the transaction details.
              </p>
            </CardHeader>

            <CardContent>
              {error && (
                <div className="mb-6">
                  <ErrorState
                    title="Unable to create transaction"
                    message={error}
                  />
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <label
                      htmlFor="amount"
                      className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      Amount
                    </label>

                    <input
                      id="amount"
                      type="number"
                      min="0.01"
                      step="0.01"
                      value={amount}
                      onChange={(event) => setAmount(event.target.value)}
                      required
                      className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="currency"
                      className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      Currency
                    </label>

                    <input
                      id="currency"
                      type="text"
                      value={currency}
                      onChange={(event) => setCurrency(event.target.value)}
                      required
                      minLength={3}
                      maxLength={3}
                      className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm uppercase text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                    />
                  </div>
                </div>

                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <label
                      htmlFor="category"
                      className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      Category
                    </label>

                    <select
                      id="category"
                      value={category}
                      onChange={(event) =>
                        setCategory(event.target.value as TransactionCategory)
                      }
                      className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                    >
                      {CATEGORIES.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label
                      htmlFor="status"
                      className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      Status
                    </label>

                    <select
                      id="status"
                      value={status}
                      onChange={(event) =>
                        setStatus(event.target.value as TransactionStatus)
                      }
                      className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                    >
                      {STATUSES.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="timestamp"
                    className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                  >
                    Transaction Date & Time
                  </label>

                  <input
                    id="timestamp"
                    type="datetime-local"
                    value={timestamp}
                    onChange={(event) => setTimestamp(event.target.value)}
                    required
                    className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  <Link
                    href={`/customers/${customerId}/transactions`}
                    className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    Cancel
                  </Link>

                  <button
                    type="submit"
                    disabled={loading}
                    className="rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
                  >
                    {loading ? "Creating..." : "Create Transaction"}
                  </button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>
    </main>
  );
}