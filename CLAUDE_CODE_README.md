# StackedSheets — Project Handoff Document
## For Claude Code continuation

---

## WHAT THIS PROJECT IS

StackedSheets is an Etsy shop selling a debt payoff spreadsheet tracker bundled with PDF guides and printable tools. We're building a 3-listing Etsy store with a data-driven pricing strategy based on extensive competitive research.

**The big pivot (latest decision):** We're creating a flagship product called **"The Debt Freedom Blueprint"** — a 100-140 page step-by-step system modeled after the "Digital Profit Blueprint" format (a product the user purchased). This replaces the thin 8-page Debt Payoff Guide. The Blueprint will be the premium anchor product, with the spreadsheet tracker as a tool INSIDE the system rather than a standalone product.

---

## BRAND IDENTITY

- **Shop name:** StackedSheets
- **Palette:** Charcoal #2B2D31, Emerald #2D8C6F, Sage #F4F7F5, Red accent #C4574B
- **Fonts for PDFs:** Lora (elegant serif, for titles/headings), Poppins (clean sans, for body/UI)
  - Available on system at: `/usr/share/fonts/truetype/google-fonts/`
  - Variants available: Lora-Variable, Lora-Italic-Variable, Poppins-Regular, Poppins-Bold, Poppins-Light, Poppins-Medium, Poppins-Italic, Poppins-BoldItalic, Poppins-LightItalic, Poppins-MediumItalic
- **Fonts for spreadsheets:** Trebuchet MS (warm) + Segoe UI (modern)
- **PDF library:** ReportLab (Python) — all PDFs are generated programmatically
- **PDF cover style:** Full charcoal background, emerald accent bars top/bottom, "S T A C K E D S H E E T S" spaced brand at top with thin line underneath, Lora serif title centered, Poppins-Light subtitle in emerald, "stackedsheets.etsy.com" at bottom in gray italic
- **PDF internal page style:** Charcoal header bar with emerald title + "StackedSheets" subtitle, charcoal footer bar with page info, body in Poppins, section headers as charcoal rounded rect bars with emerald text, tip boxes as sage rounded rects with emerald border, stat boxes as sage rounded rects with emerald border and bold emerald numbers

---

## WHAT'S BEEN BUILT (all files should be in user's downloads)

### Spreadsheets (4 files, all sheet-protected)
1. **DebtPayoffTracker_v5_StackedSheets.xlsx** — Full 9-tab version with example data
   - Tabs: Dashboard, Debts, Snowball, Avalanche, What-If, Snowflakes, Milestones, Countdown, Instructions
   - 20,944 formulas, 0 errors, 345 input cells, 26,432 locked cells
   - Features: Strategy switching (snowball/avalanche), side-by-side comparison, 120-month schedules, what-if scenarios (4 amounts), snowflake bonus payments, milestone tracking with celebrations, countdown with 5 auto-unlocking achievement badges, 24-month progress log
   - Design: Charcoal headers, emerald accents, sage input highlighting, gridlines off, emoji debt categories (💳🎓🚗🏠💰🏥📦)

2. **DebtPayoffTracker_v5_BLANK.xlsx** — Same as above but with no example data (clean start)

3. **DebtPayoffTracker_LITE.xlsx** — Stripped-down 5-tab version for entry-level listing
   - Tabs: Dashboard, Debts, Snowball, Avalanche, Instructions
   - 15,691 formulas, 0 errors, 122 input cells
   - Missing: What-If, Snowflakes, Milestones, Countdown
   - Broken references to removed sheets were cleaned (replaced with 0 or None)

4. **DebtPayoffTracker_LITE_BLANK.xlsx** — Blank version of Lite

### PDFs (7 files)
1. **NegotiationPlaybook_StackedSheets.pdf** — 18 pages, premium Lora cover
   - Content: Part 1 (Rate Negotiation p3-6), Part 2 (Hardship Programs p7-10), Part 3 (Debt Settlement p11-15), Appendices A-C (letter templates p16-18)
   - Covers: 83% rate negotiation success stat, word-for-word phone scripts, bank-specific hardship programs (Amex, Chase, Citi, Discover, BofA), settlement tactics, legal rights (US + UK), letter templates
   - This is substantial and can stay mostly as-is, though internal pages could benefit from the Poppins/Lora font upgrade

2. **DebtPayoffGuide_StackedSheets.pdf** — 8 pages, TO BE REPLACED by the Debt Freedom Blueprint
   - Current version is too thin for the price point
   - Was rebuilt once with Poppins/Lora fonts but content is insufficient

3. **QuickStartGuide.pdf** — 1 page, 3.7KB
4. **MonthlyBudgetSnapshot.pdf** — 1 page, 3.2KB
5. **DebtPayoffColoringChart.pdf** — 2 pages, 20KB
6. **DebtFreeCertificate.pdf** — 1 page, 2.4KB

### Planning/Marketing docs
7. **StackedSheets_Etsy_Listings.md** — Full listing copy (titles, tags, descriptions) for 3 listings. WILL NEED UPDATING after Blueprint is built.
8. **StackedSheets_ShotList.md** — Canva image composition guide with shot list for Excel Online screenshots

---

## PRICING STRATEGY (data-driven, from extensive research)

### Key research findings:
- Most successful Etsy finance spreadsheet shops use **separate listings as tiers** (not in-listing variations)
- Spreadsheet + PDF guide bundles cluster at **$12-$16 effective price**
- **3 tiers is optimal** — 66% of buyers choose the middle option
- **Launch with a sale** (not a cheaper price) to get the sale badge
- Original prices must be genuine per Etsy policy
- **Opt out of Etsy offsite ads** immediately (15% cut is devastating)
- Etsy's fee formula: $0.45 + (9.5% × Sale Price) without offsite ads
- Products at $14.99 have **87.5% margin** after fees
- **Charm pricing** at $X.99 outperforms round numbers by 27%
- **Start at market rate**, not below — low prices signal low quality
- After 20-50 reviews, increase by 10% (recovers in 4-6 weeks)

### Current listing structure (NEEDS REVISION after Blueprint):
| Listing | Original | Launch Sale | Effective |
|---------|----------|-------------|-----------|
| 1. Debt Payoff Tracker | $9.99 | 20% off | $7.99 |
| 2. Debt Payoff Bundle | $18.99 | 20% off | $15.19 |
| 3. Complete Debt Freedom Kit | $29.99 | 20% off | $23.99 |

**This will likely change** now that the Blueprint is the flagship. The Blueprint could be Listing 2 or 3, priced at $29.99-$39.99, with the spreadsheet-only as entry and maybe a mid-tier bundle.

---

## THE NEXT BUILD: DEBT FREEDOM BLUEPRINT

### Concept
A 100-140 page step-by-step system modeled on the "Digital Profit Blueprint" format. Each chapter follows the same structure:
- **Why this chapter matters** (motivation + context)
- **Step-by-step process** (numbered, actionable steps)
- **Worked examples with real numbers** (case studies, calculations)
- **Tools & resources**
- **Key takeaways**
- **Quick win (30-60 minutes)**
- **1-week action plan**
- **Templates & checklists** (fill-in worksheets)

### Draft chapter outline (needs finalization):

**Cover** — Lora serif, charcoal background, same style as existing covers
**Dedication/Intro page**
**Table of Contents**

**Chapter 1: The Debt Landscape** (understanding where you stand)
- Current stats US + UK, breakdown by debt type
- The compound interest trap with worked examples
- What your debt is actually costing you (comparison tables)
- Emergency fund first rule

**Chapter 2: Know Your Numbers** (auditing your debt)
- How to find every debt you owe
- Reading your credit report (free methods US + UK)
- Calculating debt-to-income ratio
- Good debt vs bad debt
- Setting up your tracker (ties to spreadsheet)

**Chapter 3: Choosing Your Strategy** (snowball vs avalanche deep dive)
- Full worked example with 6 debts ("Meet the Johnsons")
- Month-by-month tables for both strategies
- Side-by-side comparison
- When snowball beats avalanche and vice versa
- The hybrid approach
- Decision flowchart

**Chapter 4: Supercharging Your Payoff** (acceleration tactics)
- Interest rate negotiation (preview of Playbook)
- Balance transfer strategy with worked examples
- Debt consolidation: when it helps vs when it's a trap
- The snowflake method
- Finding hidden money (subscriptions, tax credits, selling items)
- Side income ideas ranked by effort/return

**Chapter 5: Debt by Type** (specific strategies)
- Credit cards, student loans (US + UK), auto loans, medical debt, mortgage, personal loans, Buy Now Pay Later
- Each with specific tactics, traps, and opportunities

**Chapter 6: Your Credit Score During Payoff**
- How utilisation works with examples
- Why closing accounts hurts
- The score dip and recovery
- Optimal order for credit health
- Free monitoring tools

**Chapter 7: Negotiating Like a Pro** (condensed from Playbook)
- Rate negotiation basics + scripts
- Hardship programs overview
- Settlement overview
- Full details in the Playbook (upsell to Kit listing)

**Chapter 8: The Psychology of Debt Freedom**
- Debt stress syndrome
- 5 proven motivation strategies
- Lifestyle inflation trap
- Partner disagreements about money
- Debt shame and openness
- Mental health resources

**Chapter 9: 10 Mistakes That Derail Progress**
- Expanded with specific dollar amounts and examples
- No emergency buffer, closing cards, spreading payments, never negotiating, ignoring small amounts, raiding retirement, going alone, stopping retirement contributions, taking on new debt, not tracking

**Chapter 10: Your 30/60/90-Day Action Plan**
- Day 1 quick start
- Week-by-week for first month
- Monthly check-in template
- 6-month and 12-month milestones
- Celebration planning

**Appendix A: Quick Reference Tables**
- APR impact calculator
- Balance transfer break-even
- Debt-to-income ranges
- Monthly budget template

**Appendix B: Letter Templates**
- Rate reduction request
- Hardship request
- Settlement offer
(Or point to Playbook if keeping them separate)

**Closing page** with encouragement and resources

### Design specifications for Blueprint:
- Same cover style as existing (Lora title, charcoal background, emerald accents)
- Internal pages: Poppins body (11pt, 16.5pt leading), Lora for chapter titles
- Wider margins (60px)
- Stat boxes with proper clearance (the old guides had overlap issues — fixed in latest rebuild)
- Section headers as charcoal rounded rect bars
- Tip/callout boxes as sage rounded rects with emerald border
- Checklists with checkbox squares
- Tables with alternating sage/white rows
- Page footer with "StackedSheets · The Debt Freedom Blueprint · Page X"
- Chapter opener pages with larger treatment (like the Digital Profit Blueprint chapter openers)

### Critical spacing rules (learned from user feedback):
- Stat boxes MUST have 20px+ clearance below before next text
- Tip boxes MUST have 18px+ clearance below
- Section headers need 15px+ gap above
- Paragraphs need 8-10px gap between them
- Never let content feel "cramped" — generous whitespace is premium
- Body font minimum 11pt, never smaller than 9.5pt for any text

---

## RESEARCH SOURCES (for content accuracy)

Research was gathered via web search during this project. Key sources used:
- Harvard Business Review study on debt snowball effectiveness (~6,000 consumers)
- Kellogg School of Management research on psychological motivation in debt payoff
- Federal Reserve Bank of New York household debt data
- Bank of England UK personal debt statistics
- CARD Act (US) and FCA Consumer Duty (UK) legal frameworks
- Credit card hardship program details for Amex, Chase, Citi, Discover, BofA
- Etsy pricing research from Customcy (164,584 shops), Marmalead, seller communities

**Important:** The user asked about whether we can claim research sources on the cover — decision was NO, keep covers clean. Sources are mentioned inside the content and in listing descriptions only.

---

## USER PREFERENCES & STYLE NOTES

- User is action-oriented, makes quick decisions
- User correctly challenges assumptions (pushed back on premature pricing decisions, demanded research first)
- User has Excel Online only (no desktop Excel) — important for compatibility notes
- User plans to use Canva for listing mockup images
- User prefers clean, uncluttered design
- User identified readability issues multiple times — spacing and font size are critical
- User bought the "Digital Profit Blueprint" (144 pages, $??) and wants to apply the same step-by-step, template-heavy, action-plan format to the debt niche
- User is "sooooo bad" at screen recordings/video — prefers automated solutions

---

## FILES THAT CAN BE CLEANED UP

These are old/superseded versions in the outputs folder:
- DebtPayoffTracker_v4.xlsx (superseded by v5)
- NegotiationMasterclass_StackedSheets.pdf (renamed to Playbook)
- DebtNegotiationLetters.pdf (integrated into Playbook appendices)
- canva_*.png/jpg files (LibreOffice renders — user said they were bad, will take own screenshots)

---

## IMMEDIATE NEXT STEPS IN CLAUDE CODE

1. **Finalize the Blueprint chapter outline** — get user approval on structure
2. **Build the PDF generation framework** — reusable functions for covers, chapter openers, body text, stat boxes, tip boxes, checklists, tables, action plans
3. **Write and generate chapter by chapter** — content + layout together
4. **Revise the listing strategy** — Blueprint changes the tier structure and pricing
5. **Update listing copy** — new descriptions reflecting the Blueprint as flagship
6. **Consider upgrading the Negotiation Playbook** internal pages to Poppins/Lora too (for consistency)
