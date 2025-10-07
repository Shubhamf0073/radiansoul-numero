"use client";

import Layout from "../components/Layout";
import { Box, Text } from "@chakra-ui/react";

export default function ContactPage() {
  return (
    <Layout>
      <Box py={12} textAlign="center">
        <Text fontSize="2xl" color="purple.600">Contact Us</Text>
        <Text mt={4} color="gray.700">
          Contact info or a form will go here.
        </Text>
      </Box>
    </Layout>
  );
}
