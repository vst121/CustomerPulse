"use client";
import { useEffect, useState } from "react";

import { getCustomers } from "@/services/api/customers";
import type { Customer, LifecycleStage } from "@/types/customer";

import LoadingState from "@/components/ui/LoadingState";

const PAGE_SIZE = 10;

const lifecycleStages: LifecycleStage[] = [
  "ACQUISITION",
  "ONBOARDING",
  "ACTIVATION",
  "ENGAGEMENT",
  "GROWTH",
  "RETENTION",
  "WIN_BACK",
];

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const [search, setSearch] = useState("");
  const [lifecycleStage, setLifecycleStage] = useState<LifecycleStage | "">("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  useEffect(() => {
    let cancelled = false;

    async function fetchCustomers() {
      try {
        setLoading(true);
        setError(null);

        const response = await getCustomers({
          page,
          page_size: PAGE_SIZE,
          search: search.trim() || undefined,
          lifecycle_stage: lifecycleStage || undefined,
        });

        if (cancelled) {
          return;
        }

        setCustomers(response.items);
        setTotal(response.total);
      } catch (err) {
        if (cancelled) {
          return;
        }

        setError(
          err instanceof Error ? err.message : "Failed to load customers.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void fetchCustomers();

    return () => {
      cancelled = true;
    };
  }, [page, search, lifecycleStage]);

  function handleSearchChange(value: string) {
    setSearch(value);
    setPage(1);
  }

  function handleLifecycleChange(value: LifecycleStage | "") {
    setLifecycleStage(value);
    setPage(1);
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Customers
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Manage customers and understand their lifecycle.
          </p>
        </div>
      </header>

      <section className="p-8">
        <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
          {/* Header */}

          <div className="border-b border-slate-200 px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-slate-900">Customer List</h2>

                <p className="mt-1 text-sm text-slate-500">{total} customers</p>
              </div>

              <button
                type="button"
                className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
              >
                Add Customer
              </button>
            </div>

            {/* Filters */}

            <div className="mt-4 flex flex-col gap-3 md:flex-row">
              <input
                type="search"
                value={search}
                onChange={(event) => handleSearchChange(event.target.value)}
                placeholder="Search customers..."
                className="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 md:max-w-md"
              />

              <select
                value={lifecycleStage}
                onChange={(event) =>
                  handleLifecycleChange(
                    event.target.value as LifecycleStage | "",
                  )
                }
                className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
              >
                <option value="">All lifecycle stages</option>

                {lifecycleStages.map((stage) => (
                  <option key={stage} value={stage}>
                    {stage}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Error */}

          {error && (
            <div className="border-b border-red-100 bg-red-50 px-6 py-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Loading */}

          {loading && (
            <div className="px-6">
              <LoadingState message="Loading customers..." />
            </div>
          )}

          {/* Table */}

          {!loading && !error && (
            <>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="border-b border-slate-200 bg-slate-50">
                    <tr>
                      <th className="px-6 py-3 font-medium text-slate-500">
                        Customer
                      </th>

                      <th className="px-6 py-3 font-medium text-slate-500">
                        Email
                      </th>

                      <th className="px-6 py-3 font-medium text-slate-500">
                        Lifecycle
                      </th>

                      <th className="px-6 py-3 font-medium text-slate-500">
                        Created
                      </th>

                      <th className="px-6 py-3 font-medium text-slate-500">
                        Action
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {customers.map((customer) => (
                      <tr
                        key={customer.id}
                        className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                      >
                        <td className="px-6 py-4">
                          <div className="font-medium text-slate-900">
                            {customer.first_name} {customer.last_name}
                          </div>
                        </td>

                        <td className="px-6 py-4 text-slate-600">
                          {customer.email}
                        </td>

                        <td className="px-6 py-4">
                          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                            {customer.lifecycle_stage}
                          </span>
                        </td>

                        <td className="px-6 py-4 text-slate-600">
                          {new Date(customer.created_at).toLocaleDateString()}
                        </td>

                        <td className="px-6 py-4">
                          <a
                            href={`/customers/${customer.id}`}
                            className="font-medium text-slate-900 hover:underline"
                          >
                            View
                          </a>
                        </td>
                      </tr>
                    ))}

                    {customers.length === 0 && (
                      <tr>
                        <td
                          colSpan={5}
                          className="px-6 py-12 text-center text-slate-500"
                        >
                          No customers found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}

              <div className="flex items-center justify-between border-t border-slate-200 px-6 py-4">
                <p className="text-sm text-slate-500">
                  Page {page} of {totalPages}
                </p>

                <div className="flex gap-2">
                  <button
                    type="button"
                    disabled={page <= 1}
                    onClick={() => setPage((current) => current - 1)}
                    className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    Previous
                  </button>

                  <button
                    type="button"
                    disabled={page >= totalPages}
                    onClick={() => setPage((current) => current + 1)}
                    className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    Next
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </section>
    </main>
  );
}
