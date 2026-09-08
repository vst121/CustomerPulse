type BadgeProps = {
  children: React.ReactNode;
  className?: string;
};

export default function Badge({ children, className = "" }: BadgeProps) {
  return (
    <span
      className={`rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700 dark:bg-slate-800 dark:text-slate-200 ${className}`}
    >
      {children}
    </span>
  );
}
