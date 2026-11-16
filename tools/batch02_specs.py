"""Batch 02 pin specs (Monday run 16 Nov 2026): 30 pins for 20-29 Nov 2026, 3 a day.
Allocation: established products (networth, planner, portfolio, smallbiz) 2 each; new this batch
(endoflife, bookkeeping) 4 each; the 7 invoice-template trades 2 each (all on the 'Invoice Templates UK' board).
Bookkeeping is 'style: bold': 3 of its 4 pins use the bold template.
Every number on a pin is read from tools/screens/ (example data) or the registry notes.
Dict order sets the round-robin, which spreads the shared invoice board to at most twice a day."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "screens") + "/"
REG = json.load(open(os.path.join(HERE, "products.json")))["products"]
GS = " Instant download for Google Sheets and Excel."
END = {
    "networth": " Planning tool, not financial advice.",
    "portfolio": " Tracking tool, not financial advice.",
    "smallbiz": " Tracking tool, not financial advice.",
    "endoflife": " An organiser, not legal advice.",
    "bookkeeping": " Record-keeping tool, not tax advice.",
    "planner": "",
}
INV_END = " Invoice template, not tax advice."
EOL_BADGE = "Fillable PDF · Printable · Tracker"
BK_CTA = "UK Bookkeeping & Self Assessment Tracker"


def P(key, pins):
    r = REG[key]
    assert r["live"] and r["link"], key
    end = END.get(key, INV_END)
    for p in pins:
        p["desc"] = p["desc"] + end
    return dict(board=r["board"], link=r["link"], kw=r["kw"], pins=pins)


PRODUCTS = {
 "networth": P("networth", [
    dict(template="closeup", screen=S + "networth/freedom.png", crop=(0, 0, 0.618, 1),
         callout_label="EXAMPLE: LIQUID MONEY COVERS", callout_value="17.0 months",
         title_overlay="Your Life Freedom Formula", accent="Freedom", sub="Months your liquid money covers your costs",
         note="Example figures from the included sample data",
         title="Net Worth Tracker Spreadsheet: How Many Months Your Liquid Money Covers",
         desc="The Life Freedom Formula divides your liquid money by your monthly living costs, less any passive income, "
              "to show how many months it would last. Sits beside your net worth and 10-year forecast. "
              "Example and blank files, £ and $ versions." + GS),
    dict(template="seasonal", big="2027", title_overlay="Plan the changes 2027 brings", accent="changes",
         sub="Dated life changes, month by month", product="Net Worth Tracker 2027", screen=S + "networth/dash.png",
         title="Net Worth Tracker Spreadsheet 2027: Plan Life Changes Month by Month",
         desc="Add dated life changes in Future Plans, like a drop in pay for maternity leave, nursery costs or paying more into a pension, "
              "and see the effect month by month and on your 10-year net worth forecast. Start the new year with every number in one place." + GS),
 ]),
 "invoices-plumber": P("invoices-plumber", [
    dict(template="features", kicker="Plumbing invoice template", title_overlay="Built for plumbing and heating", accent="plumbing",
         screen=S + "invoices-plumber/price-list.png", bullets=["Boiler, CP12 and radiator items", "Gas Safe no. on every quote",
         "CIS on labour, not materials", "Quote to invoice in one step"],
         title="Plumbing Invoice Template UK: Quotes and Invoices for Plumbing and Heating",
         desc="A plumber's quote and invoice template with a ready price list: boiler services, landlord gas safety records, combi swaps, "
              "radiators and leak repairs. Your Gas Safe and WaterSafe numbers print on every quote. Edit the example prices to your own. No macros." + GS),
    dict(template="closeup", screen=S + "invoices-plumber/invoice-totals.png", crop=(0.5, 0, 1, 0.3),
         callout_label="EXAMPLE: CIS AT 20% OF LABOUR", callout_value="£912.00",
         title_overlay="CIS worked out for you", accent="CIS", sub="Labour only, with reverse charge VAT",
         note="Example data shown",
         title="Plumbing Invoice Template with CIS Deduction and Reverse Charge VAT",
         desc="Working as a CIS subcontractor? Mark lines as labour or materials and the invoice takes the CIS deduction from labour only, "
              "adds the reverse charge VAT wording and shows the amount due. No macros." + GS),
 ]),
 "endoflife": P("endoflife", [
    dict(template="hero", tag="ENGLAND · WALES · SCOTLAND · NI", title_overlay="UK End of Life Planner", accent="Planner",
         sub="Everything your family needs, in one place", screen=S + "endoflife/cover.png",
         badge=EOL_BADGE, footer="Instant download · A4",
         title="End of Life Planner UK: If I Die Binder for England, Wales, Scotland and NI",
         desc="Gather the information your family would need, calmly and in one place: who to call, where your will is, your money, "
              "pensions, policies, digital life and wishes. Fillable A4 PDF, a printable copy and a linked tracker, written for each UK nation."),
    dict(template="features", kicker="If I die binder UK", title_overlay="Every account, easy to find", accent="easy to find",
         screen=S + "endoflife/tracker.png", bullets=["Accounts and policies listed", "Flags anything not checked", "Yearly review date",
         "Totals kept separate"], badge=EOL_BADGE,
         title="End of Life Planner Tracker: Accounts, Pensions and Policies in One List",
         desc="The linked tracker lists every bank account, ISA, pension, policy and debt, flags anything not checked in 12 months "
              "and reminds you when your yearly review is due. Money, pensions, insurance cover and debts are kept as separate totals."),
    dict(template="statement", statement="A calm checklist for the people you love.", sub="End of life planner UK",
         product="UK End of Life Planner", screen=S + "endoflife/checklist.png", badge=EOL_BADGE,
         title="End of Life Planner UK: A What-To-Do-First Checklist for Your Family",
         desc="Section 17 is a step-by-step list for whoever sorts things out: registering, Tell Us Once, finding the will, "
              "contacting banks and pensions, and probate or confirmation, with the differences for each UK nation."),
    dict(template="seasonal", big="2027", title_overlay="Your affairs, in order", accent="in order",
         sub="A calm job for the turn of the year", product="UK End of Life Planner", screen=S + "endoflife/cover.png",
         badge="Fillable PDF · Printable · Instant download",
         title="End of Life Planner UK: Get Your Affairs in Order Before the New Year",
         desc="Use the quiet weeks before 2027 to write down what your family would need: contacts, accounts, pensions, wishes "
              "and where your will is kept. Includes UK will templates with signing guidance for each nation."),
 ]),
 "planner": P("planner", [
    dict(template="hero", tag="NEW YEAR PLANNING", title_overlay="Set your 2027 goals now", accent="2027 goals",
         sub="Ready to start Monday 4 January", screen=S + "planner/dash.png", footer="UK + US dates · Instant download",
         title="12 Week Year Planner 2027: Set Your Goals Before January",
         desc="Write up to 6 goals for 2027, break them into tasks with hour estimates and let the planner set a weekly pace. "
              "Starts Monday 4 January 2027 by default, or pick your own date." + GS),
    dict(template="statement", statement="Small weekly hours, big yearly goals.", sub="12 week goal planner spreadsheet",
         product="12 Week Goal Planner 2027", screen=S + "planner/weekly.png",
         title="12 Week Year Planner: Small Weekly Hours Toward Big 2027 Goals",
         desc="Each week, book your hours, tick off up to 8 habits and get a score from hours done against hours planned. "
              "A review week closes every 12-week block." + GS),
 ]),
 "invoices-electrician": P("invoices-electrician", [
    dict(template="hero", tag="ELECTRICIANS", title_overlay="Electrician quotes, done right", accent="quotes",
         sub="NICEIC and Part P details on every page", screen=S + "invoices-electrician/quote-page.png",
         footer="Quote · Invoice · Payments · Instant download",
         title="Electrician Invoice Template UK: Quotes with Your NICEIC and Part P Details",
         desc="An electrician's quote and invoice template: your NICEIC number, Part P registration and insurance print on every quote. "
              "Turn an agreed quote into an invoice and log payments as they come in. No macros." + GS),
    dict(template="statement", statement="EICRs to rewires, already listed.", sub="Electrical quote template UK",
         product="Electrician Invoice Template", screen=S + "invoices-electrician/price-list.png",
         title="Electrician Invoice Template: Price List for EICRs, Consumer Units and EV Chargers",
         desc="Starts with an electrician's price list: EICRs by size of home, consumer unit swaps, EV charger installs, sockets, "
              "downlights and full rewires. Replace the example prices with your own and pick them on each quote. No macros." + GS),
 ]),
 "bookkeeping": P("bookkeeping", [
    dict(template="bold", tag="SELF-EMPLOYED", hook="Self-employed? Know your numbers before 31 January.", accent="31 January.",
         answer="Your tax return totals, box by box", screen=S + "bookkeeping/yearend.png", crop=(0, 0, 1, 0.55), cta=BK_CTA,
         title="Small Business Bookkeeping Spreadsheet UK: Know Your Numbers Before 31 January",
         desc="Log income and costs as you go and the Year-End Summary lays out your self-employment totals by Self Assessment box, "
              "with allowable and not-allowable costs split for you. For sole traders and landlords." + GS),
    dict(template="bold", bg="teal", hook="Let out a flat as well as running a business?", accent="flat",
         answer="Property income tracked alongside", screen=S + "bookkeeping/landlord.png", crop=(0, 0, 1, 0.55), cta=BK_CTA,
         title="Small Business Bookkeeping Spreadsheet for Sole Traders Who Are Also Landlords",
         desc="Track up to three rental properties beside your business: your share of income, expenses and finance costs, "
              "and whether the £1,000 property allowance or your expenses is the larger deduction." + GS),
    dict(template="bold", hook="Do you know your profit this month?", accent="profit",
         answer="Net profit, costs and tax pot at a glance", screen=S + "bookkeeping/dashboard.png", crop=(0, 0, 0.5, 1), cta=BK_CTA,
         title="Small Business Bookkeeping Tracker UK: Your Profit This Month at a Glance",
         desc="The dashboard shows gross and net profit, average running costs, cash in the bank and a tax pot at your own percentage, "
              "all from what you've logged so far this tax year." + GS),
    dict(template="seasonal", big="31 Jan", title_overlay="Self Assessment, sorted early", accent="sorted",
         sub="Totals by box for your tax return", product="Bookkeeping & Self Assessment Tracker",
         screen=S + "bookkeeping/yearend.png",
         title="Small Business Bookkeeping and Self Assessment: Get Ahead of 31 January",
         desc="Get your records in order before the 31 January Self Assessment deadline. Income, costs, mileage and use of home "
              "come together in a Year-End Summary laid out by box." + GS),
 ]),
 "invoices-builder": P("invoices-builder", [
    dict(template="features", kicker="CIS invoice template for builders", title_overlay="Day rates and m² prices", accent="m²",
         screen=S + "invoices-builder/price-list.png", bullets=["Builder, bricklayer, plasterer", "Brickwork and blockwork per m²",
         "Skip and scaffold hire", "CIS on labour lines only"],
         title="Builder Invoice Template UK: Day Rates, Per m² Prices and CIS",
         desc="A builder's quote and invoice template with a ready price list: trade day rates, brickwork and blockwork per m², "
              "foundations per metre, skip and scaffold hire. Labour lines carry the CIS deduction; materials don't. No macros." + GS),
    dict(template="statement", statement="CIS taken from labour, never materials.", sub="CIS invoice template UK",
         product="Builder CIS Invoice Template", screen=S + "invoices-builder/invoice-totals.png", anchor=(1, 0),
         title="Builder Invoice Template with CIS Deduction and Domestic Reverse Charge",
         desc="Subcontracting on a site? The invoice works out the 20% CIS deduction on labour, adds the reverse charge VAT wording "
              "and shows the amount due, with your UTR printed underneath. No macros." + GS),
 ]),
 "portfolio": P("portfolio", [
    dict(template="features", kicker="Investment portfolio tracker", title_overlay="See it all before 2027", accent="2027",
         screen=S + "portfolio/table.png", bullets=["Stocks, ETFs and crypto", "Cash savings and property", "Return a year by account",
         "Example and blank copy"],
         title="Investment Portfolio Tracker Spreadsheet: Every Asset Class Before 2027",
         desc="Bring stocks and ETFs, crypto, cash savings and property into one workbook before the new year. "
              "See value, gain and a money-weighted return a year by class and by account." + GS),
    dict(template="closeup", screen=S + "portfolio/kpi.png", callout_label="EXAMPLE: WHOLE PORTFOLIO, A YEAR",
         callout_value="+7.1%", title_overlay="One return for everything", accent="return",
         sub="Deposits and withdrawals allowed for", note="Example data shown (included sample portfolio)",
         title="Investment Portfolio Tracker: One Yearly Return Across Every Account",
         desc="A money-weighted return a year for the whole portfolio, so new deposits don't make it look better than it is. "
              "Five dashboards: one overall and one per asset class." + GS),
 ]),
 "invoices-cleaning": P("invoices-cleaning", [
    dict(template="closeup", screen=S + "invoices-cleaning/room-prices.png", crop=(0, 0, 0.6, 0.5),
         callout_label="EXAMPLE: WEEKLY CLEAN DISCOUNT", callout_value="10% off",
         title_overlay="Price a clean by its rooms", accent="rooms", sub="Regular, deep, end of tenancy, one-off",
         note="Example prices: use your own",
         title="Cleaning Invoice Template UK with a Room-by-Room Quote Calculator",
         desc="Type the bedrooms, bathrooms and other rooms, pick the type of clean and how often, add extras like an oven clean, "
              "and the room calculator prices the quote, with weekly and fortnightly discounts and a minimum charge. No macros." + GS),
    dict(template="features", kicker="Cleaning invoice template", title_overlay="Deep cleans to end of tenancy", accent="end of tenancy",
         screen=S + "invoices-cleaning/price-list.png", bullets=["Regular and deep clean prices", "Holiday let changeovers",
         "Oven, carpet and window extras", "Your DBS check on quotes"],
         title="Cleaning Invoice Template UK: Regular, Deep and End of Tenancy Cleans",
         desc="A cleaner's quote and invoice template with a ready price list: regular cleans, deep cleans and end of tenancy by size of home, "
              "holiday let changeovers and extras. Your insurance and DBS details print on every quote. No macros." + GS),
 ]),
 "smallbiz": P("smallbiz", [
    dict(template="statement", statement="Work back from the take-home you want.", sub="Small business profit tracker",
         product="Small Business Profit Tracker", screen=S + "smallbiz/needs.png",
         title="Small Business Profit Tracker: Work Back From the Take-Home You Want",
         desc="Set the take-home you want and the tracker works out the profit, sales, orders and shop visits you need a year, "
              "a month and a week, from your own numbers." + GS),
    dict(template="seasonal", big="2027", title_overlay="Set your 2027 sales target", accent="sales target",
         sub="And check your pace every month", product="Small Business Profit Tracker", screen=S + "smallbiz/dash.png",
         title="Small Business Profit Tracker 2027: Set Your Sales Target for the New Year",
         desc="Plan the new year from your numbers: the sales you need each month, your profit and loss, and a monthly pace check "
              "against your goal." + GS),
 ]),
 "invoices-gardener": P("invoices-gardener", [
    dict(template="features", kicker="Landscaping invoice template", title_overlay="Mowing, hedges and patios", accent="patios",
         screen=S + "invoices-gardener/price-list.png", bullets=["Hedges per metre, turf per m²", "Garden clearance day rates",
         "Patio and fencing prices", "Waste carrier no. on quotes"],
         title="Landscaping Invoice Template UK: Gardening and Landscaping Price List",
         desc="A gardener's quote and invoice template with a ready price list: mowing, hedge cutting per metre, turfing per m², "
              "garden clearance, patios and fencing. Your waste carrier licence and insurance print on every quote. No macros." + GS),
    dict(template="hero", tag="GARDENERS · LANDSCAPERS", title_overlay="Winter clearance quotes", accent="Winter",
         sub="From quote to paid, in one workbook", screen=S + "invoices-gardener/quote-page.png",
         footer="Quote · Invoice · Payments · Instant download",
         title="Landscaping Invoice Template: Quotes for Winter Garden Clearance Jobs",
         desc="Quote winter clearance and tidy-up jobs from your own price list, turn the agreed quote into an invoice and log "
              "payments as they arrive. Invoices show Paid, Part paid or Overdue. No macros." + GS),
 ]),
 "invoices-handyman": P("invoices-handyman", [
    dict(template="features", kicker="Handyman invoice template UK", title_overlay="Every odd job, priced", accent="priced",
         screen=S + "invoices-handyman/price-list.png", bullets=["Half-day and full-day rates", "Flat-pack and TV mounting",
         "Doors, shelves and tiling", "Minimum charge for small jobs"],
         title="Handyman Invoice Template UK: Price List for Every Odd Job",
         desc="A handyman's quote and invoice template with a ready price list: half and full days, a minimum call charge, flat-pack, "
              "TV mounting, doors, shelves, tiling and painting. Edit the example prices to your own. No macros." + GS),
    dict(template="statement", statement="Repair lists quoted in minutes.", sub="Handyman invoice template UK",
         product="Handyman Invoice Template", screen=S + "invoices-handyman/quote-page.png",
         title="Handyman Invoice Template UK: Quote a Landlord's Repairs List Fast",
         desc="Pick lines from your price list to quote a whole list of repairs, print it as an A4 PDF with your insurance and DBS details, "
              "then turn it into an invoice when the job's agreed. No macros." + GS),
 ]),
 "invoices-sole-trader": P("invoices-sole-trader", [
    dict(template="hero", tag="SOLE TRADERS", title_overlay="Quote, invoice, get paid", accent="get paid",
         sub="Set up in 7 simple steps", screen=S + "invoices-sole-trader/start-steps.png",
         footer="Quote · Invoice · Payments · Instant download",
         title="Invoice Template UK for Sole Traders: Quote, Invoice and Get Paid",
         desc="Set up in 7 steps: your details, your price list and your clients. Then make a quote, save it as a PDF, turn it into "
              "an invoice and log payments. Works for any service you sell. No macros." + GS),
    dict(template="closeup", screen=S + "invoices-sole-trader/dashboard.png", crop=(0, 0.04, 0.64, 0.42),
         callout_label="EXAMPLE: OLDEST OVERDUE INVOICE", callout_value="62 days",
         title_overlay="See who owes you", accent="owes", sub="Outstanding, overdue and aged debt",
         note="Example data shown",
         title="Invoice Template UK: See Who Owes You and How Overdue It Is",
         desc="The dashboard shows what you've quoted, invoiced and been paid, what's outstanding, what's overdue and for how long, "
              "plus a VAT threshold check. No macros." + GS),
 ]),
}
