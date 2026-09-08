"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import Card, { CardContent, CardHeader } from "@/components/ui/Card";
import ErrorState from "@/components/ui/ErrorState";
import { createCustomer } from "@/services/api/customers";

export default function NewCustomerPage() {
  const router = useRouter();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      setLoading(true);
      setError(null);

      const customer = await createCustomer({
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        email: email.trim(),
      });

      router.push(`/customers/${customer.id}`);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create customer.",
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
              href="/customers"
              className="text-sm font-medium text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
            >
              Customers
            </Link>

            <span className="text-slate-300 dark:text-slate-700">/</span>

            <span className="text-sm text-slate-500 dark:text-slate-400">
              Add Customer
            </span>
          </div>

          <h1 className="mt-3 text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            Add Customer
          </h1>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Create a new customer profile.
          </p>
        </div>
      </header>

      <section className="p-8">
        <div className="mx-auto max-w-2xl">
          <Card>
            <CardHeader>
              <h2 className="font-semibold text-slate-900 dark:text-white">
                Customer Information
              </h2>

              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Enter the basic information for the new customer.
              </p>
            </CardHeader>

            <CardContent>
              {error && (
                <div className="mb-6">
                  <ErrorState
                    title="Unable to create customer"
                    message={error}
                  />
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <label
                      htmlFor="first-name"
                      className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      First Name
                    </label>

                    <input
                      id="first-name"
                      type="text"
                      value={firstName}
                      onChange={(event) => setFirstName(event.target.value)}
                      required
                      maxLength={100}
                      autoComplete="given-name"
                      className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="last-name"
                      className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      Last Name
                    </label>

                    <input
                      id="last-name"
                      type="text"
                      value={lastName}
                      onChange={(event) => setLastName(event.target.value)}
                      required
                      maxLength={100}
                      autoComplete="family-name"
                      className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-slate-700 dark:text-slate-300"
                  >
                    Email
                  </label>

                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                    autoComplete="email"
                    className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-slate-500 dark:focus:ring-slate-700"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  <Link
                    href="/customers"
                    className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    Cancel
                  </Link>

                  <button
                    type="submit"
                    disabled={loading}
                    className="rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
                  >
                    {loading ? "Creating..." : "Create Customer"}
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
