#!/usr/bin/env bash
set -euo pipefail

# Change this Git repository from HTTPS to SSH.
# This script does not make SSH keys or push code.

git remote set-url origin git@github.com:yassineedev/pac-man.git
echo "Remote URL:"
git remote -v
echo "Testing SSH with GitHub..."
ssh -T git@github.com || true
echo "If GitHub said 'successfully authenticated', SSH is ready."
