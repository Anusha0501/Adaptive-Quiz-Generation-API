import * as React from "react";
import { cn } from "@/components/ui/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "ghost" };

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  const variants = {
    primary: "bg-primary text-primary-foreground hover:bg-primary/90",
    secondary: "bg-white/10 text-white hover:bg-white/15",
    ghost: "bg-transparent text-white hover:bg-white/10"
  };
  return <button className={cn("inline-flex items-center justify-center rounded-xl px-5 py-3 font-semibold transition disabled:cursor-not-allowed disabled:opacity-60", variants[variant], className)} {...props} />;
}
