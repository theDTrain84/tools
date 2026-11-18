# Three Things at Once

> A living record of this fall's failures and attacks on digital systems, from Microsoft 365 and the FAA ground stop to the NSA's network: what you may have run into, what each operator said, and how two AI systems and a person checked it.

**A living record.** Last updated November 18, 2026, 8:30 a.m. Eastern.

Kept by Dustin Nimmo, Mise and Muse. Two AI systems from two companies search separately, we open the sources, and a person decides what it adds up to. See how this was made

**DNSC** From the public record

Three things at once · Understanding the week, from the record

Seven failures in six days. Four confirmed attacks before them.

- began with a change to a running system
- day stated, hour not stated
- confirmed attack

Tap or click any row to go straight to that outage.

**Confirmed attacks** four public systems, Oct 9 to 28

- Federal bankruptcy noticing center *from Oct 9*
- Ohio Auditor of State *Oct 25*
- FEC filing system *Oct 26 to 27*
- UNM Health *Oct 26 to 28*

**Microsoft 365** work email and Teams

about 24 hr · Nov 12 to 13, about 24 hours; began with a change to a running system.

**FAA** every U.S. departure

4 hr 40 min · Nov 13, 4 hours 40 minutes; began with a change to a running system.

**Workday** payroll and time off

until Sat 11 a.m. · From Nov 13 until Nov 14, 11 a.m.; began with a change to a running system.

**JPMorgan Chase** the bank app and Zelle

about 7 hr · Nov 16, about 11:30 a.m. to 6:30 p.m.

**United** departures

about 30 min, per United · Nov 16, about 30 minutes by United's count; hour not stated.

**Apple** Apple Pay and iCloud

late morning to about 5 p.m. · Nov 17, late morning to about 5 p.m.; began with a change to a running system.

**NSA** a classified network

still being restored · Nov 17, still being restored; began with a change to a running system.

Bars to scale, Eastern time. A faded end means the hour was not stated. Each outage is explained below.

## Three things are happening to our digital systems at the same time.

1. Attacks. · Some now run by machines.
2. Rushed changes. · Change moving faster than coordination.
3. Hidden dependencies. · Changes made without seeing what depends on them.

**For anyone who runs technology, all three come back to coordination: who knew what was changing, who checked what it touched, and who was watching the door.**

If you felt it this week

### What you may have run into, and what the company says happened.

1. Microsoft 365 **Your work email would not open.** *Microsoft says* a flaw it shipped in July sat in its gateway servers, the machines that pass traffic into its service. A traffic shift and a capacity cut followed, and its automatic switch to backup made it worse. · See the ticket
2. FAA **Your flight sat at the gate.** *Federal officials say* a new router, a box that passes messages between networks, went in during an upgrade in El Dorado, Arkansas, and flooded the air traffic network. About 12,000 flights did not operate. · See the ticket
3. Workday **You could not clock in or request time off.** *Workday says* a disaster recovery test, a practice run of its backup site, unexpectedly connected the backup to its live databases. · See the ticket
4. JPMorgan Chase **Your bank app failed.** *Chase says* a software bug in a hardware system in its own data center caused it, and called the outage "not cyber-related." · See the ticket
5. United **Your United departure was delayed.** *United calls it* a technology issue. It has not said what failed. · See the board
6. Apple **Apple Pay, iCloud or the App Store would not work.** *Apple says* an internal update caused the outages. · See the ticket

A seventh failure reached no public service: the NSA's classified network, after a security patch, which is a fix for a flaw in software. See the ticket

#### What they have in common

**Five of the seven began with a change to a system that was already running:** an upgrade, an update shipped in July, a backup test, an internal update, a security patch.

In each of those five, the service people use leaned on another part. When that part changed, the service broke. That relationship is called a dependency.

**Whether anyone coordinated those changes is not yet on the record.** None of the seven was called an attack by its operator, and no source ties a failure to an attack, to another failure, or to AI.

The rest of this page follows the three things at once.

- Attacks four confirmed since Oct 9
- Rushed changes Microsoft, Apple, the NSA
- Hidden dependencies Workday, the FAA, Chase

Attacks

### Four public systems confirmed attacked in three weeks, and attackers now have tools that work on their own.

Each attack below was confirmed by the office or hospital that was hit. None is tied on the record to the November failures.

#### Some attacks now run themselves.

On November 16, Google's threat team reported attackers using AI to find software flaws and exploit them "without a human in the loop for the first time." 17

- **Under 3 hours**From first target to privileged access, in some break ins, per an FBI warning of Nov 13. 18
- **8 → 22**Newly exploited, previously unknown flaws a month: the 2025 average, then August 2026. 17

None of the seven November failures was called an attack by its operator, and no source ties any attack here to them.

[Chart: A loop of four steps: find a flaw, write the exploit, break in, take control. A dot runs the loop with no person in it. Beside it, three bars: 8 flaws a month in 2025, 11 in 2026, 22 in August 2026.]

Bar heights to scale. Google Threat Intelligence Group, Nov 16, 2026.

U.S. Courts · Oct 9

#### Federal bankruptcy noticing center

[Chart: An attack from outside reached Bankruptcy noticing center (run by BAE Systems).]

- Attacks
- contractor

1. Oct 9All bankruptcy notices halted. 16
2. Oct 16U.S. Courts, as reported: a "cybersecurity incident." 16
3. OpenNo restoration on the record.

Back to the week

Ohio Auditor of State · Oct 25

#### Web server and online accounts

[Chart: An attack from outside reached Web server, online accounts (Ohio Auditor of State).]

- Attacks
- Ohio

1. Oct 25Web server attacked; the office takes it and its online accounts offline. 14
2. Oct 27The office: "potentially foreign state actors." Not ransomware. 14
3. OpenNo restoration on the record.

Back to the week

FEC · Oct 26 to 27

#### Federal Election Commission e-filing

[Chart: An attack from outside reached Electronic filing system (FEC).]

- Attacks
- election

1. Oct 26Spending reports blocked, a week before the midterms. 15
2. Oct 27FEC email, per Reuters: "a bad actor attempting to breach FEC systems." 15
3. OpenNo restoration on the record.

Back to the week

UNM Health · Oct 26 to 28

#### New Mexico's only Level I trauma center

[Chart: An attack from outside reached End user devices (UNM Health).]

- Attacks
- hospital

1. Oct 26 to 28Ambulances diverted for 2 hours; clinics and surgeries cancelled. 28
2. Oct 27UNM's health sciences center: a cyberattack on "end user devices." 28
3. OpenNo final public report on the record.

Back to the week

Where two of the three meet

#### The PHP patch: an attack risk, then a scramble to change running systems.

The vulnerabilities "are in PHP, a programming language that powers about 70% of the world's websites." They were discovered last month, and "AI tools helped researchers exploit them," which set off a global scramble to patch. The NSA itself urged organizations to apply the patches. 37

**As reported**The patch came out October 21, 2026 for two critical flaws, and Germany and Belgium took government websites offline as a precaution. 38

At the NSA, the patch was the change: the Director of National Intelligence said the patching "caused some of these systems to not come back up." No attack on the NSA is on the record. 37

[Chart: PHP, drawn as one block, feeds ten website tiles, seven of them shaded for about 70 percent of the world's websites. Below, four steps: flaws found, AI tools help researchers exploit them, a patch, and at the NSA some systems do not come back up.]

Tiles show a share, not a count. CNN, Nov 17.

Rushed changes

### Change moving faster than coordination: one change sits unnoticed, then others land on top of it.

The operators' own statements describe changes stacking. At the NSA, the Director of National Intelligence said a security patch kept some systems from coming back up. Whether anyone saw these changes together is not yet on the record.

#### Microsoft 365: three changes, one outage

Microsoft, preliminary cause 5

1. July 2026 **A defect ships**Deployed in Microsoft's networking gateway servers.
2. About four months unnoticed
3. Then **A traffic shift**Network traffic is moved.
4. Then **A 14% capacity cut**Less capacity to carry it.
5. Nov 12 to 13 **Down about 24 hours**Automatic failover made it worse. More than 70 countries.

Microsoft says it was not related to a cyberattack or to AI. Final report due about Nov 20.

Earlier this fall, the same shape

**Microsoft Azure, Sept 30** A paused update resumed all at once and overloaded a control plane, in 34 regions for about 6 hours. 27 *Microsoft incident report*

**Google Cloud Storage, Oct 8 to 9** A configuration change, then a rollback that did not fully work. About 18 hours. 27 *Google incident report*

Microsoft · Nov 12 to 13

#### Microsoft 365 email and apps

About 24 hours, in more than 70 countries.

[Chart: Microsoft 365 email and apps (Microsoft) leans on Gateway servers (Microsoft), marked changed.]

- **What changed**: A defect deployed in July, then a traffic shift and a 14% capacity cut. Automatic failover made it worse.

- Rushed changes
- change to a running system
- failover

1. Nov 12Outlook, Teams and other apps go down. 5
2. By Nov 17Preliminary cause posted. Microsoft: "not related to cyber or AI / agents." 5
3. About Nov 20Final report due.

Back to the week

Apple · Nov 17

#### iCloud, App Store, Apple Pay

Sign in, purchases and iPhone activation failed for many users.

[Chart: iCloud, App Store, Apple Pay (Apple) leans on Internal update (Apple), marked changed.]

- **What changed**: "An internal update caused some outages this morning."

- Rushed changes
- change to a running system

1. Nov 17Outages from the late morning, Eastern time. 13
2. Nov 17Apple, as relayed by a Bloomberg reporter and 9to5Mac: an internal update; not a cyberattack. 13
3. AfternoonSome systems still being restored. 13
4. About 5 p.m. reportedFully resolved, per the research desk's board. 40

Back to the week

NSA · Nov 17

#### NSA Net, the agency's classified network

Staggered log ins. Restoration "ongoing but not yet complete," a source said.

[Chart: NSA Net, its internal network (NSA) leans on Security patch (not stated), marked changed.]

- **What changed**: A software patch for major vulnerabilities discovered last month, per the Director of National Intelligence.

The stated cause is a response to an attack risk. No attack on the NSA is on the record.

- Rushed changes
- change to a running system
- security patch

1. Nov 17The NSA: "The National Security Agency experienced temporary degradation during scheduled routine maintenance." 37
2. Later Nov 17Director of National Intelligence Jay Clayton, on Fox Business: "The patching that has gone on following that has caused some of these systems to not come back up." He saw no sign any recent outage was a cyberattack. 37
3. OpenRestoration "ongoing but not yet complete," per a source. 37

Back to the week

#### More code is written by machines, and changes land less steadily.

Every change to a running system has to be checked against everything that leans on it. Earlier this fall, a paused Microsoft cloud update resumed all at once and overloaded a control plane, and a Google storage change could not be fully rolled back. 27

- **7.2%**Estimated drop in delivery stability tied to AI adoption, in Google's 2024 research on software teams. 19
- **1 in 4+**Share of Google's new code written by AI, per its chief executive, Oct 2024. 21
- **+81%**Duplicated code blocks, in a 2026 study of 623 million changes. 20
- **21% → 3.8%**Changed lines spent reworking old code, 2022 to 2026, same study. 20

No outage on the board has been traced to code written by AI. Microsoft says its outage was not related to AI.

[Chart: Changes move along a track toward one check. The check asks what else leans on the part being changed. Past the check, a running system has three other systems leaning on it.]

The shape of a dependency. The share of AI-written changes drawn here is not to scale.

Hidden dependencies

### Changes made without seeing what depends on them. A recovery test connected to live databases. A new router flooded 17 of 22 air traffic centers.

Whether anyone mapped what these changes would touch before making them is not yet on the record.

Workday · Nov 13 to 14

#### HR and payroll platform

At affected employers, staff could not log in, clock in or request time off.

[Chart: Workday live production databases on the left and its disaster recovery backup site on the right, with a wall between them meant to keep them apart. During a test, the backup site connected through the wall to production.]

- **What changed**: While validating its weekly disaster recovery maintenance window, "tenanted services within the DR Site unexpectedly connected to Production databases," leaving data "in an inconsistent state."

- Hidden dependencies
- change to a running system
- backup test

1. Nov 13Customer systems offline. 9
2. NoticeCause stated in a customer notice, as quoted in coverage. A spokesperson: not related to a cybersecurity incident. 9
3. Nov 14Service declared restored at 11 a.m. 9
4. OpenPost incident report not yet published.

Back to the week

FAA · Nov 13

#### Nationwide ground stop

About 4 hr 40 min; about 12,000 flights did not operate.

[Chart: Air traffic network (FAA) leans on Router in El Dorado, Ark. (contractor L3Harris), marked changed.]

- **What changed**: A router installed during copper to fiber work flooded the network; 17 of 22 centers unstable.
- **The contractor**: L3Harris says its work is done "in close coordination with the FAA," as reported by Reuters. 29

- Hidden dependencies
- change to a running system
- contractor
- legacy equipment

1. Nov 13Every departure from U.S. airports held. 6
2. Nov 14FAA Administrator: "zero evidence of anything nefarious, and zero evidence of anything AI-related." 3
3. Nov 15Technicians' union: two "contractor owned and maintained routers"; its members "were not involved." 8
4. Nov 17The Transportation Department "officially submitted its $50.1 billion budget funding request." Thirteen Senate Democrats asked for technical briefings from the FAA, L3Harris and Juniper, and the FAA began halting the installation of the routers. 40
5. OpenRoot cause under FAA and FBI review. 6

Back to the week

JPMorgan Chase · Nov 16

#### Online banking, branches, Zelle

About 11:30 a.m. to 6:30 p.m. Eastern.

[Chart: Online banking, branches, Zelle (JPMorgan Chase) leans on Hardware in its own data center (JPMorgan Chase), marked software bug.]

- **What failed**: "a software bug in an on-premise hardware system" 10
- **Reported**: An FBI official told NewsNation the outage was traced to a software release by JPMorgan Chase. 39

- software bug
- own data center
- reached other banks, reported

1. Nov 16Transactions fail online, in branches and on Zelle. Chase: "not cyber-related." Service back by evening. 10
2. Nov 17 reportedChase: the bug spread to other institutions "when we were party to a transaction involving other banks"; the issue was not systemic. 39
3. Nov 17 reportedAn FBI official: traced to a software release by JPMorgan Chase. 39

Back to the week

The ground stop, step by step

### How one router at one site held every departure in the country.

**FAA nationwide ground stop** Nov 13, 2026 · Cause stated · full report still owed

1. [Chart: Two en route centers with a router between them. Messages travel through the router in both directions.] ##### What a router does It passes messages along a network. The FAA's 22 en route centers, which handle flights between airports, depend on that network to stay in touch.
2. [Chart: At one site, an old copper line is crossed out and a new fiber line is drawn. A new router, marked as the change, sits on the line.] ##### What was being changed At one site in El Dorado, Ark., old copper lines were being swapped for fiber. A router installed by the contractor L3Harris went in mid-day. 6 "We use 1980s little copper lines," the Transportation Secretary said that day. 26
3. [Chart: The new router sends a flood of connection attempts toward the rest of the network.] ##### What the new router did It flooded the network with "over 1,000 connection attempts every four to five seconds," the Transportation Secretary said, and swamped the FAA's older equipment. 6 Why the router did this is not yet known. The root cause review is open.
4. [Chart: 22 centers, 17 marked unstable in red and 5 steady. Below, a plane held at the gate and a plane already in the air still flying.] ##### How far it spread 17 of the 22 centers became unstable. The FAA held every departure from U.S. airports for 4 hours 40 minutes; planes already flying kept going. About 12,000 flights did not operate. 6 How the flood reached 17 centers, and why 5 held, is not yet public.

- **Runs the network**: FAA
- **The part**: A router in El Dorado, Ark., installed by contractor L3Harris during copper to fiber work
- **Duration**: 4 hr 40 min
- **FAA's word**: "legacy equipment"
- **The contractor**: L3Harris says its work is done "in close coordination with the FAA," as reported by Reuters. 29
- **Root cause**: Under FAA and FBI review

"isolated to two contractor owned and maintained routers ... PASS-represented technicians were not involved."*The FAA technicians' union, Nov 15 8*

"Identifying the device that failed does not establish why it failed."*Senate Commerce Democrats, to the FAA, DOT, L3Harris and Juniper, Nov 17 7*

The people who used to check the change

### Who used to check the change?

The record on that is thin. Nearly everything below comes from news coverage of the cuts, not from company filings.

Cuts at companies in this story

**Microsoft**May 2025 31

about 6,000

**Microsoft**July 2025 31

about 9,000

**Microsoft**July 2026 32

4,800

**Workday**Feb 2025 33

about 1,750

**Workday**Sept 2026 34

about 525

- **Microsoft:** teams reported as management layers, engineering and product (May 2025); sales, support and Xbox (July 2025); commercial sales and Xbox (July 2026).
- **Workday:** its chief executive tied the 2025 cut to investment in AI. The 2026 cut was concentrated in Product and Technology.
- **No layoff round found** for JPMorgan Chase or L3Harris, and no technology staff cut found at United. 36

Bars to scale. Reported figures; the companies' own filings were not opened.

171,501

technology job cuts announced January to October 2026, up from 141,159 a year earlier, by the count of Challenger, Gray & Christmas. Across all industries, employers cited AI for 121,401 cuts. 30

#### Cut by role: mostly not on the record

No company in this story has named its testing, reliability or release teams in a cut. The closest named case is Salesforce, whose August 2026 cut reportedly included "incident commanders," the people who run the response to an outage, and technical support engineers. 35

No post incident report, union or study ties any cut to these outages. Microsoft says AI is not replacing the workers it laid off. 32

In the federal government

#### Federal technology teams are smaller, and the repair bill keeps rising.

The government's in house technology team, 18F, about 90 people, was eliminated March 1, 2025. 25 On November 13 the Transportation Secretary said of air traffic control: "This is an emergency ... I want $50 billion," and "We use 1980s little copper lines." 26

No investigation has tied staffing cuts to any failure on the board. The FAA technicians' union says its members were not involved in the router work.

Technology staff, share lost

**Cybersecurity agency**3,300 → 2,200 22

a third

**GSA tech service**per its inspector general 23

67%

**IRS technology**its CIO's count 24

about 40%

**18F**about 90 people 25

eliminated

The stated price of rebuilding air traffic control

**Jul 2025**enacted

$12.5B

**Jul 2025**"the full project"

$31.5B

**Sep 2026**total, as reported

$42.5B

**Nov 2026**"I want $50 billion"

$50B

Bars to scale. Sources 22 to 26.

Two officials, two answers

### The Homeland Security Secretary relayed a theory about "SI." The FAA's chief had already said there was no sign of AI.

Fox News, "Hannity" · Nov 16

> "I believe that it's the SI ... because these programs aren't designed to work as fast as SI is."
>
> "That kind of makes sense to me."

**Markwayne Mullin, Secretary of Homeland Security**, relaying what "one guy that's very smart with tech" told him. 1

On the ground stop · Nov 14

> "We see zero evidence of anything nefarious, and zero evidence of anything AI-related."

**Bryan Bedford, FAA Administrator.** 3

In the same interview, the Secretary said the federal cyber agency told him the outages were "all individually unrelated," and that "with 98% certainty, we're not seeing a cyber attack." 1 2

AI · SI

#### "SI" is today's AI, renamed

An executive order signed September 29, 2026 tells federal agencies to use "Super Intelligence" and "SI" in place of "Artificial Intelligence" and "AI." The terms cover the same technologies the law already defines as artificial intelligence. 4

It names no new kind of machine.

After the outage

### Who asked for what.

A failure is followed by requests: for money, for contracts, for someone to blame. Those are on the record too, and they can be checked. This ledger lists them with dates and amounts. It draws no conclusion about why.

1. July 2025 · Congress approved $12.5 billion over five years for air traffic control upgrades and controller hiring. opened · $12.5B
2. July 1, 2026 · The FAA awarded L3Harris a contract to upgrade and operate the national aircraft tracking network through 2045. A federal notice lists $913.4 million for the five year base period; the award was sole source. This is a different system from the network that failed on Nov 13. reported · $913.4M
3. Fri Nov 13, 2026 earlier in the day · Transportation Secretary Sean Duffy and the White House asked Congress for $30.1 billion: $10.1 billion for air traffic control modernization (including $7.2 billion for a common automation platform and controller workstations and $2 billion for cloud computing), $2 billion for control towers, $18 billion for airport projects. opened · $30.1B
4. Fri Nov 13, 2026 · The ground stop: 4 hours 40 minutes; about 12,000 flights did not operate. on this page · 4 hr 40 min
5. Fri Nov 13, 2026 late · The administration raised the request to $50 billion. Duffy: "This is an emergency." "What's more important than having an air traffic control system that actually works?" The breakdown of the larger figure is not on the record. opened · $50B
6. On the record · Support for the request: American, Delta, United and Southwest airlines. opened
7. Mon Nov 16, 2026 · On Fox News, the Homeland Security Secretary relayed a theory about "SI," today's AI renamed, from "one guy that's very smart with tech." on this page
8. Open · Whether Congress acts on the $50 billion; who receives the contracts; the root cause report on the router. no source yet

All rows concern the air traffic system. Dollar bars are drawn to scale against $50 billion.

The board, as of November 17

### Five failures still owe a full report. One closed with a stated cause, one without a real one. Four attacks have no final report on the record.

A ticket moves only when the operator or an investigator says something on the record.

Outages and attacks 11 tickets Attacks 4 Rushed changes 3 Hidden dependencies 2 AI doing human work 0 Links between tickets 0

Cause statedfull report still owed · 5

FAA · Nov 13

##### Nationwide ground stop

A contractor's router, installed during copper to fiber work. Open ticket

- Hidden dependencies
- change to a running system

Microsoft · Nov 12 to 13

##### Microsoft 365

A July defect, then a traffic shift and a 14% capacity cut. Open ticket

- Rushed changes
- change to a running system

Workday · Nov 13 to 14

##### HR and payroll platform

A recovery test connected the backup site to live databases. Open ticket

- Hidden dependencies
- change to a running system

Apple · Nov 17

##### iCloud, App Store, Apple Pay

An internal update. Open ticket

- Rushed changes
- change to a running system

NSA · Nov 17

##### NSA Net, its classified network

A security patch kept some systems from coming back up, per the Director of National Intelligence. Open ticket

- Rushed changes
- change to a running system

Closedwith a stated cause · 1

JPMorgan Chase · Nov 16

##### Online banking, branches, Zelle

"a software bug in an on-premise hardware system." reportedTraced to a software release, an FBI official said; it reached other banks, Chase said. Open ticket

- software bug

Closedcause not really stated · 1

United Airlines · Nov 16

##### Flights held systemwide

United: a "technology issue," with "no indication" it was cybersecurity related. 11

United said fewer than 150 flights. reportedFlightAware recorded 418 delayed United flights, and United called it a "widespread system outage." 39

- technology issue

What failed? Not stated.

Back to the week

Confirmed attacksno final report on the record · 4

U.S. Courts from Oct 9

##### Bankruptcy noticing center

All notices halted. A "cybersecurity incident." Open ticket

- Attacks
- contractor

No restoration on the record

Ohio Auditor of State · Oct 25

##### Web server and online accounts

"potentially foreign state actors." Not ransomware. Open ticket

- Attacks
- Ohio

No restoration on the record

FEC · Oct 26 to 27

##### Electronic filing system

"a bad actor attempting to breach FEC systems." Open ticket

- Attacks
- election

No restoration on the record

UNM Health · Oct 26 to 28

##### Level I trauma center

Ambulances diverted 2 hours. Attack on "end user devices." Open ticket

- Attacks
- hospital

No final report on the record

**No ticket is tagged AI doing human work, and no line connects one ticket to another.** No operator, official or investigator on the record has drawn one.

#### Also on the research desk's board

Muse's board held 28 items on the morning of November 18. These are the ones not counted above. A second check opened sources for some of them, marked below. None changes the counts.

- **Marriott website and app sign in, Nov 17.** A technical issue; Marriott: "Our review found no indication that the disruption was cybersecurity-related." Resolved. reported, via Skift
- **Charles Schwab website, Nov 17.** A spokesperson said "A brief webpage loading issue has been resolved." No cause given. reported, Business Insider
- **Navy Federal Credit Union app, Nov 16 to 17.** No cause given. reported
- **Cloudflare, Nov 17.** Two incidents on its status page: Durable Objects (resolved 7:17 PM ET) and "R2 elevated errors and timeouts for requests from South America" (resolved 5:08 PM ET). No cause stated. Muse: verified on the status page
- **Anthropic, Nov 17.** Sign in with Apple on claude.ai and the Claude iOS app; resolved; no cause stated by Anthropic. Muse: verified on the status page
- **Monadnock Community Hospital, New Hampshire, from Nov 9.** Phones and systems went down on Nov 9. On Nov 16 the hospital confirmed a "cyber incident." Ambulances are being diverted and some major elective surgeries are cancelled through Nov 23. This one is an attack. second check: local paper and the hospital's site opened
- **Optimizely, Nov 16.** A compromise of its web experimentation product, used to run tests on other companies' websites. At least 178 organizations were affected, as reported by The Register. This one is an attack, not an outage. second check: status page and The Register opened
- **Outside the United States.** Attacks reported at Equinor (Norway), Ipsos, Infoblox and the IIHF website. reported
- **Gmail and American Express, Nov 17.** User reports only. Google said it was "not currently seeing evidence of a broad Gmail service disruption." The second check found no report of an American Express outage that day. unconfirmed

What an uptime promise allows

### At 99.9 percent, a system may be down about 8 hours 46 minutes in a whole year. The ground stop alone ran 4 hours 40 minutes.

A service level agreement, or SLA, is a written promise of how much of the time a system will work, with penalties when it does not. Each added nine divides the allowance by ten.

525,600

minutes in a year. 99.9 percent of them leaves about 526 minutes of allowed downtime. 99.99 percent leaves about 53.

Microsoft 365Nov 12 to 13

about 24 hr

A year's allowanceat 99.9%

about 8 hr 46 min

JPMorgan Chase · Nov 16

about 7 hr

FAA ground stop · Nov 13

4 hr 40 min

A year's allowanceat 99.99%

about 53 min

United Airlines · Nov 16, United's figure

about 30 min

One scale, 24 hours wide. The uptime terms each operator promises its own customers are not public in these sources.

What can be said

### What the record supports, what is still unproven, and what it contradicts.

#### Supported

- **Six operators named a cause; United said only "a technology issue."** None called its failure an attack.
- Five of the seven failures began with a change to a running system, by the operators' or officials' own account.
- The FAA says a contractor's router, installed during an upgrade, flooded legacy equipment at 17 of 22 centers.
- Microsoft's outage traces to a defect it shipped in July and did not catch for four months.
- The FAA Administrator saw "zero evidence of anything AI-related."
- "SI" is the government's new word for AI.
- Four public systems were confirmed attacked between October 9 and 28.
- Google and the FBI document fully automated AI attacks.
- The Director of National Intelligence said a security patch kept some NSA systems from coming back up.
- The staffing cuts and the rising price are on the record.

#### Plausible, unproven

- **New systems laid on old ones fail at the seams.** The FAA case fits. No finding of a common cause exists.
- **Writing software with AI is making it less stable industry wide.** No outage on the board is traced to it.
- **The cuts made failures likelier or slower to fix.** Not investigated.
- **Chase's outage began with a software release.** Reported from an FBI official; Chase itself has said a software bug.
- **Layoffs removed the people who check changes.** Who was cut by role is mostly not on the record.

#### Contradicted

- **"AI caused the outages."** Operators and officials say no.
- **"The FAA's AI tool caused the ground stop."** The Transportation Secretary: "no possible way." The router job was upkeep of the old network. 6
- **"A cyberattack took down the flights, the email, the bank or the NSA network."** Each operator says otherwise, and the Director of National Intelligence saw no sign of one.
- **"It is all connected."** The federal cyber agency called the outages "all individually unrelated." No source ties the attacks to the failures.
- **"Super intelligence has arrived."** The order renames today's AI.

Worth asking the people in charge

### Six questions.

1. When the root cause report on the ground stop is finished, will it be published in full, and will it say why one router could reach 17 of 22 centers?
2. Who has to sign off before a change is made to a live national system, and did that sign off happen in Arkansas on November 13?
3. How many people at the cybersecurity agency and in the FAA's technical operations do this work today, compared with two years ago?
4. What does the $50 billion buy, by when, and who outside the contractors checks the work?
5. What uptime standard are the nation's critical systems held to in writing, and who answers when it is missed?
6. When a senior official offers a theory on television, what evidence did the agencies under him provide for it?

Plain words

### Ten terms from this season.

- **SI**: The federal government's name for AI since September 29, 2026.
- **Ground stop**: An order that holds planes at the gate. Planes already in the air keep flying.
- **En route center**: One of the FAA's 22 air route traffic control centers, which handle flights between airports.
- **Router**: The device that directs traffic between networks. A faulty one can flood the others with requests.
- **Legacy system**: Old technology still doing an important job, often hard to replace or repair.
- **Disaster recovery site**: A backup copy of a system, kept apart from production, the live system people use.
- **SLA**: Service level agreement. A written promise of how much of the time a system will be up.
- **Failover**: The automatic switch to a backup when the main system fails.
- **Zero day**: A software flaw attackers use before the maker knows it exists.
- **Agent**: An AI program that carries out a chain of steps on its own.

Authors: Dustin Nimmo, Mise and Muse

### How this was made

One person and two AI systems from two different companies.

**Dustin Nimmo**

Dustin Nimmo asked the questions, named the three categories, and decided what this page says.

**Muse**

Muse is an AI agent made by Meta. It ran the research desk. Every hour it searched for new outages, attacks and official statements, and kept them on a board, each one marked verified, reported or unconfirmed.

**Mise**

Mise is Dustin's AI partner, built on Claude, made by Anthropic. It researched the same week separately, opened the sources it could reach, and built this page.

1. Muse searchesmade by Meta · Mise searchesbuilt on Claude, by Anthropic
2. Comparewhere they disagree
3. Open the sourceread the statement itself
4. A person decideswhat the facts add up to

#### How a fact got onto the page

Each system searched on its own. Where they disagreed, we went back to the source.

A failure is counted here only when its operator or a named official stated the cause. Where we read that statement ourselves, the source list says so. Where we are relying on a named news outlet, the item says reported.

Three times in one evening the check changed the page:

1. Mise's first read had the NSA outage as routine maintenance. Muse found the later statement by the Director of National Intelligence. Mise opened the report, confirmed the quote, and the ticket changed.
2. Muse's board lists incidents that Mise could not confirm on its own. They are not counted. They sit in a separate list on this page, labelled.
3. Dustin read United's explanation, 'a technology issue,' and said it explained nothing. The ticket now says the cause was not really stated.

This page is updated as the record changes, and each update is dated at the top.

#### Why two systems from two companies

Every AI system makes mistakes, and two systems built by different companies tend to make different ones. When a second system searches on its own, it catches what the first one missed or got wrong. When both find the same statement, we still open the source.

The systems gathered and checked. A person who has run systems like these decided what the facts add up to.

One disclosure: Mise runs on Anthropic's Claude, and a brief Anthropic sign in issue appears in the research desk's list above.

Sources

### Where each fact comes from.

1. Mullin on Fox News "Hannity," Nov 16, 2026, as transcribed by [Breitbart](https://www.breitbart.com/clips/2026/11/16/mullin-kind-of-makes-sense-that-systems-going-down-due-to-inability-to-handle-ai-si-speed/).
2. [Fortune, Nov 17, 2026](https://fortune.com/2026/11/17/trump-administration-ai-outages-mullin-gary-marcus-banks-airlines/).
3. Bedford, Nov 14, 2026: ABC News live updates, via ABC7.
4. Executive Order 14434, ["Inaugurating the Era of Super Intelligence," Sept 29, 2026](https://www.whitehouse.gov/presidential-actions/2026/09/inaugurating-the-era-of-super-intelligence/); [FDA notice, Nov 16, 2026](https://www.fda.gov/science-research/fda-and-super-intelligence/fdas-use-super-intelligence-and-si-under-executive-order-14434).
5. Microsoft's preliminary cause, as reported by PCWorld and Petri.
6. FAA ground stop, router and centers: FedScoop; BankInfoSecurity; Transportation Secretary Duffy's remarks.
7. [CNBC, Nov 17, 2026](https://www.cnbc.com/2026/11/17/faa-ground-stop-routers.html).
8. Professional Aviation Safety Specialists (PASS), as reported by One Mile at a Time, Nov 15, 2026.
9. Workday: [UC Today](https://uctoday.com/workday-outage-backup-test-payroll-timekeeping); Fox 29; ThousandEyes.
10. JPMorgan Chase statement: CNBC; Al Jazeera, Nov 16, 2026.
11. United Airlines statement: ABC7, Nov 16, 2026.
12. NSA network, first reports: CNN, via The New Republic, Nov 17, 2026.
13. Apple: [9to5Mac, Nov 17, 2026](https://9to5mac.com/2026/11/17/icloud-app-store-and-other-apple-services-hit-by-ongoing-outage/).
14. Ohio Auditor of State: WOSU, Oct 27, 2026.
15. FEC: Reuters, via the Honolulu Star-Advertiser, Oct 27, 2026.
16. Bankruptcy noticing center: The Register, Oct 16, 2026.
17. [Google Threat Intelligence Group, Nov 16, 2026](https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold).
18. [FBI FLASH, Nov 13, 2026](https://www.ic3.gov/CSA/2026/261113.pdf).
19. [Google DORA report, 2024](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report).
20. [GitClear, 2026](https://www.gitclear.com/the_ai_code_quality_maintainability_gap).
21. Sundar Pichai, Alphabet earnings call, Oct 29, 2024.
22. Cybersecurity and Infrastructure Security Agency staffing: Nextgov, Aug 21, 2026.
23. GSA inspector general: Nextgov, Dec 19, 2025.
24. IRS chief information officer: The Register, Feb 19, 2026.
25. [Nextgov, March 2025](https://www.nextgov.com/people/2025/03/gsa-eliminates-18f/403400/).
26. Air traffic control price: White House, July 4, 2025; Jalopnik, July 16, 2025; AirlineGeeks, Sept 28, 2026; Fox Business, Nov 13, 2026.
27. Earlier changes this fall: [Azure status history](https://azure.status.microsoft/en-us/status/history/) (Sept 30); [Google Cloud status](https://status.cloud.google.com/incidents/mSFVt6PiP557bjRyYsut) (Oct 8 to 9).
28. UNM Health: Help Net Security, Oct 27, 2026.
29. L3Harris statement on its FAA work, as reported by Reuters, Nov 2026.
30. [Challenger, Gray & Christmas, Nov 5, 2026](https://www.challengergray.com/blog/october-layoffs-at-three-year-low-seasonal-hiring-plans-up-26/).
31. Microsoft 2025 cuts: [Business Today, July 2, 2025](https://www.businesstoday.in/amp/technology/news/story/microsoft-layoffs-9000-employees-let-go-in-biggest-job-cut-since-2023-482819-2025-07-02). Reports differ on which teams took which round.
32. Microsoft July 2026 cut and its chief people officer, as paraphrased: [CNBC, July 6, 2026](https://www.cnbc.com/2026/07/06/microsoft-cuts-2point1percent-of-employees-as-xbox-unit-plans-to-spin-studios.html).
33. Workday Feb 2025 cut: [The Register, Feb 5, 2025](https://www.theregister.com/2025/02/05/workday_restructure_job_cuts/); TechCrunch; Bloomberg.
34. Workday Sept 2026 cut: [American Bazaar, Sept 30, 2026](https://americanbazaaronline.com/2026/09/30/workday-to-cut-2-5-of-workforce-affecting-about-525-employees-489102/), on the company's SEC filing.
35. Salesforce Aug 2026 cut: Business Today; IBTimes.
36. JPMorgan Chase technology budget: Fortune, Apr 29, 2026. L3Harris: state layoff notices via an aggregator, 2025 to 2026. United: [AirlineGeeks, Oct 16, 2025](https://airlinegeeks.com/2025/10/16/united-to-shrink-corporate-workforce/).
37. NSA statement, Director of National Intelligence Jay Clayton on Fox Business, and the PHP vulnerabilities: [CNN, via Local News 8, Nov 17, 2026](https://localnews8.com/politics/cnn-us-politics/2026/11/17/exclusive-highly-classified-us-national-security-communications-network-goes-down-sources-say-2/).
38. PHP patch date and European precautions, as reported by The Hill, SecureWorld, WJLA and TechRadar. Not opened.
39. Chase and United updates, as reported in the wire story "Systems restored at major U.S. banks and United Airlines following tech outages," Nov 17, 2026 (DailyFly; Big Country News Connection), and NewsNation. Not opened.
40. ABC News, "Senate Democrats demand briefings on FAA ground stop," Nov 17, 2026: the $50.1 billion request, the senators' letter and the halt to router installation. Apple's resolution time is from the research desk's board (Muse), Nov 17, 2026, as reported there and not opened by Mise.
41. Reuters, "Trump official seeks $50 billion for air traffic control after outage," Nov 14, 2026, read in a syndicated copy at [devdiscourse.com](https://www.devdiscourse.com/article/international/4006918-trump-official-seeks-50-billion-for-air-traffic-control-after-outage).
42. L3Harris aircraft tracking contract, as reported: AIN Online, July 7, 2026, and the federal contract listing at [highergov.com](https://www.highergov.com/contract/693KA726C00059). Not opened.

Authors: **Dustin Nimmo**, Mise and Muse. [DNSC](https://dnsc.ai), from the public record.

Posted November 18, 2026. Revised the same morning: the FAA's November 17 line now cites ABC News, which reports a funding request and a senators' letter where the earlier line said a Senate briefing. Last verified November 18, 2026, 8:30 a.m. Eastern. If a fact here is wrong, say so and it will be fixed and noted.

---

Source: https://tools.dnsc.ai/stories/three-things-at-once/ · Generated from the page on Nov 18, 2026
