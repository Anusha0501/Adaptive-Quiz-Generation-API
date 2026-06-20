import type { AnalyticsSummary, GenerateQuizRequest, QuizResponse } from "@/types/quiz";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers }
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function generateQuiz(payload: GenerateQuizRequest): Promise<QuizResponse> {
  return request<QuizResponse>("/generate-quiz", {
    method: "POST",
    body: JSON.stringify({ topic: payload.topic, difficulty: payload.difficulty, number_of_questions: payload.numberOfQuestions })
  });
}

export async function getQuiz(id: string): Promise<QuizResponse> { return request<QuizResponse>(`/quiz/${id}`); }
export async function getAnalytics(): Promise<AnalyticsSummary> { return request<AnalyticsSummary>("/analytics"); }
