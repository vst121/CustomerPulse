"use client";

import { useEffect, useState } from "react";

import { getCustomer } from "@/services/api/customers";
import type { Customer } from "@/types/customer";

type CustomerPageProps = {
  params: Promise<{
    customerId: string;
  }>;
};

export default function CustomerPage({ params }: CustomerPageProps) {
  const [customerId, setCustomerId] = useState<string | null>(null);
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCustomer() {
      try {
        const { customerId } = await params;

        setCustomerId(customerId);

        const response = await getCustomer(customerId);

        setCustomer(response);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load customer.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadCustomer();
  }, [params]);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <div className="text-sm text-slate-500">Loading customer...</div>
      </main>
    );
  }

  if (error || !customer) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6">
          <h1 className="font-semibold text-red-900">
            Unable to load customer
          </h1>

          <p className="mt-2 text-sm text-red-700">
            {error ?? "Customer not found."}
          </p>

          {customerId && (
            <p className="mt-2 text-xs text-red-600">
              Customer ID: {customerId}
            </p>
          )}
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}

      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <a
            href="/customers"
            className="text-sm font-medium text-slate-500 hover:text-slate-900"
          >
            ← Customers
          </a>

          <div className="mt-4 flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                {customer.first_name} {customer.last_name}
              </h1>

              <p className="mt-1 text-sm text-slate-500">{customer.email}</p>
            </div>

            <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
              {customer.lifecycle_stage}
            </span>
          </div>
        </div>
      </header>

      {/* Content */}

      <section className="p-8">
        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <ProfileCard
            title="Lifecycle Stage"
            value={customer.lifecycle_stage}
          />

          <ProfileCard title="Customer ID" value={customer.id} />

          <ProfileCard title="Email" value={customer.email} />

          <ProfileCard
            title="Customer Since"
            value={new Date(customer.created_at).toLocaleDateString()}
          />
        </div>

        {/* Navigation */}

        <div className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">Customer Insights</h2>

            <p className="mt-1 text-sm text-slate-500">
              Explore customer activity, value, and intelligence.
            </p>
          </div>

          <div className="grid gap-4 p-6 md:grid-cols-3">
            <InsightLink
              title="Customer 360"
              description="Complete customer overview"
              href={`/customers/${customer.id}/360`}
            />

            <InsightLink
              title="Intelligence"
              description="Prediction and next best action"
              href={`/customers/${customer.id}/intelligence`}
            />

            <InsightLink
              title="Transactions"
              description="Customer transaction history"
              href={`/customers/${customer.id}/transactions`}
            />
          </div>
        </div>
      </section>
    </main>
  );
}

type ProfileCardProps = {
  title: string;
  value: string;
};

function ProfileCard({ title, value }: ProfileCardProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{title}</p>

      <p className="mt-3 break-all text-lg font-semibold text-slate-900">
        {value}
      </p>
    </div>
  );
}

type InsightLinkProps = {
  title: string;
  description: string;
  href: string;
};

function InsightLink({ title, description, href }: InsightLinkProps) {
  return (
    <a
      href={href}
      className="rounded-lg border border-slate-200 p-5 transition hover:border-slate-400 hover:bg-slate-50"
    >
      <h3 className="font-semibold text-slate-900">{title}</h3>

      <p className="mt-1 text-sm text-slate-500">{description}</p>

      <p className="mt-4 text-sm font-medium text-slate-900">Open →</p>
    </a>
  );
}
