"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { getCustomer } from "@/services/api/customers";
import { getCustomerIntelligence } from "@/services/api/intelligence";

import type { Customer } from "@/types/customer";
import type { CustomerIntelligence } from "@/types/customerIntelligence";

import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";

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
        {" "}
        <LoadingState message="Loading customer intelligence..." />{" "}
      </main>
    );
  }

  if (error || !customer || !intelligence) {
    return (
      <main className="min-h-screen bg-slate-50 p-8">
        <ErrorState
          title="Unable to load customer intelligence"
          message={error ?? "Customer intelligence is unavailable."}
        />{" "}
      </main>
    );
  }

  const customerScore = Number(customer.score?.score ?? 0);

  const churnProbability =
    Number(intelligence.prediction.churn_probability) * 100;

  const normalizedChurnProbability = Math.min(
    Math.max(churnProbability, 0),
    100,
  );

  const riskLevel =
    normalizedChurnProbability >= 70
      ? "High"
      : normalizedChurnProbability >= 40
        ? "Elevated"
        : "Low";

  const riskExplanation =
    normalizedChurnProbability >= 70
      ? "The customer shows a strong likelihood of churn and may require immediate retention action."
      : normalizedChurnProbability >= 40
        ? "The customer shows behavioral signals that may require proactive engagement."
        : "The customer currently shows relatively stable behavior.";

  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}

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
        {/* Customer Health */}

        <section className="rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">Customer Health</h2>

            <p className="mt-1 text-sm text-slate-500">
              High-level indicators of the customer's current state.
            </p>
          </div>

          <div className="grid gap-6 p-6 md:grid-cols-3">
            <MetricCard
              title="Customer Score"
              value={customerScore.toFixed(2)}
              description="Current customer score"
            />

            <MetricCard
              title="Churn Probability"
              value={`${normalizedChurnProbability.toFixed(0)}%`}
              description="Predicted probability of churn"
            />

            <MetricCard
              title="Lifecycle Stage"
              value={customer.lifecycle_stage}
              description="Current customer lifecycle position"
            />
          </div>
        </section>

        {/* Behavioral Signals */}

        <section className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">Behavioral Signals</h2>

            <p className="mt-1 text-sm text-slate-500">
              Customer behavior used as input to the prediction.
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
              title="Customer Inactivity"
              value={`${intelligence.features.days_since_last_transaction} days`}
              description="Days since last transaction"
            />
          </div>
        </section>

        {/* Risk Assessment */}

        <section className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-4">
            <h2 className="font-semibold text-slate-900">Risk Assessment</h2>

            <p className="mt-1 text-sm text-slate-500">
              Interpretation of the predicted churn probability.
            </p>
          </div>

          <div className="p-6">
            <div className="grid gap-8 md:grid-cols-[auto_1fr] md:items-center">
              <div>
                <p className="text-sm font-medium text-slate-500">Assessment</p>

                <p className="mt-2 text-3xl font-bold text-slate-900">
                  {riskLevel}
                </p>
              </div>

              <div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-500">Churn probability</span>

                  <span className="font-semibold text-slate-900">
                    {normalizedChurnProbability.toFixed(0)}%
                  </span>
                </div>

                <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-100">
                  <div
                    className="h-full rounded-full bg-slate-900 transition-all duration-500"
                    style={{
                      width: `${normalizedChurnProbability}%`,
                    }}
                  />
                </div>

                <p className="mt-4 text-sm leading-6 text-slate-600">
                  {riskExplanation}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Decision & Next Best Action */}

        <section className="mt-8 rounded-xl border border-slate-200 bg-white shadow-sm">
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
        </section>

        {/* Intelligence Flow */}

        <section className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="font-semibold text-slate-900">Intelligence Flow</h2>

          <p className="mt-1 text-sm text-slate-500">
            How customer behavior becomes an actionable recommendation.
          </p>

          <div className="mt-6 flex flex-col gap-3 md:flex-row md:items-center">
            <FlowStep label="Customer Behavior" />

            <FlowArrow />

            <FlowStep label="Prediction" />

            <FlowArrow />

            <FlowStep label="Decision" />

            <FlowArrow />

            <FlowStep label="Next Best Action" />
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
    <div className="rounded-lg border border-slate-200 p-5">
      {" "}
      <p className="text-sm font-medium text-slate-500">{title} </p>
      <p className="mt-3 text-2xl font-bold text-slate-900">{value}</p>
      <p className="mt-2 text-xs text-slate-500">{description}</p>
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
      {" "}
      <p className="text-sm font-medium text-slate-500">{title} </p>
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
      {" "}
      <p className="text-sm font-medium text-slate-500">{title} </p>
      <p className="mt-3 break-words text-lg font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}

function FlowStep({ label }: { label: string }) {
  return (
    <div className="flex-1 rounded-lg border border-slate-200 bg-slate-50 px-4 py-4 text-center">
      {" "}
      <span className="text-sm font-medium text-slate-700">{label} </span>{" "}
    </div>
  );
}

function FlowArrow() {
  return <div className="hidden text-xl text-slate-400 md:block">→ </div>;
}
