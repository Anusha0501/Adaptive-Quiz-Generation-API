"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { toast } from "sonner";
import { generateQuiz, getAnalytics, getQuiz } from "@/services/api";
import type { GenerateQuizRequest } from "@/types/quiz";

export function useGenerateQuiz() {
  return useMutation({
    mutationFn: (payload: GenerateQuizRequest) => generateQuiz(payload),
    onSuccess: () => toast.success("Quiz generated successfully"),
    onError: (error) => toast.error(error.message)
  });
}

export function useQuiz(id: string) { return useQuery({ queryKey: ["quiz", id], queryFn: () => getQuiz(id), enabled: Boolean(id) }); }
export function useAnalytics() { return useQuery({ queryKey: ["analytics"], queryFn: getAnalytics }); }
