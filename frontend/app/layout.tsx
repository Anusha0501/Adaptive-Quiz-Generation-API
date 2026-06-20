import type { Metadata } from "next";
import Link from "next/link";
import { Providers } from "./providers";
import "./globals.css";

export const metadata: Metadata = { title: "Adaptive Quiz AI", description: "AI assessment platform with Bloom taxonomy analytics" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><Providers><header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5"><Link href="/" className="text-lg font-bold">Adaptive Quiz AI</Link><nav className="flex gap-4 text-sm text-muted-foreground"><Link href="/quiz-generator">Generator</Link><Link href="/quiz">Take Quiz</Link><Link href="/results">Results</Link><Link href="/analytics">Analytics</Link></nav></header>{children}</Providers></body></html>;
}
