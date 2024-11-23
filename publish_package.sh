#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting package publication process...${NC}"

# Ensure we're in the correct directory
if [ ! -f "setup.py" ]; then
    echo "Error: setup.py not found. Are you in the correct directory?"
    exit 1
fi

# Function to check if command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 successful${NC}"
    else
        echo -e "${YELLOW}✗ $1 failed${NC}"
        exit 1
    fi
}

# Add all changes
echo "Adding all changes..."
git add .
check_status "Git add"

# Commit changes
echo "Committing changes..."
git commit -m "Prepare for package publication"
check_status "Git commit"

# Create and switch to develop branch for TestPyPI
echo "Creating and switching to develop branch..."
git checkout -b develop 2>/dev/null || git checkout develop
check_status "Switch to develop branch"

# Push to develop for TestPyPI
echo "Pushing to develop branch for TestPyPI..."
git push origin develop --force
check_status "Push to develop"

# Function to increment version
increment_version() {
    local version=$1
    local major minor patch
    IFS='.' read -r major minor patch <<< "$version"
    patch=$((patch + 1))
    echo "$major.$minor.$patch"
}

# Create and push tag for PyPI
echo "Creating new version tag..."
BASE_VERSION=$(python3 -c "import setup; print(setup.VERSION)" 2>/dev/null || echo "0.1.0")
VERSION=$BASE_VERSION

# Keep incrementing version until we find one that doesn't exist
while git rev-parse "v$VERSION" >/dev/null 2>&1; do
    echo -e "${YELLOW}Version v$VERSION already exists, incrementing...${NC}"
    VERSION=$(increment_version "$VERSION")
done

echo "Using version: v$VERSION"
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
check_status "Create tag"

echo "Pushing tag..."
git push origin "v${VERSION}"
check_status "Push tag"

echo -e "${GREEN}All done! Now:${NC}"
echo "1. Go to GitHub and create a release from tag v${VERSION}"
echo "2. Check the Actions tab to monitor the publishing process"
echo "3. Once complete, verify on PyPI: https://pypi.org/project/processportmonitor/"
echo "4. And TestPyPI: https://test.pypi.org/project/processportmonitor/"

# Optional: Open relevant URLs in browser
if command -v open >/dev/null; then
    echo -e "${YELLOW}Opening relevant URLs...${NC}"
    open "https://github.com/cenab/ProcessPortMonitor/releases/new"
    open "https://github.com/cenab/ProcessPortMonitor/actions"
fi