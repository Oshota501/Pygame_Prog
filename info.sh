echo "Python Code ...\n"
git ls-files | grep '.py$' | xargs wc -l
echo ""
git ls-files | grep '.pyi$' | xargs wc -l

echo "\nC++ Code ...\n"
git ls-files | grep '.cc$' | xargs wc -l

