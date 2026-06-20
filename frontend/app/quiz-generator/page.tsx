"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useGenerateQuiz } from "@/hooks/use-quiz";
import type { Difficulty } from "@/types/quiz";

export default function QuizGeneratorPage() {
  const router = useRouter();
  const [topic, setTopic] = useState("PostgreSQL indexing");
  const [difficulty, setDifficulty] = useState<Difficulty>("medium");
  const [numberOfQuestions, setNumberOfQuestions] = useState(10);
  const mutation = useGenerateQuiz();

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const quiz = await mutation.mutateAsync({ topic, difficulty, numberOfQuestions });
    sessionStorage.setItem("activeQuiz", JSON.stringify(quiz));
    router.push("/quiz");
  }

  return <main className="mx-auto max-w-4xl px-6 py-12"><Card><p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Quiz Generator</p><h1 className="mt-3 text-4xl font-black">Create a validated AI quiz</h1><p className="mt-2 text-muted-foreground">The frontend collects the requested controls while the backend enforces ten unique MCQs and validation gates.</p><form onSubmit={onSubmit} className="mt-8 grid gap-5"><label className="grid gap-2"><span className="font-semibold">Topic</span><Input value={topic} onChange={(event) => setTopic(event.target.value)} required minLength={2} /></label><label className="grid gap-2"><span className="font-semibold">Difficulty</span><select className="rounded-xl border border-white/10 bg-white/5 px-4 py-3" value={difficulty} onChange={(event) => setDifficulty(event.target.value as Difficulty)}><option className="bg-slate-900" value="easy">Easy</option><option className="bg-slate-900" value="medium">Medium</option><option className="bg-slate-900" value="hard">Hard</option></select></label><label className="grid gap-2"><span className="font-semibold">Number of Questions</span><Input type="number" min={1} max={10} value={numberOfQuestions} onChange={(event) => setNumberOfQuestions(Number(event.target.value))} /></label>{mutation.isError ? <p className="rounded-xl bg-red-500/10 p-3 text-red-200">{mutation.error.message}</p> : null}<Button disabled={mutation.isPending}>{mutation.isPending ? "Generating..." : "Generate Quiz"}</Button></form></Card></main>;
}
