import * as React from "react";
import { cn } from "@/components/ui/utils";

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={cn("w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 outline-none ring-primary transition focus:ring-2", props.className)} />;
}
