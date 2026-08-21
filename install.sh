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
echo "You can now run 'quill' from your terminal."
echo "(Ensure that ~/.local/bin is in your system PATH)"
