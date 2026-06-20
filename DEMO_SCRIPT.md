# Demo Script

1. Open the landing page and describe the product overview, Bloom-aware generation, validation, duplicate detection, and analytics value proposition.
2. Navigate to `/quiz-generator`, enter `PostgreSQL indexing`, select `Medium`, keep `10` questions, and click **Generate Quiz**.
3. Show loading and toast feedback while the frontend calls `POST /generate-quiz`.
4. Complete the quiz in `/quiz`, highlighting timer, navigation buttons, answered-question progress, and Bloom labels.
5. Submit the quiz and review `/results`: score, correct/wrong answers, answer review, and Bloom distribution chart.
6. Open `/analytics` to show quiz history, performance trend graph, difficulty bar chart, and Bloom pie chart.
7. Open backend Swagger at `/docs` to show deployable API contracts.
