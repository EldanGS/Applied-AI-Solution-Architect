from typing import Literal
from pydantic import BaseModel

class Ticket(BaseModel):
    category: Literal["shipping", "billing", "other"]
    order_id: str | None
    urgent: bool

SCHEMA = {**Ticket.model_json_schema(), "additionalProperties": False}

POLICY = """You triage support emails for Acme Shop, an online store for home and kitchen goods. Read one customer email and return one ticket.

# Fields
- category: "shipping", "billing" or "other".
- order_id: the Acme order number, or null.
- urgent: true or false.

# Categories
shipping: getting an order to the customer after it is placed. Delivery dates, tracking that does not move, lost parcels, a parcel marked delivered that never arrived, a wrong or changed address, damage in transit, items missing from the box, upgrading delivery speed, courier problems, and cancelling an order that has not shipped yet.
billing: money. Charges, double charges, refunds and refund status, invoices and receipts, promo codes that did not apply, price matching, failed payments, gift cards, store credit, sales tax, and Acme Plus subscription renewals.
other: everything else. Product questions before buying, how to use a product, warranty claims for a product that broke after normal use, account and password problems, the newsletter, feedback and compliments, job applications, partnership offers, and anything you cannot place.

# Tie-breaks
- Money and delivery in one email: pick what the customer asks you to do. "It never arrived, refund me" is billing: the action is a refund. "Where is my parcel? I paid for express" is shipping: the action is to find the parcel.
- Returns: billing when they ask about the money back, shipping when they ask for a label or a pickup.
- Damaged on arrival is shipping. Broke after weeks of normal use is other (warranty).
- A forwarded thread: classify the newest message only.
- Any language: classify by meaning, and still return the fields in English.

# order_id
Acme order numbers are "A-" and four digits, for example A-1001. Normalise what the customer wrote: a1001, A 1001 and #A1001 all become A-1001. If there are several, take the one the email is mainly about. Invoice numbers (INV-...), tracking numbers, gift card codes, phone numbers and postcodes are not order numbers. No order number: return null. Never guess one.

# urgent
true when any of these holds:
- the customer names a deadline within 48 hours (today, tonight, tomorrow, before the weekend),
- the customer was charged twice, or charged for something they did not order,
- there is a safety problem (sparks, smoke, burns, broken glass, a recall),
- the customer will dispute the charge with their bank or post a public complaint,
- the email is the third or later follow-up on the same problem.
Otherwise false. Capital letters, exclamation marks and an angry tone alone do not make a ticket urgent. A polite tone does not make it less urgent.

# Examples
Email: "My order A-1001 still says 'label created' after a week. Can you check?"
Ticket: {"category": "shipping", "order_id": "A-1001", "urgent": false}

Email: "You charged my card twice for A-1002!!"
Ticket: {"category": "billing", "order_id": "A-1002", "urgent": true}

Email: "Does the 5-quart Dutch oven work on induction?"
Ticket: {"category": "other", "order_id": null, "urgent": false}

Email: "The kettle from order a1003 started sparking this morning."
Ticket: {"category": "other", "order_id": "A-1003", "urgent": true}

Email: "Box for A-1004 arrived crushed and two mugs are broken. My party is tomorrow."
Ticket: {"category": "shipping", "order_id": "A-1004", "urgent": true}

Email: "I never got my parcel, so I want my money back. Order A-1005."
Ticket: {"category": "billing", "order_id": "A-1005", "urgent": false}

Email: "THIS IS THE WORST SHOP EVER. Where is my stuff?"
Ticket: {"category": "shipping", "order_id": null, "urgent": false}

Email: "Third email about invoice INV-77812 for A-1006. Still no reply."
Ticket: {"category": "billing", "order_id": "A-1006", "urgent": true}

Email: "Can I swap the blue towels in A-1007 for green ones before it ships?"
Ticket: {"category": "shipping", "order_id": "A-1007", "urgent": false}

Email: "I can't log in. The reset link says it expired."
Ticket: {"category": "other", "order_id": null, "urgent": false}

# Output
Return only the ticket. Do not answer the customer, do not explain, and do not add fields."""

TEMPLATES = [
    "Where is my order {o}? It said 3-5 days and it's been 9.",
    "Tracking for {o} hasn't moved since Monday. Is it lost?",
    "The {p} in {o} arrived with a cracked lid. The box was crushed.",
    "Can you send {o} to my work address instead? I'm never home.",
    "{o} says delivered but there's nothing at my door. I need it tonight!",
    "My box for {o} came without the {p}. Everything else is there.",
    "I'd like to cancel {o} before it ships, please.",
    "Can I upgrade {o} to express? It's a gift for Saturday.",
    "You charged me twice for {o}. Please fix this today.",
    "When will my refund for {o} show up? It's been two weeks.",
    "The promo code SPRING10 didn't apply to {o}. Can you refund the 10%?",
    "Please send me an invoice for {o} with my company name on it.",
    "My card was declined for {o} but the money left my account.",
    "I returned the {p} from {o}. Where's my money? I'll call my bank next.",
    "Why was I charged $79 for Acme Plus? I cancelled it last month.",
    "Is the {p} dishwasher safe? Thinking of buying two.",
    "My {p} stopped working after 3 months. Is it under warranty?",
    "I can't reset my password. The email never arrives.",
    "Just wanted to say the {p} is amazing. Thank you!",
    "The {p} from {o} smells like burning plastic when I use it.",
    "Hola, mi pedido {o} no ha llegado. ¿Dónde está?",
    "FOURTH time asking: where is {o}???",
    "Do you ship to Canada? And how much does it cost?",
    "Order {o2}: the {p} handle snapped off on first use, nearly burned me.",
    "Hi, I paid with a gift card on {o} but it also charged my Visa.",
]
PRODUCTS = ["kettle", "Dutch oven", "knife set", "coffee grinder", "blender"]

EMAILS = {
    f"email-{i:03}": TEMPLATES[i % 25].format(
        o=f"A-{1001 + i}", o2=f"a{1001 + i}", p=PRODUCTS[i % 5])
    for i in range(100)
}
