#!/usr/bin/env python3
"""
Main entry point for the Todo Console Application.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colorama import Fore, Style, init

# Initialize colorama
init()

from src.cli.menu import Menu


def main():
    """
    Main function to run the Todo Console Application.
    """
    print(f"{Fore.CYAN}Welcome to the Todo Console Application!{Style.RESET_ALL}")
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()