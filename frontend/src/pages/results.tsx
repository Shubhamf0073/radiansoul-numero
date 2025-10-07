"use client";
import { useEffect, useState } from "react";
import { VStack, Heading, Spinner } from "@chakra-ui/react";
import NumberCard from "../components/NumberCard";
import CombinedAnalysis from "../components/CombinedAnalysis";

interface Result {
  title: string;
  number: number;
  interpretation: string;
}

export default function ResultsPage() {
  const [results, setResults] = useState<Result[]>([]);
  const [combined, setCombined] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchResults() {
      try {
        const res = await fetch("http://127.0.0.1:8000/numerology-results?name=Shubham&dob=1995-10-04");
        const data = await res.json();
        
        // Example structure: { numbers: [{title, number, interpretation}], combined: "summary text" }
        setResults(data.numbers);
        setCombined(data.combined);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchResults();
  }, []);

  if (loading) return <Spinner size="xl" />;

  return (
    <VStack spacing={6} p={6}>
      <Heading>Numerology Results</Heading>

      {results.map((r) => (
        <NumberCard key={r.title} title={r.title} number={r.number} interpretation={r.interpretation} />
      ))}

      <CombinedAnalysis summary={combined} />
    </VStack>
  );
}
