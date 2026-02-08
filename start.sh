#!/bin/bash

echo "========================================"
echo "  ChatGPT to Gemini Migration Tool"
echo "========================================"
echo ""

while true; do
    echo "What would you like to do?"
    echo ""
    echo "1. View the Guide (open index.html)"
    echo "2. Run Migration (convert conversations)"
    echo "3. View Conversations (start viewer)"
    echo "4. Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice

    case $choice in
        1)
            echo ""
            echo "Opening guide in your browser..."
            if command -v xdg-open > /dev/null; then
                xdg-open index.html
            elif command -v open > /dev/null; then
                open index.html
            else
                echo "Please open index.html manually in your browser"
            fi
            echo ""
            ;;
        2)
            echo ""
            echo "Running migration script..."
            echo ""
            python3 migrate_to_gemini.py
            echo ""
            echo "Migration complete!"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            echo ""
            echo "Starting conversation viewer..."
            echo "Your browser will open automatically."
            echo "Press Ctrl+C to stop the server when done."
            echo ""
            python3 view_conversations.py
            ;;
        4)
            echo ""
            echo "Thank you for using ChatGPT to Gemini Migration Tool!"
            echo ""
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            echo ""
            ;;
    esac
done
