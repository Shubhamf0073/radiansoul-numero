"use client";
import { Box, Text, VStack } from "@chakra-ui/react";

interface NumberCardProps {
  title: string;
  number: number;
  interpretation: string;
}

export default function NumberCard({ title, number, interpretation }: NumberCardProps) {
  return (
    <Box borderWidth="1px" borderRadius="lg" p={4} bg="white" shadow="md">
      <VStack spacing={2} align="start">
        <Text fontWeight="bold" fontSize="lg">{title} - {number}</Text>
        <Text>{interpretation}</Text>
      </VStack>
    </Box>
  );
}
