"use client";

import Layout from "../components/Layout";
import { Box, Text } from "@chakra-ui/react";

export default function HomePage() {
  return (
    <Layout>
      <Box
        height="70vh"
        display="flex"
        alignItems="center"
        justifyContent="center"
        bg="gray.50"
      >
        <Text fontSize="3xl" color="purple.600">
          Numerology Frontend Connected 🎉
        </Text>
      </Box>
    </Layout>
  );
}
