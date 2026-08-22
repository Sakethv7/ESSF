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
rm -rf _deploy/docs

# Inject current SHA as cache-buster in all HTML files
find _deploy -name "*.html" \
  -exec sed -i '' "s/?v=[a-zA-Z0-9]*\"/?v=${SHA}\"/g" {} +

echo ""
echo "Done. _deploy/ is ready."
echo ""

# Optional automated FTP push — only runs if credentials are set in the
# environment (never commit these). Leaves the manual FileZilla flow as
# the default when they're not set.
if [[ -n "$FTP_HOST" && -n "$FTP_USER" && -n "$FTP_PASS" ]]; then
  if ! command -v lftp >/dev/null 2>&1; then
    echo "FTP_HOST/FTP_USER/FTP_PASS are set but 'lftp' is not installed (brew install lftp)."
    echo "Falling back to manual upload instructions below."
  else
    echo "Pushing _deploy/ to $FTP_HOST:public_html/ via lftp..."
    # Note: no --delete. public_html/ on eksoach.in has legacy files from the
    # old site (cgi-bin/, prayer-web/, Testing/, old .html pages) that this
    # script must never remove — it only uploads/overwrites _deploy/'s files.
    lftp -u "$FTP_USER","$FTP_PASS" "$FTP_HOST" -e "
      set ssl:verify-certificate no;
      mirror -R --verbose _deploy/ public_html/;
      bye
    "
    echo "Upload complete. Spot-check the pages below."
  fi
else
  echo "Upload the contents of _deploy/ to public_html/ on eksoach.in via FTP."
  echo "Exclude nothing — .htaccess must be uploaded too."
  echo "(To automate this step, set FTP_HOST, FTP_USER, FTP_PASS and re-run.)"
fi

echo ""
echo "Files to verify after upload:"
echo "  https://eksoach.in/              → Home page"
echo "  https://eksoach.in/pages/executives.html"
echo "  https://eksoach.in/pages/past-events.html"
echo "  https://eksoach.in/pages/gallery-bharat-mandapam.html  → 222-photo gallery"
echo "  https://eksoach.in/pages/social-activity.html"
echo "  https://eksoach.in/pages/contact.html"
