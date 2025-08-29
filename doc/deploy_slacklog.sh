# Deploy Slacklog Sphinx HTML to https://rizitis.github.io/slacklog/

set -e

# Prevent running as root
if [ "$EUID" -eq 0 ]; then
    echo "ERROR: Do not run this script as root. Exiting."
    exit 1
fi

# Paths
SPHINX_BUILD_DIR="_build/html"
GITHUB_PAGES_DIR="$HOME/GITHUB/rizitis.github.io/slacklog"

echo "Copying HTML to GitHub Pages..."
rm -rf "$GITHUB_PAGES_DIR"/*
cp -r "$SPHINX_BUILD_DIR"/* "$GITHUB_PAGES_DIR"/

cd "$GITHUB_PAGES_DIR"

echo "We are hacking in https://rizitis.github.io so renaming _folders to avoid Jekyll issues..."
mv _static static
mv _sources sources
mv _modules modules

echo "Updating HTML links...because of Jekyll hacking pages https://rizitis.github.io/slackware/"
find . -name '*.html' -exec sed -i 's|"_static/|"static/|g; s|"_sources/|"sources/|g; s|"_modules/|"modules/|g' {} +

find . -type f -exec sed -i \
  -e 's/_static/static/g' \
  -e 's/_modules/modules/g' \
  -e 's/_sources/sources/g' {} +


echo "Done! Now I must commit and push the changes."
echo ""
