#!/bin/bash
# ESSF pre-deploy script — run locally before FTP upload to eksoach.in
# Usage: bash deploy.sh
# Output: _deploy/ folder — upload its entire contents to public_html/

set -e

SHA=$(git rev-parse --short HEAD)
echo "Building deploy package — SHA: $SHA"

# Clean and recreate deploy dir
rm -rf _deploy
cp -r . _deploy

# Strip everything that should NOT go on the server
rm -rf _deploy/.git
rm -rf _deploy/.github
rm -rf _deploy/.claude
rm -rf _deploy/_deploy
rm -f  _deploy/deploy.sh
rm -f  _deploy/*.md
rm -f  _deploy/FOR_MONTY.html
rm -f  _deploy/PROPOSAL.html
rm -f  _deploy/SESSION_HANDOFF*
rm -rf _deploy/skills/

# Inject current SHA as cache-buster in all HTML files
find _deploy -name "*.html" \
  -exec sed -i '' "s/?v=[a-zA-Z0-9]*\"/?v=${SHA}\"/g" {} +

echo ""
echo "Done. _deploy/ is ready."
echo ""
echo "Upload the contents of _deploy/ to public_html/ on eksoach.in via FTP."
echo "Exclude nothing — .htaccess must be uploaded too."
echo ""
echo "Files to verify after upload:"
echo "  https://eksoach.in/              → Home page"
echo "  https://eksoach.in/pages/executives.html"
echo "  https://eksoach.in/pages/past-events.html"
echo "  https://eksoach.in/pages/social-activity.html"
echo "  https://eksoach.in/pages/contact.html"
