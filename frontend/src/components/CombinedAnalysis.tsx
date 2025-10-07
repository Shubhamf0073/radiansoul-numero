"use client";
import { Box, Text } from "@chakra-ui/react";

interface CombinedAnalysisProps {
  summary: string;
}

export default function CombinedAnalysis({ summary }: CombinedAnalysisProps) {
  return (
    <Box borderWidth="1px" borderRadius="lg" p={4} bg="purple.50" shadow="md">
      <Text fontWeight="bold" fontSize="lg" mb={2}>Combined Analysis</Text>
      <Text>{summary}</Text>
    </Box>
  );
}
