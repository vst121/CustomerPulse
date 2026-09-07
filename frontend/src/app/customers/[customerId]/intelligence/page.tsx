"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { getCustomerIntelligence } from "@/services/api/intelligence";
import { getCustomer } from "@/services/api/customers";
import type { Customer } from "@/types/customer";
import type { CustomerIntelligence } from "@/types/customerIntelligence";

import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import MetricCard from "@/components/ui/MetricCard";

type IntelligencePageProps = {
  params: Promise<{
    customerId: string;
  }>;
};

export default function IntelligencePage({ params }: IntelligencePageProps) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [intelligence, setIntelligence] = useState<CustomerIntelligence | null>(
    null,
  );

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadIntelligence() {
      try {
        const { customerId } = await params;

        const [customerResponse, intelligenceResponse] = await Promise.all([
          getCustomer(customerId),
          getCustomerIntelligence(customerId),
        ]);

        if (cancelled) {
          return;
        }

        setCustomer(customerResponse);
        setIntelligence(intelligenceResponse);
      } catch (err) {
        if (cancelled) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load customer intelligence.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadIntelligence();

    return () => {
      cancelled = true;
    };
  }, [params]);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <LoadingState message="Loading customer intelligence..." />
      </main>
    );
  }

  if (error || !customer || !intelligence) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <ErrorState
          title="Unable to load customer intelligence"
          message={error ?? "Customer intelligence is unavailable."}
        />
      </main>
    );
  }

  const churnProbability =
    Number(intelligence.prediction.churn_probability) * 100;

  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <Link
            href={`/customers/${customer.id}`}
            className="text-sm font-medium text-slate-500 hover:text-slate-900"
          >
            ← Customer Profile
          </Link>

          <div className="mt-4">
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              {customer.first_name} {customer.last_name}
            </h1>

            <p className="mt-1 text-sm text-slate-500">Customer Intelligence</p>
          </div>
        </div>
      </header>

      <section className="p-8">
        <div className="grid gap-6 lg:grid-cols-3">
          <RiskCard probability={churnProbability} />

          <MetricCard
            title="Transactions"
            value={String(intelligence.features.transaction_count)}
            description="Completed transactions"
          />

          <MetricCard
            title="Total Transaction Value"
            value={`€${intelligence.features.total_transaction_value}`}
            description="Customer transaction value"
          />
        </div>

        <div className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">Behavioral Signals</h2>

            <p className="mt-1 text-sm text-slate-500">
              Features used by the prediction model.
            </p>
          </div>

          <div className="grid gap-6 p-6 md:grid-cols-3">
            <SignalCard
              title="Transaction Count"
              value={String(intelligence.features.transaction_count)}
              description="Completed transactions"
            />

            <SignalCard
              title="Average Transaction"
              value={`€${intelligence.features.average_transaction_value}`}
              description="Average transaction value"
            />

            <SignalCard
              title="Days Since Last Transaction"
              value={String(intelligence.features.days_since_last_transaction)}
              description="Customer inactivity"
            />
          </div>
        </div>
        <div className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">
              Decision & Next Best Action
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              The recommended intervention based on the prediction.
            </p>
          </div>

          <div className="grid gap-6 p-6 md:grid-cols-3">
            <DecisionCard
              title="Action"
              value={intelligence.action.action_type}
            />

            <DecisionCard
              title="Priority"
              value={String(intelligence.action.priority)}
            />

            <div className="rounded-lg border border-slate-200 p-5">
              <p className="text-sm font-medium text-slate-500">Reason</p>

              <p className="mt-3 text-sm leading-6 text-slate-700">
                {intelligence.action.reason}
              </p>
            </div>
          </div>
        </div>

        <div className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="font-semibold text-slate-900">Intelligence Flow</h2>

          <div className="mt-6 flex flex-col gap-3 md:flex-row md:items-center">
            <FlowStep label="Customer Behavior" />
            <FlowArrow />
            <FlowStep label="Churn Prediction" />
            <FlowArrow />
            <FlowStep label="Decision" />
            <FlowArrow />
            <FlowStep label="Next Best Action" />
          </div>
        </div>
      </section>
    </main>
  );
}

type RiskCardProps = {
  probability: number;
};

function RiskCard({ probability }: RiskCardProps) {
  const normalizedProbability = Math.min(Math.max(probability, 0), 100);

  const riskLabel =
    normalizedProbability >= 70
      ? "High Risk"
      : normalizedProbability >= 40
        ? "Elevated Risk"
        : "Low Risk";

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Churn Probability
          </p>

          <p className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
            {normalizedProbability.toFixed(0)}%
          </p>
        </div>

        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
          {riskLabel}
        </span>
      </div>

      <div className="mt-6">
        <div className="flex justify-between text-xs text-slate-400">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>

        <div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-slate-900 transition-all duration-500"
            style={{
              width: `${normalizedProbability}%`,
            }}
          />
        </div>
      </div>

      <p className="mt-4 text-sm text-slate-500">
        Predicted probability of customer churn based on observed customer
        behavior.
      </p>
    </div>
  );
}

type SignalCardProps = {
  title: string;
  value: string;
  description: string;
};

function SignalCard({ title, value, description }: SignalCardProps) {
  return (
    <div className="rounded-lg border border-slate-200 p-5">
      <p className="text-sm font-medium text-slate-500">{title}</p>

      <p className="mt-3 text-2xl font-bold text-slate-900">{value}</p>

      <p className="mt-2 text-xs text-slate-500">{description}</p>
    </div>
  );
}

type DecisionCardProps = {
  title: string;
  value: string;
};

function DecisionCard({ title, value }: DecisionCardProps) {
  return (
    <div className="rounded-lg border border-slate-200 p-5">
      <p className="text-sm font-medium text-slate-500">{title}</p>

      <p className="mt-3 break-words text-lg font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}

function FlowStep({ label }: { label: string }) {
  return (
    <div className="flex-1 rounded-lg border border-slate-200 bg-slate-50 px-4 py-4 text-center">
      <span className="text-sm font-medium text-slate-700">{label}</span>
    </div>
  );
}

function FlowArrow() {
  return <div className="hidden text-xl text-slate-400 md:block">→</div>;
}
