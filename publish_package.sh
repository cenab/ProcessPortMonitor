#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Use Python from virtual environment or system
PYTHON="/opt/homebrew/opt/python@3.11/bin/python3.11"

echo -e "${GREEN}Starting package publication process...${NC}"

# Ensure we're in the correct directory
if [ ! -f "setup.py" ]; then
    echo -e "${RED}Error: setup.py not found. Are you in the correct directory?${NC}"
    exit 1
fi

# Function to check if command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 successful${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        exit 1
    fi
}

# Extract version from setup.py using grep
VERSION=$(grep -E "version='[^']*'" setup.py | cut -d"'" -f2)

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: Could not extract version from setup.py${NC}"
    exit 1
fi

echo -e "${GREEN}Publishing version: ${VERSION}${NC}"

# Check if tag already exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo -e "${RED}Error: Tag v$VERSION already exists. Please increment the version in setup.py${NC}"
    exit 1
fi

# Create and push tag
echo "Creating tag v$VERSION..."
git tag -a "v$VERSION" -m "Version $VERSION"
check_status "Create tag"

# Push tag
echo "Pushing tag..."
git push origin "v$VERSION"
check_status "Push tag"

echo -e "${GREEN}Tag v$VERSION created and pushed successfully!${NC}"
echo -e "${YELLOW}Now create a release on GitHub with tag v$VERSION to trigger PyPI publication${NC}"