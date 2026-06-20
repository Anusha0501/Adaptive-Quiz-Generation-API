export type Difficulty = "easy" | "medium" | "hard";
export type BloomLevel = "Remember" | "Understand" | "Apply" | "Analyze" | "Evaluate" | "Create";

export interface Question {
  question: string;
  options: string[];
  answer: string;
  bloom_level: BloomLevel;
  difficulty_score: number;
  validation_score: number;
}

export interface QuizResponse {
  id: string;
  topic: string;
  difficulty: Difficulty;
  questions: Question[];
}

export interface GenerateQuizRequest {
  topic: string;
  difficulty: Difficulty;
  numberOfQuestions: number;
}

export interface AnalyticsSummary {
  quiz_count: number;
  average_generation_ms: number;
}
