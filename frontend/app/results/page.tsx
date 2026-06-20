"use client";

import { useEffect, useMemo, useState } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Card } from "@/components/ui/card";
import type { QuizResponse } from "@/types/quiz";

const colors = ["#8b5cf6", "#06b6d4", "#22c55e", "#f59e0b", "#ef4444", "#ec4899"];

export default function ResultsPage() {
  const [quiz, setQuiz] = useState<QuizResponse | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  useEffect(() => { const storedQuiz = sessionStorage.getItem("completedQuiz"); const storedAnswers = sessionStorage.getItem("quizAnswers"); if (storedQuiz) setQuiz(JSON.parse(storedQuiz)); if (storedAnswers) setAnswers(JSON.parse(storedAnswers)); }, []);
  const result = useMemo(() => { if (!quiz) return null; const correct = quiz.questions.filter((q, index) => answers[index] === q.answer); const bloom = Object.entries(quiz.questions.reduce<Record<string, number>>((acc, q) => ({ ...acc, [q.bloom_level]: (acc[q.bloom_level] ?? 0) + 1 }), {})).map(([name, value]) => ({ name, value })); return { correct, wrong: quiz.questions.length - correct.length, score: Math.round((correct.length / quiz.questions.length) * 100), bloom }; }, [answers, quiz]);
  if (!quiz || !result) return <main className="mx-auto max-w-3xl px-6 py-12"><Card>No completed quiz found.</Card></main>;
  return <main className="mx-auto max-w-6xl px-6 py-10"><h1 className="mb-6 text-4xl font-black">Results</h1><div className="grid gap-5 md:grid-cols-3"><Card><p className="text-muted-foreground">Score</p><p className="text-5xl font-black">{result.score}%</p></Card><Card><p className="text-muted-foreground">Correct Answers</p><p className="text-5xl font-black text-green-300">{result.correct.length}</p></Card><Card><p className="text-muted-foreground">Wrong Answers</p><p className="text-5xl font-black text-red-300">{result.wrong}</p></Card></div><div className="mt-6 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]"><Card><h2 className="text-xl font-bold">Bloom Taxonomy Analysis</h2><div className="h-72"><ResponsiveContainer><PieChart><Pie data={result.bloom} dataKey="value" nameKey="name" outerRadius={90} label>{result.bloom.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer></div></Card><Card><h2 className="text-xl font-bold">Answer Review</h2><div className="mt-4 space-y-4">{quiz.questions.map((q, index) => <div key={q.question} className="rounded-2xl bg-white/5 p-4"><p className="font-semibold">{index + 1}. {q.question}</p><p className="mt-2 text-sm text-green-300">Correct: {q.answer}</p>{answers[index] !== q.answer ? <p className="text-sm text-red-300">Your answer: {answers[index] ?? "Not answered"}</p> : null}</div>)}</div></Card></div></main>;
}
