"use client";
import { useState } from "react";
import { Box, Input, Button, Text, VStack } from "@chakra-ui/react";

export default function NameAnalysis() {
  const [name, setName] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name) return;
    setLoading(true);

    try {
      const res = await fetch(`/api/name-analysis?name=${encodeURIComponent(name)}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Something went wrong" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={6}>
      <VStack spacing={4}>
        <Input
          placeholder="Enter full name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Button colorScheme="purple" onClick={handleSubmit} isLoading={loading}>
          Analyze
        </Button>

        {result && (
          <Box mt={6} p={4} borderWidth={1} borderRadius="md">
            {result.error ? (
              <Text color="red.500">{result.error}</Text>
            ) : (
              <pre>{JSON.stringify(result, null, 2)}</pre>
            )}
          </Box>
        )}
      </VStack>
    </Box>
  );
}