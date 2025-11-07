HOW TO LINK YOUR PORTFOLIO TO YOUR TOI AUTHOR PAGE (AUTO-UPDATING)

1) Upload these files to your GitHub repo (kanwardeepsingh-portfolio):
   - index.html (the site file you already have)
   - scripts/scrape_toi.py
   - .github/workflows/update-stories.yml

2) Commit the files to the 'main' branch.

3) Enable GitHub Pages:
   Settings → Pages → Source → Deploy from branch → main → /(root)

4) The GitHub Action will run every day at 02:00 UTC (and you can run it manually).
   It scrapes your TOI author page and writes 'stories.json' in the repo root.

5) Your index.html already auto-loads 'stories.json'. When that file updates,
   your portfolio's "Latest Stories" section updates automatically.

Optional: If Times of India changes page structure, update the scraper logic in scripts/scrape_toi.py.
