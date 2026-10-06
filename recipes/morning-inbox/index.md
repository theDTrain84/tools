# The morning inbox · Recipe card

> A recipe card: AI triages your inbox into three tiers, labels only, drafts the replies that need you, and sends a short digest. You still send every email.

Recipe card · 01

## The morning inbox.

AI reads the inbox twice a day, sorts every thread into three tiers, labels them, drafts the replies that need you, and sends you a digest you can read in thirty seconds. It never sends, never archives, never deletes. You still send every email.

> "It totally worked. It has, like, changed my life. I basically start every day at 6:00 a.m. now. I can stay on top of everything without bothering people."

A CEO, ten weeks into working this way

#### What you need

- An AI that can read your mail and make drafts. Claude with the Gmail connector works; so does any assistant with mail access and scheduled tasks.
- Three labels in your inbox: **Needs reply**, **Worth a look**, **Noise**.
- Two scheduled runs: 7 AM for overnight, 1 PM for the morning.
- Ten minutes to tell it who matters: your clients, your team, your partners, the deadlines that count.

#### The rules it keeps

- **Label only.** Nothing is archived, deleted or marked read by the machine.
- **Drafts, never sends.** A reply draft waits in your drafts folder. You read it, change it, and you press send.
- **No drafts to strangers.** Cold pitches get a line in the digest, never a reply.
- **Short.** The digest fits in thirty seconds. The single most urgent thing comes first.

### The prompt

Paste this into a scheduled task. Replace the parts in brackets with your own names and needs. Keep the rules.

```
You are running [my name]'s twice-daily email triage. I get a flood of email and want only what matters surfaced.

1. Search the inbox for messages received since the last run (the 7 AM run covers overnight; the 1 PM run covers the morning). Skip threads that already carry one of the triage labels unless a new message arrived since it was labeled.

2. Classify every new thread into exactly one tier:
   - NEEDS REPLY: a real person wrote to me and expects a response or a decision. My clients and partners: [names]. My team: [names or domain]. Warm introductions. Anything time-sensitive with a deadline: payroll, legal, invoices, contracts. Calendar confusion that needs untangling.
   - WORTH A LOOK: informational but relevant. Meeting notes, financial notices that need awareness but no reply, calendar changes to meetings I organize, the newsletters I actually read: [names]. A cold pitch earns this tier only if it plausibly matches a real need of mine: [my needs]. Give it one line on why it might matter.
   - NOISE: cold outreach with no fit, promotions, event marketing, automated notifications with no action, calendar accepts and declines.

3. Apply the matching label to each thread. Never archive, delete or mark anything read. Label only.

4. For each NEEDS REPLY thread where a reply from me is clearly expected (at most five per run), read the full thread and create a reply draft in my voice: [three words for your voice, for example warm, direct, short]. Do not draft replies to cold outreach or sales pitches. Never send.

5. End with a digest I can read in under thirty seconds:
   - NEEDS YOU (n): one line per item: who, what they want, the deadline if any, and "(draft ready)" if you drafted a reply.
   - WORTH A LOOK (n): one line each.
   - Noise filed: the count only.
   Lead with the single most urgent thing if there is one.

If the mail connection fails, stop and say so plainly.
```

A button: Copy the prompt.

The line that makes it work: the machine proposes, you decide. That is true of every recipe here. The person holds the stakes, so the person presses send.

### Variations

- **The daily briefing.** One morning email that summarizes all activity by project or deal across a team. Same rules, read-only, built for a CEO who wanted to stay on top of everything without bothering people.
- **Call requests overnight.** Draft replies to scheduling requests so they are waiting at 7 AM.
- **One person at a time.** Set it up for the person who gets the most mail first. Adoption lives in the surface a person already inhabits.

### Where it came from

Built inside an investment bank over ten weeks, first for the CEO, then for a co-founder, then as a scheduled task the firm runs itself. The quote above is from the room, with the name left out on purpose.

---

Source: https://tools.dnsc.ai/recipes/morning-inbox/ · Generated from the page on Oct 6, 2026
