"""Bold hook pins for the UK Bookkeeping & Self Assessment Tracker (Matt, 9 Nov 2026: "be quite good with the
advertising... 'are you ready for self assessment'... bold pictures"). Hook bank + 6 preview specs; the Monday run
uses these (and new variants in the same style) once the product is live in products.json."""
import os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens", "bookkeeping") + "/"
CTA = "UK Bookkeeping & Self Assessment Tracker"
PINS = [
 dict(template="bold", tag="SOLE TRADERS · LANDLORDS", hook="Are you ready for Self Assessment?", accent="Self Assessment?",
      answer="Your tax return totals, box by box", screen=S + "yearend.png", cta=CTA),
 dict(template="bold", bg="teal", hook="Struggling with Self Assessment as a small business owner?", accent="Struggling",
      answer="Log as you go. Totals done for you.", screen=S + "dashboard.png", crop=(0, 0, 0.5, 1), cta=CTA),
 dict(template="bold", hook="Still keeping receipts in a shoebox?", accent="shoebox?",
      answer="Income, costs and miles in one place", screen=S + "dashboard.png", crop=(0, 0, 0.5, 1), cta=CTA),
 dict(template="bold", bg="teal", hook="Driving for work? Your miles add up.", accent="miles add up.",
      answer="55p a mile for the first 10,000", screen=S + "mileage.png", cta=CTA, badge="2026/27 rates · Google Sheets + Excel"),
 dict(template="bold", tag="IF YOUR INCOME IS OVER £30,000", hook="Making Tax Digital in April 2027: are your records ready?",
      accent="records ready?", answer="Quarterly totals laid out for you", screen=S + "quarterly.png", cta=CTA),
 dict(template="bold", bg="teal", hook="How much should you set aside for tax?", accent="set aside",
      answer="Track a tax pot at your own %", screen=S + "dashboard.png", crop=(0, 0, 0.5, 1), cta=CTA),
]
# More hooks for later batches (same rules: questions or plain claims, no fear, no HMRC endorsement, no outcome promises)
HOOKS = ["Is January tax panic your yearly tradition?", "Do you know your profit this month?",
         "Self-employed? Know your numbers before 31 January.", "Let out a flat as well as running a business?",
         "Selling on eBay or Vinted? 30 sales and the platform reports you.", "Work from home? Claim a flat rate for it.",
         "VAT registered? Let the spreadsheet split it out.", "How many months could your business run on its cash?"]

if __name__ == "__main__":
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pinkit
    os.makedirs("out/bold_preview", exist_ok=True)
    paths = [pinkit.render(p, f"out/bold_preview/bookkeeping-bold-{i+1:02d}.png") for i, p in enumerate(PINS)]
    pinkit.contact_sheet(paths, "out/bold_preview/contact.png", cols=3, thumb=420)
    print("\n".join(paths))
