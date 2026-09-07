type ErrorStateProps = {
  title?: string;
  message: string;
};

export default function ErrorState({
  title = "Something went wrong",
  message,
}: ErrorStateProps) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-6">
      <h1 className="font-semibold text-red-900">
        {title}
      </h1>

      <p className="mt-2 text-sm text-red-700">
        {message}
      </p>
    </div>
  );
}