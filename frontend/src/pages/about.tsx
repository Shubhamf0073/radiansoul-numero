"use client";

import Layout from "../components/Layout";
import { Box, Text } from "@chakra-ui/react";

export default function AboutPage() {
  return (
    <Layout>
      <Box py={12} textAlign="center">
        <Text fontSize="2xl" color="purple.600">About RadianSoul</Text>
        <Text mt={4} color="gray.700">
          This page will contain info about platform and vision.
        </Text>
      </Box>
    </Layout>
  );
}
