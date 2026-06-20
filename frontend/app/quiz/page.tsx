"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import type { QuizResponse } from "@/types/quiz";

export default function QuizPage() {
  const [quiz, setQuiz] = useState<QuizResponse | null>(null);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [seconds, setSeconds] = useState(600);

  useEffect(() => { const stored = sessionStorage.getItem("activeQuiz"); if (stored) setQuiz(JSON.parse(stored)); }, []);
  useEffect(() => { const timer = setInterval(() => setSeconds((value) => Math.max(0, value - 1)), 1000); return () => clearInterval(timer); }, []);
  const progress = useMemo(() => quiz ? Math.round((Object.keys(answers).length / quiz.questions.length) * 100) : 0, [answers, quiz]);

  function finish() { if (!quiz) return; sessionStorage.setItem("quizAnswers", JSON.stringify(answers)); sessionStorage.setItem("completedQuiz", JSON.stringify(quiz)); }
  if (!quiz) return <main className="mx-auto max-w-3xl px-6 py-12"><Card><h1 className="text-3xl font-bold">No active quiz</h1><p className="mt-2 text-muted-foreground">Generate a quiz first to start the assessment.</p><Link href="/quiz-generator" className="mt-6 inline-block"><Button>Generate Quiz</Button></Link></Card></main>;
  const question = quiz.questions[current];
  return <main className="mx-auto max-w-5xl px-6 py-10"><div className="mb-6 grid gap-4 md:grid-cols-3"><Card><p className="text-sm text-muted-foreground">Timer</p><p className="text-3xl font-black">{Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, "0")}</p></Card><Card><p className="text-sm text-muted-foreground">Progress</p><p className="text-3xl font-black">{progress}%</p></Card><Card><p className="text-sm text-muted-foreground">Question</p><p className="text-3xl font-black">{current + 1}/{quiz.questions.length}</p></Card></div><Card><div className="mb-5 h-2 rounded-full bg-white/10"><div className="h-2 rounded-full bg-primary" style={{ width: `${progress}%` }} /></div><p className="text-sm font-semibold text-primary">{question.bloom_level}</p><h1 className="mt-2 text-2xl font-bold">{question.question}</h1><div className="mt-6 grid gap-3">{question.options.map((option) => <button key={option} onClick={() => setAnswers({ ...answers, [current]: option })} className={`rounded-2xl border p-4 text-left transition ${answers[current] === option ? "border-primary bg-primary/20" : "border-white/10 bg-white/5 hover:bg-white/10"}`}>{option}</button>)}</div><div className="mt-8 flex flex-wrap justify-between gap-3"><Button variant="secondary" disabled={current === 0} onClick={() => setCurrent(current - 1)}>Previous</Button><div className="flex flex-wrap gap-2">{quiz.questions.map((_, index) => <button key={index} onClick={() => setCurrent(index)} className={`h-10 w-10 rounded-xl ${index === current ? "bg-primary" : answers[index] ? "bg-green-500/70" : "bg-white/10"}`}>{index + 1}</button>)}</div>{current === quiz.questions.length - 1 ? <Link href="/results" onClick={finish}><Button>Submit Quiz</Button></Link> : <Button onClick={() => setCurrent(current + 1)}>Next</Button>}</div></Card></main>;
}
