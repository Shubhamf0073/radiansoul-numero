"use client";

import { ReactNode } from "react";
import { Box, Flex, Spacer, HStack, Link as ChakraLink } from "@chakra-ui/react";
import NextLink from "next/link";

type LayoutProps = {
  children: ReactNode;
};

export default function Layout({ children }: LayoutProps) {
  return (
    <Box>
      {/* Navbar */}
      <Flex
        as="nav"
        bg="purple.600"
        color="white"
        padding={4}
        align="center"
      >
        <Box fontWeight="bold" fontSize="xl">
          <NextLink href="/">RadianSoul</NextLink>
        </Box>
        <Spacer />
        <HStack spacing={4}>
          <ChakraLink as={NextLink} href="/" _hover={{ textDecoration: "underline" }}>
            Home
          </ChakraLink>
          <ChakraLink as={NextLink} href="/about" _hover={{ textDecoration: "underline" }}>
            About
          </ChakraLink>
          <ChakraLink as={NextLink} href="/services" _hover={{ textDecoration: "underline" }}>
            Services
          </ChakraLink>
          <ChakraLink as={NextLink} href="/contact" _hover={{ textDecoration: "underline" }}>
            Contact
          </ChakraLink>
        </HStack>
      </Flex>

      {/* Page Content */}
      <Box>{children}</Box>

      {/* Footer */}
      <Box bg="purple.600" color="white" textAlign="center" py={4} mt={8}>
        © {new Date().getFullYear()} RadianSoul. All rights reserved.
      </Box>
    </Box>
  );
}
