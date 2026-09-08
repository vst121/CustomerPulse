"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type TransactionTrend = {
  month: string;
  amount: number;
};

type TransactionTrendChartProps = {
  data: TransactionTrend[];
  currency?: string;
};

export default function TransactionTrendChart({
  data,
  currency = "EUR",
}: TransactionTrendChartProps) {
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
        <LineChart
          data={data}
          margin={{
            top: 10,
            right: 20,
            left: 0,
            bottom: 10,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            vertical={false}
          />

          <XAxis
            dataKey="month"
            tickLine={false}
            axisLine={false}
          />

          <YAxis
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `${value}`}
          />

          <Tooltip
            formatter={(value) => [
              `${Number(value).toFixed(2)} ${currency}`,
              "Spending",
            ]}
          />

          <Line
            type="monotone"
            dataKey="amount"
            stroke="currentColor"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            className="text-slate-900"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}