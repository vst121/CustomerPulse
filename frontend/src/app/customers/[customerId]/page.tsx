"use client";
import Link from "next/link";
import { useEffect, useState } from "react";

import { getCustomer } from "@/services/api/customers";
import type { Customer } from "@/types/customer";

import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import Badge from "@/components/ui/Badge";
import Card, { CardContent, CardHeader } from "@/components/ui/Card";

type CustomerPageProps = {
  params: Promise<{
    customerId: string;
  }>;
};

export default function CustomerPage({ params }: CustomerPageProps) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCustomer() {
      try {
        const { customerId } = await params;

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
        <LoadingState message="Loading customer..." />
      </main>
    );
  }

  if (error || !customer) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <ErrorState
          title="Unable to load customer"
          message={error ?? "Customer not found."}
        />
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}

      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <Link
            href="/customers"
            className="text-sm font-medium text-slate-500 hover:text-slate-900"
          >
            ← Customers
          </Link>

          <div className="mt-4 flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                {customer.first_name} {customer.last_name}
              </h1>

              <p className="mt-1 text-sm text-slate-500">{customer.email}</p>
            </div>

            <Badge className="px-4 py-2 text-sm">
              {customer.lifecycle_stage}
            </Badge>
          </div>
        </div>
      </header>

      {/* Content */}

      <section className="p-8">
        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <Card>
            <CardContent>
              <p className="text-sm font-medium text-slate-500">
                Lifecycle Stage
              </p>

              <p className="mt-3 text-lg font-semibold text-slate-900">
                {customer.lifecycle_stage}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <p className="text-sm font-medium text-slate-500">Customer ID</p>

              <p className="mt-3 break-all text-lg font-semibold text-slate-900">
                {customer.id}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <p className="text-sm font-medium text-slate-500">Email</p>

              <p className="mt-3 break-all text-lg font-semibold text-slate-900">
                {customer.email}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <p className="text-sm font-medium text-slate-500">
                Customer Since
              </p>

              <p className="mt-3 text-lg font-semibold text-slate-900">
                {new Date(customer.created_at).toLocaleDateString()}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Navigation */}

        <Card className="mt-8">
          <CardHeader>
            <h2 className="font-semibold text-slate-900">Customer Insights</h2>

            <p className="mt-1 text-sm text-slate-500">
              Explore customer activity, value, and intelligence.
            </p>
          </CardHeader>

          <CardContent>
            <div className="grid gap-4 md:grid-cols-4">
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
              <InsightLink
                title="Recommendations"
                description="Customer recommendations"
                href={`/customers/${customer.id}/recommendations`}
              />
            </div>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}

type InsightLinkProps = {
  title: string;
  description: string;
  href: string;
};

function InsightLink({ title, description, href }: InsightLinkProps) {
  return (
    <Link
      href={href}
      className="rounded-lg border border-slate-200 p-5 transition hover:border-slate-400 hover:bg-slate-50"
    >
      <h3 className="font-semibold text-slate-900">{title}</h3>

      <p className="mt-1 text-sm text-slate-500">{description}</p>

      <p className="mt-4 text-sm font-medium text-slate-900">Open →</p>
    </Link>
  );
}
