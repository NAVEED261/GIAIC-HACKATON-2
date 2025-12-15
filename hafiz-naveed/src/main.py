"""
Hackathon-2 Phase-1: Console-Based Todo System

An AI-native, specification-driven Task Management System
designed to manage personal and professional work across
scalable cloud architectures.

This module serves as the application entry point for the
Phase-1 console CLI implementation.
"""

from cli import HafizNaveed


def main() -> None:
    """Initialize and run the Todo application."""
    app = HafizNaveed()
    app.run()


if __name__ == "__main__":
    main()
