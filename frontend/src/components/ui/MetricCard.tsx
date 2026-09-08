import Card, { CardContent } from "./Card";

type MetricCardProps = {
  title: string;
  value: string;
  description?: string;
};

export default function MetricCard({
  title,
  value,
  description,
}: MetricCardProps) {
  return (
    <Card>
      <CardContent>
        <p className="text-sm font-medium text-slate-500">{title}</p>

        <p className="mt-3 text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          {value}
        </p>

        {description && (
          <p className="mt-2 text-sm text-slate-500">{description}</p>
        )}
      </CardContent>
    </Card>
  );
}
