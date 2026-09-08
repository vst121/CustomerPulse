"use client";

import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

type CategorySpending = {
  category: string;
  amount: number;
};

type SpendingByCategoryChartProps = {
  data: CategorySpending[];
  currency?: string;
};

export default function SpendingByCategoryChart({
  data,
  currency = "EUR",
}: SpendingByCategoryChartProps) {
  if (data.length === 0) {
    return (
      <div className="flex h-80 items-center justify-center text-sm text-slate-500">
        No transaction data available.
      </div>
    );
  }

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="amount"
            nameKey="category"
            cx="50%"
            cy="50%"
            outerRadius={110}
            innerRadius={65}
            paddingAngle={2}
            label={({ category, percent }) =>
              `${category} ${(percent * 100).toFixed(0)}%`
            }
          >
            {data.map((entry) => (
              <Cell key={entry.category} />
            ))}
          </Pie>

          <Tooltip
            formatter={(value) => [
              `${Number(value).toFixed(2)} ${currency}`,
              "Spending",
            ]}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}