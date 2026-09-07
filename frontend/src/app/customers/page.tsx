"use client";

import { useEffect, useState } from "react";

import { getCustomers } from "@/services/api/customers";
import type { Customer } from "@/types/customer";

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCustomers() {
      try {
        setLoading(true);
        setError(null);

        const response = await getCustomers({
          page: 1,
          page_size: 20,
        });

        setCustomers(response.items);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load customers.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadCustomers();
  }, []);

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
          <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
            <div>
              <h2 className="font-semibold text-slate-900">Customer List</h2>

              <p className="mt-1 text-sm text-slate-500">
                {customers.length} customers loaded.
              </p>
            </div>

            <button
              type="button"
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
            >
              Add Customer
            </button>
          </div>

          {loading && (
            <div className="px-6 py-12 text-center text-sm text-slate-500">
              Loading customers...
            </div>
          )}

          {error && (
            <div className="px-6 py-12 text-center text-sm text-red-600">
              {error}
            </div>
          )}

          {!loading && !error && (
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
                      className="border-b border-slate-100 last:border-0"
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
          )}
        </div>
      </section>
    </main>
  );
}
