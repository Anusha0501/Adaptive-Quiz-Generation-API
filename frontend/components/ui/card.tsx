import { cn } from "@/components/ui/utils";

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("gradient-card p-6", className)} {...props} />;
}
