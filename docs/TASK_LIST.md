### Task List

1. **Repository guidelines**
   - Design classes and modules with a single responsibility, keeping an object-oriented approach
   - Keep logic modules under 350 lines, with an average of ~300 lines per file overall
   - Run `pytest` and `python harvester.py` whenever modifying code, and avoid committing generated files such as logs or `__pycache__`

2. **Core feature development**
   - Build scrapers for Craigslist, Reddit, RemoteOK, and WeWorkRemotely, and provide an extensible `extra_sources/` folder for additional custom scrapers
   - Implement a lead-scoring engine that evaluates keyword matches, urgency, budget, decision‑maker language, and DM friendliness
   - Produce ranked outputs in CSV, Markdown, and JSON formats, sorted by score and recency
   - Create an outreach generator offering price suggestions, ready-to-send DM templates, and multiple tone options
   - Add an alert system with optional Telegram notifications and configurable score thresholds

3. **Technical setup**
   - Use Python 3.10+ with libraries such as requests, BeautifulSoup4, PyYAML, python-dateutil, lxml, and sqlite3
   - Provide a `config.yaml` for keywords, cities, budget ranges, scoring weights, and Telegram settings; store data in SQLite with CSV/Markdown exports and support pluggable extra scrapers

4. **Success metrics and constraints**
   - Aim for 3–5 high-quality leads per day, at least one closed job per two days, and outreach generation in under two minutes per lead
   - Track KPIs: lead quality score ≥10, response rate ≥30%, close rate ≥10%, and daily potential revenue ≥$300
   - Avoid Upwork/Fiverr scraping, heavy NLP/AI classification in v1, and any payment gateway integration

5. **Roadmap milestones**
   - Phase 1 (v1.0 – MVP): implement core features and manual DM sending
   - Phase 2 (v1.5): add LinkedIn/Twitter scrapers and an automated lead-response tracker
   - Phase 3 (v2.0): integrate AI-based DM rewriting and optional automatic sending via APIs
