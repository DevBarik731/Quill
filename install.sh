#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"

echo "Installing Quill Notes App..."

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Create the wrapper script
cat << EOF > "$BIN_DIR/quill"
#!/bin/bash
python3 "$APP_DIR/quill.py" "\$@"
EOF

# Make the wrapper executable
chmod +x "$BIN_DIR/quill"

echo "Quill installed successfully!"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "It looks like $BIN_DIR is not in your PATH."
    read -p "Would you like to add it to your profile (e.g. ~/.bashrc, ~/.zshrc)? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PROFILE=""
        if [[ "$SHELL" == *"zsh"* ]]; then
            PROFILE="$HOME/.zshrc"
        elif [[ "$SHELL" == *"bash"* ]]; then
            PROFILE="$HOME/.bashrc"
        fi
        
        if [ -n "$PROFILE" ]; then
            echo "" >> "$PROFILE"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$PROFILE"
            echo "Added to $PROFILE. Please run 'source $PROFILE' or restart your terminal to apply changes."
        else
            echo "Could not detect shell profile. Please add 'export PATH=\"\$HOME/.local/bin:\$PATH\"' manually."
        fi
    else
        echo "Please add $BIN_DIR to your PATH manually."
    fi
fi

echo "You can now run 'quill' from your terminal."
