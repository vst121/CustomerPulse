"use client";

type CustomerHealthCardProps = {
  score: number;
  churnProbability: number;
};

function getRiskLabel(probability: number): string {
  if (probability >= 70) {
    return "High";
  }

  if (probability >= 40) {
    return "Medium";
  }

  return "Low";
}

function getHealthLabel(score: number, churnProbability: number): string {
  if (churnProbability >= 70 || score < 40) {
    return "At Risk";
  }

  if (churnProbability >= 40 || score < 60) {
    return "Needs Attention";
  }

  return "Healthy";
}

export default function CustomerHealthCard({
  score,
  churnProbability,
}: CustomerHealthCardProps) {
  const riskLabel = getRiskLabel(churnProbability);
  const healthLabel = getHealthLabel(score, churnProbability);

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-semibold text-slate-900">Customer Health</h2>

          <p className="mt-1 text-sm text-slate-500">
            Value and churn risk overview.
          </p>
        </div>

        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
          {healthLabel}
        </span>
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        {/* Customer Score */}

        <div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-600">
              Customer Score
            </span>

            <span className="text-sm font-semibold text-slate-900">
              {score}
            </span>
          </div>

          <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-slate-900 transition-all"
              style={{
                width: `${Math.min(Math.max(score, 0), 100)}%`,
              }}
            />
          </div>
        </div>

        {/* Churn Risk */}

        <div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-600">
              Churn Risk
            </span>

            <span className="text-sm font-semibold text-slate-900">
              {churnProbability.toFixed(0)}%
            </span>
          </div>

          <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-slate-900 transition-all"
              style={{
                width: `${Math.min(Math.max(churnProbability, 0), 100)}%`,
              }}
            />
          </div>

          <p className="mt-2 text-xs text-slate-500">
            {riskLabel} churn probability
          </p>
        </div>
      </div>
    </div>
  );
}
