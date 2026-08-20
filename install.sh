#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"

echo "Installing Quill Notes App..."

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Create the wrapper script
cat << EOF > "$BIN_DIR/Quill"
#!/bin/bash
python3 "$APP_DIR/notes_app.py" "\$@"
EOF

# Make the wrapper executable
chmod +x "$BIN_DIR/Quill"

echo "Quill installed successfully!"
echo "You can now run 'Quill' from your terminal."
echo "(Ensure that ~/.local/bin is in your system PATH)"
