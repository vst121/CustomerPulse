"use client";

import { useEffect, useState } from "react";

import MetricCard from "@/components/ui/MetricCard";
import { getCustomers } from "@/services/api/customers";
import PageHeader from "@/components/layout/PageHeader";

const lifecycleStages = [
  "Acquisition",
  "Onboarding",
  "Activation",
  "Engagement",
  "Growth",
  "Retention",
  "Win-back",
];

export default function HomePage() {
  const [customerCount, setCustomerCount] = useState<number | null>(null);

  useEffect(() => {
    async function loadCustomerCount() {
      try {
        const response = await getCustomers({
          page: 1,
          page_size: 1,
        });

        setCustomerCount(response.total);
      } catch {
        setCustomerCount(null);
      }
    }

    loadCustomerCount();
  }, []);

  return (
    <main className="min-h-screen">
      <PageHeader title="Dashboard" description="Customers Dashboard " />
      <div className="p-8">
        <div className="mb-8">
          <p className="text-sm font-medium text-slate-500">
            Customer Lifecycle & Value Management
          </p>

          <h3 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
            Customer Overview
          </h3>

          <p className="mt-2 max-w-2xl text-slate-600">
            Understand your customers, their lifecycle, and the actions that can
            improve customer value.
          </p>
        </div>

        <div className="mb-10 max-w-sm">
          <MetricCard
            title="Customers"
            value={customerCount !== null ? String(customerCount) : "—"}
            description="Total customers"
          />
        </div>

        <section>
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-slate-900">
              Customer Lifecycle
            </h4>

            <p className="mt-1 text-sm text-slate-500">
              CustomerPulse manages the customer journey from acquisition to
              win-back.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7">
            {lifecycleStages.map((stage, index) => (
              <div
                key={stage}
                className="rounded-xl border border-slate-200 bg-white p-5"
              >
                <div className="mb-4 flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-700">
                  {index + 1}
                </div>

                <h5 className="text-sm font-semibold text-slate-900">
                  {stage}
                </h5>

                <p className="mt-1 text-xs leading-5 text-slate-500">
                  Customer lifecycle stage
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-10">
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
            <h4 className="text-lg font-semibold text-slate-900">
              Customer Intelligence
            </h4>

            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
              CustomerPulse combines customer behavior, value, lifecycle
              signals, churn prediction, and next-best-action decisions to
              support customer-focused decisions.
            </p>

            <div className="mt-5 flex flex-wrap items-center gap-2 text-sm">
              <span className="rounded-full bg-white px-3 py-1.5 font-medium text-slate-700 ring-1 ring-slate-200">
                Customer Data
              </span>

              <span className="text-slate-400">→</span>

              <span className="rounded-full bg-white px-3 py-1.5 font-medium text-slate-700 ring-1 ring-slate-200">
                Prediction
              </span>

              <span className="text-slate-400">→</span>

              <span className="rounded-full bg-white px-3 py-1.5 font-medium text-slate-700 ring-1 ring-slate-200">
                Decision
              </span>

              <span className="text-slate-400">→</span>

              <span className="rounded-full bg-white px-3 py-1.5 font-medium text-slate-700 ring-1 ring-slate-200">
                Next Best Action
              </span>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
