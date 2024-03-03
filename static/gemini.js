import { GoogleGenerativeAI } from "@google/generative-ai";

// Access your API key (see "Set up your API key" above)
API_KEY = "AIzaSyAf9uqaQa3mkQvTqPolRuCYcrpfj1xTYrA"

const genAI = new GoogleGenerativeAI(API_KEY);

async function run() {
  // For text-only input, use the gemini-pro model
  const model = genAI.getGenerativeModel({ model: "gemini-pro"});
  

  const prompt = "Act as a finetuned legal business documents LLM. You will be provided with information about a Partnership Agreement. Your task is to generate a prominent Partnership Agreement based on the provided context. Ensure that the agreement includes appropriate paragraphs and headings. If you encounter any placeholder text enclosed in brackets, such as [Start Date] or [Duration], please replace it with relevant information based on the context. "

  const result = await model.generateContent(prompt);
  const response = await result.response;
  const text = response.text();
  console.log(text);
}
await run();

