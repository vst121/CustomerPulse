"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import Badge from "@/components/ui/Badge";
import Card, { CardContent, CardHeader } from "@/components/ui/Card";
import ErrorState from "@/components/ui/ErrorState";
import LoadingState from "@/components/ui/LoadingState";
import { getCustomer } from "@/services/api/customers";
import {
  generateCustomerRecommendation,
  getCustomerRecommendations,
} from "@/services/api/recommendations";
import type { Customer } from "@/types/customer";
import type { Recommendation } from "@/types/recommendation";

function getRecommendationLabel(type: string): string {
  return type
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function CustomerRecommendationsPage({
  params,
}: {
  params: Promise<{ customerId: string }>;
}) {
  const [customer, setCustomer] = useState<Customer | null>(null);

  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        setLoading(true);
        setError(null);

        const { customerId } = await params;

        const [customerResponse, recommendationResponse] = await Promise.all([
          getCustomer(customerId),
          getCustomerRecommendations(customerId),
        ]);

        if (cancelled) {
          return;
        }

        setCustomer(customerResponse);
        setRecommendations(recommendationResponse);
      } catch (err) {
        if (cancelled) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load recommendations.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void fetchData();

    return () => {
      cancelled = true;
    };
  }, [params]);

  async function handleGenerate() {
    try {
      setGenerating(true);
      setError(null);

      const { customerId } = await params;

      const recommendation =
        await generateCustomerRecommendation(customerId);

      setRecommendations((current) => [recommendation, ...current]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to generate recommendation.",
      );
    } finally {
      setGenerating(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 p-8 dark:bg-slate-950">
        <LoadingState message="Loading recommendations..." />
      </main>
    );
  }

  if (error && !customer) {
    return (
      <main className="min-h-screen bg-slate-50 p-8 dark:bg-slate-950">
        <ErrorState title="Unable to load recommendations" message={error} />
      </main>
    );
  }

  if (!customer) {
    return (
      <main className="min-h-screen bg-slate-50 p-8 dark:bg-slate-950">
        <ErrorState
          title="Customer not found"
          message="The requested customer could not be found."
        />
      </main>
    );
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

            <Link
              href={`/customers/${customer.id}`}
              className="text-sm font-medium text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
            >
              {customer.first_name} {customer.last_name}
            </Link>

            <span className="text-slate-300 dark:text-slate-700">/</span>

            <span className="text-sm text-slate-500 dark:text-slate-400">
              Recommendations
            </span>
          </div>

          <div className="mt-4 flex items-start justify-between gap-6">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
                Recommendations
              </h1>

              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                AI-driven next best actions for {customer.first_name}{" "}
                {customer.last_name}.
              </p>
            </div>

            <button
              type="button"
              onClick={handleGenerate}
              disabled={generating}
              className="rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
            >
              {generating ? "Generating..." : "Generate Recommendation"}
            </button>
          </div>
        </div>
      </header>

      <section className="p-8">
        <div className="mx-auto max-w-5xl">
          {error && (
            <div className="mb-6">
              <ErrorState
                title="Recommendation action failed"
                message={error}
              />
            </div>
          )}

          <Card>
            <CardHeader>
              <h2 className="font-semibold text-slate-900 dark:text-white">
                Customer Recommendations
              </h2>

              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Recommended actions based on the customer&apos;s current
                behavior and intelligence.
              </p>
            </CardHeader>

            <CardContent>
              {recommendations.length === 0 ? (
                <div className="py-12 text-center">
                  <p className="font-medium text-slate-900 dark:text-white">
                    No recommendations yet
                  </p>

                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                    Generate a recommendation to determine the next best action
                    for this customer.
                  </p>

                  <button
                    type="button"
                    onClick={handleGenerate}
                    disabled={generating}
                    className="mt-5 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
                  >
                    {generating ? "Generating..." : "Generate Recommendation"}
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {recommendations.map((recommendation) => (
                    <div
                      key={recommendation.id}
                      className="rounded-xl border border-slate-200 p-5 dark:border-slate-800"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <h3 className="font-semibold text-slate-900 dark:text-white">
                            {getRecommendationLabel(recommendation.type)}
                          </h3>

                          <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
                            {recommendation.reason}
                          </p>
                        </div>

                        <Badge>Recommendation</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </section>
    </main>
  );
}
