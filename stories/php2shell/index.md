# PHP2Shell

> On October 21, 2026 PHP shipped fixes for two flaws, nicknamed PHP2Shell, that let anyone on the internet run commands on a website’s server without logging in. Cloudflare’s CEO posted that its network saw millions of attempts by that night. What PHP is, how the attack works, who went offline, what to ask your host, the 34 hours from leak to millions of attempts, and who found it with AI.

DNSC · From the public record

PHP2Shell · October 22, 2026 · Understanding the week, from the record

PHP · Cloudflare · Oct. 20 to 22, 2026

## PHP fixed two flaws that let anyone on the internet run commands on a website’s server. Cloudflare saw millions of attempts within 12 hours of the fix.

PHP is the programming language that builds the pages of about 69 in every 100 websites whose server language is known. [23] On October 21 the PHP project shipped fixes for two flaws, nicknamed PHP2Shell, that let anyone run their own commands on a site’s server over the web, with no login. [1][6] That night Cloudflare’s chief executive posted that attempts to use them on its network had gone from thousands, in the 10 hours before the announcement, to millions. [13]

[Chart: 100 squares stand for 100 websites whose server-side language W3Techs can identify. 69 are filled: the ones running PHP.]

69 of 100

websites whose server-side language is known run PHP, by W3Techs’ count on Oct. 22, 2026. [23]

PHP’s own site: it powers everything from your blog to the most popular websites in the world. [11]

The fix has to be installed on each server by whoever runs it; updating the website itself does not fix PHP. [6][12] On October 21 BambooHR’s HR and payroll service and Dutch government sites went offline as a precaution. [19][20]

Not yet published

**Disclosure:** Anthropic is the company that makes Claude, the AI that helps make this site. The PHP Foundation says it worked with Alpha-Omega to scan PHP with Anthropic’s Claude Mythos earlier this year, and thanks Alpha-Omega, OpenAI and Anthropic for giving the team access to their tools and funding some of the security work. Anthropic is not among the finders it credits for these two flaws. [5]

What it is

### A web request can trigger the attack before the site’s own code runs.

- **PHP the language**: A programming language that runs on a website’s server and builds each page before it reaches a visitor’s browser. WordPress, Drupal, Nextcloud and phpMyAdmin are built on it. [22]
- **Shell the command line**: A computer’s command line. Having a shell on a server means being able to type commands on it from far away. PHP2Shell is the name the finders gave the pair. [6]
- **Remote code execution RCE**: Running commands on someone else’s computer over the internet. Unauthenticated means no login first. PHP rates both flaws 9.2 out of 10. [2][3][4]
- **WAF web application firewall**: A filter in front of a site that checks each request and blocks ones that match known attacks. Cloudflare turned on rules for these flaws for its customers, free plans included. [12]

Drawn from PHP’s advisory and the two GitHub advisories [1][3][4]; the leaked items are the ones Wiz lists. [7]

**The two flaws, in PHP’s words**

**CVE-2026-109618, RCE via OOM corruption:** out-of-memory handling can interrupt PHP while internal request data is only partially initialized. Request cleanup may then treat the invalid data as valid. [1] The confirmed impact is unauthenticated remote code execution as the web worker account. [3]

**CVE-2026-109619, RCE via stale global state:** request-owned internal state can survive after its backing memory has been freed. A later request handled by the same worker may use that stale state before normal initialization resets it. [1] Session upload progress can reach session handling before ordinary session initialization. Its confirmed impact includes memory disclosure and remote code execution. [4]

**Who is at risk:** all PHP installations serving web requests, including PHP-FPM, Apache with mod_php, php-cgi, FrankenPHP and LiteSpeed. We consider the risk highest for mod_php, with a demonstrated exploit where an unauthenticated request can trigger the attack before any application code runs. [1] For PHP-FPM, the advisory says no complete exploit has been shown. [3]

**What can leak:** Wiz says leaked memory may hold passwords, authentication tokens, API keys and certificates from other requests or the server. [7]

The race

### Thousands of attempts before the fix, millions by that night.

> In the 10 hours before it was publicly announced, across the @Cloudflare network we saw thousands of attempts to exploit it. That jumped to tens of thousands in the 45 minutes post announcement, hundreds of thousands within 2 hours, and millions now. [13] · Matthew Prince, Cloudflare’s chief executive, on X, 9:25 PM ET Wednesday, Oct. 21 (01:25 UTC Thursday)

Attempts on Cloudflare’s network, log scale: each step up is ten times more. Each bar spans the range of Prince’s word (thousands is 1,000 to 9,999); his post gives no exact counts. Times are Eastern. [12][13]

- **Attempts.** CISA said on Oct. 21 that it has not observed exploitation of these vulnerabilities as of the time of publication. [18] The Dutch National Cyber Security Centre said a day later, We see attempts to exploit the vulnerabilities. (translated) [21] No source on the record confirms a successful break-in. [27]
- **Before the fix.** Cloudflare says it turned its rules on at 3:02 a.m. UTC on Oct. 21, for all plans with its firewall, free included. That was nearly 11 hours before PHP’s 14:00 UTC release. [1][12] Its chief technology officer posted that morning that PHP sites behind Cloudflare already have an initial set of WAF rules deployed. [14]
- **Changing payloads.** Cloudflare says attackers changed their payloads to try to get past the rules. [12]
- **Four days earlier.** Amazon says its honeypots caught one attempt dated Oct. 17, and that it remains unclear how the actor acquired exploit information prior to disclosure. It adds, it’s unclear if any of these attempts would have succeeded in real-world systems. [17]

Who it reaches

### Where PHP runs, and who went offline to patch it.

40of 100

of all websites run WordPress (39.6, by W3Techs’ count), which is built on PHP. [22][24] Wiz says it confirmed the attack against WordPress and Drupal in August. [7]

[Chart: 100 squares for all websites; 39.6 filled: WordPress.]

20of 100

of all websites send their traffic through Cloudflare, by Cloudflare’s count; W3Techs measures 27.8. [15][25]

[Chart: 100 squares for all websites; 20 filled: Cloudflare, by its own count.]

35of 100

PHP sites run version 7 or 5 (26.9 and 7.7), lines that no longer get releases from the PHP project. [1][23]

[Chart: 100 squares for PHP websites; 34.6 filled: version 7 or 5.]

#### Taken offline as a precaution, Oct. 21

As each one announced it, or as reported.

- **BambooHR**HR and payroll, in the U.S., Canada and Ireland: We know this interrupts essential work, including payroll. [19] midnight ET · 7:51 AM to 2:01 PM midnight
- **The Netherlands**MijnOverheid and DigiD (the government’s online services and log-in), the House of Representatives’ site, the National Cyber Security Centre’s own site, the Data Protection Authority, Notubiz (a meeting system used by about 100 municipalities) and several university systems. [20]
- **Finland and Japan**Finland’s state IT provider, Valtori, shut government public web services and said the outages were not caused by exploitation of the vulnerabilities or by a cyber breach. Japan’s National Tax Agency took its service down; the Finance Ministry and Meteorological Agency partly suspended theirs. [29]
- **University of Washington**Cut network access to systems running vulnerable PHP until each was patched, leaving them running. [22]

What to do

### Update PHP on the server, or ask your host whether it has.

PHP: There are no complete mitigations, updating is the only safe choice. [1]

**Fixed versions [1][18]**

| If you run | Fixed in | Note |
|---|---|---|
| PHP 8.5 | 8.5.12 |  |
| PHP 8.4 | 8.4.27 |  |
| PHP 8.3 | 8.3.36 |  |
| PHP 8.2 | 8.2.35 | End of life Dec. 31, 2026 |
| 7.4 to 8.1 | no release | PHP posted source patches; some vendors ship fixes |
| 5.4 to 7.3 | no fix | PHP: upgrade to a supported version |

CISA: systems that can’t be updated right away, or that run PHP 8.1 or earlier, should go offline until they can be patched or updated. [18]

**If you can’t update today: PHP’s stopgaps**

PHP says these reduce exposure to specific attack paths but do not make an installation safe. [1]

**For CVE-2026-109618:** set `memory_limit=-1` where applications can’t override it; set a low `post_max_size` (8M without uploads, 32M with); enforce request-size limits at the web server or proxy; do not use `RLIMIT_AS` or `RLIMIT_DATA`. [1]

**For CVE-2026-109619:** Set session.upload_progress.enabled=0 and restart every worker. On PHP 8.5, also set `fatal_error_backtraces=0` and restart every worker. [1]

**Signs to look for:** unexpectedly large or malformed PHPSESSID response cookies, unusual multipart requests (uploads) followed by memory-limit errors or repeated HTTP 500 responses, unexplained PHP worker crashes or restarts [6], and PHP worker processes launching shells or downloading tools. [18] The finders say the absence of these signs does not establish that a system is unaffected. [6]

#### If a host or vendor runs PHP for you

1. Cloudflare’s advice: ask your hosting provider to apply the fix if it manages PHP. Updating the site’s code or plugins alone does not fix these flaws. [12]
2. PHP: Linux distributions and LTS vendors received the patches in advance, so check your vendor for updated packages. [1]
3. A vendor’s fix can carry an older-looking version number. Debian advises looking for the CVE number in the package changelog. [27] Debian’s fixed builds are 8.2.35-1~deb12u1 and 8.4.27-1~deb13u1. [26]

#### If you run it yourself

1. Update to a fixed version, then restart Apache, PHP-FPM and any long-running PHP workers. Updating only the application does not fix the PHP runtime. [6]
2. CISA: find every system running PHP, including PHP built into other software; patch the internet-facing ones first; take systems offline if they can’t be updated right away; a web application firewall may offer partial protection until then. [18] The UK’s cyber agency also says to consider taking a system offline until it is fixed. [31]
3. CERT-EU: Only an update fully fixes these vulnerabilities. [30]

The 34 hours

### From leaked ID numbers to millions of attempts, Tuesday to Wednesday night.

Times are Eastern (EDT). UTC is four hours later. The release was set for Thursday; PHP moved it up a day after the leak. [2][5][28]

leak and fix defenders attempts seen taken offline hollow: a notice or a none seen · Sources: [1][2][5][12][13][16][19][20][27][28]

**Each time, and where it comes from**

**Tue. ~11 AM ET (15:00 UTC):** the two CVE IDs began circulating on online forums and social media. [5] A now-deleted Hacker News post said the flaws would be disclosed on October 22, as BleepingComputer reported. [28]

**Tue. 3:30 PM ET (19:30 UTC):** the Foundation says PHP brought its pre-announcement forward and published it at 19:30 UTC. [5] The notice set the release for Wednesday, 21 October 2026 at 14:00 UTC and said, We reserve the right to release earlier should details of either vulnerability become public. [2] BleepingComputer reported it at 4:56 PM ET. [28] The Foundation says it moved the release from October 22nd, 14:00 UTC, to October 21st, 14:00 UTC. [5]

**Tue. ~4 PM ET (around 20:00 UTC):** as a result of the leak and pre-announcement, Calif mistakenly published a video of its exploits working, per the PHP Foundation. [5]

**Tue. 11:02 PM ET (03:02 UTC Wed.):** Cloudflare’s rules on by default. [12]

**Wed. 3:41 AM ET (07:41 UTC):** more than six hours before the coordinated release, Chainguard published built images with the fix; the Foundation says it unilaterally broke the embargo. [5]

**Wed. by 5:10 AM ET:** NOS, at 11:10 Amsterdam time, lists Dutch government and education sites taken offline as a precaution. [20]

**Wed. 7:26 AM and 10:19 AM ET (11:26 and 14:19 UTC):** watchTowr reported no exploitation, then attempts in its honeypots, as The Hacker News logged; watchTowr’s own page went up at 14:19 UTC. [16][27]

**Wed. 7:51 AM to 2:01 PM ET (11:51 to 18:01 UTC):** BambooHR offline, then back online following security patching and validation. [19]

**Wed. 10 AM ET (14:00 UTC):** PHP releases 8.5.12, 8.4.27, 8.3.36 and 8.2.35. [1] The Foundation says its team did not identify any functional exploits at the time of release/public disclosure. [5]

**Wed. 9:25 PM ET (01:25 UTC Thu.):** Prince’s post. Reuters calls it late Wednesday; outlets on UTC date it Thursday. [13][29]

How long it lived

### The affected releases go back to PHP 5.4, from March 2012.

Years run left to right; the dashed box on the axis is the zoomed stretch. [5][7][8][9][10]

- **2004.** Stefan Esser’s advisory: an attacker could trigger the memory_limit request termination in places where an interruption is unsafe and run code on PHP servers. [9] Calif traces its find to that line of research. [8]
- **2012.** PHP 5.4.0 came out March 1, 2012. [10] Wiz says releases back to PHP 5.4 are affected. [7]
- **2024.** While fixing one of the issues Quarkslab reported, a PHP core developer contracted by the PHP Foundation found the first signs of the OOM problem behind CVE-2026-109618. Then, a potential exploit for the OOM problem was theorized, but no concrete vectors were found. [5]
- **The delay.** We won’t pretend otherwise: the delay was a structural failure, caused by both the security team’s decision process and its lack of resources. The Foundation says it has since added people, a security team and tools. [5]
- **71 days** from Calif’s first report on Aug. 11 to the fix on Oct. 21. [5][8]

Who found it

### Three research teams, working with AI models, found it and reported it.

#### Calif

Ryan Austin

Found Aug. 1 · reported Aug. 11

Joined OpenAI’s Patch the Planet program July 30, where PHP stood out as a high-impact target. [8]

> Models do not reliably begin with obscure twenty-year-old exploitation primitives. [8]

#### OpenAI Codex Security

Amy Burnett

Same root cause · more on Sept. 18

OpenAI independently reported the same root cause as Calif, followed by further attack vectors from OpenAI on September 18th, the PHP Foundation says. [5]

#### Wiz Research

Sagi Tzadik, Shir Tamari, Nir Ohfeld, Tomer Schwartz

Found Aug. 19 · reported Aug. 24

Used Wiz Atlas, Gemini 4 Argon and GPT-5.6 Sol, by Wiz’s account. [7]

> a single researcher completed in a week what previously would have taken a world-class team months of work. [7]

#### The PHP security team

Confirmed Calif’s proof of concept Aug. 15 [8] and acknowledged Wiz’s reports Sept. 21. [7] The three teams worked with the PHP security team and the Gemini team at Google on discovery, coordination and patch verification. [6]

#### Oct. 21: the fix

8.5.12, 8.4.27, 8.3.36 and 8.2.35. [1]

> No model is simply capable of unearthing all bugs with simple prompts. At least for now. [8] · Calif

> AI helps the team validate reports and group reports sharing the same root cause, and a person makes every call and works on every patch. [5] · The PHP Foundation

> Frontier models helped work through complex exploit chains and adapt them across different deployments. [6] · The three research teams, on php2shell.com

Sources

1. The PHP Group, “Security advisory: Critical remote code execution vulnerabilities, update now,” and the PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35 release notes, Oct. 21, 2026, [php.net/archive/2026.php](https://www.php.net/archive/2026.php#2026-10-21-5), read Oct. 22, 2026.
2. The PHP Group, “Upcoming Critical PHP Security Release,” Oct. 20, 2026, [php.net/archive/2026.php](https://www.php.net/archive/2026.php#2026-10-20-1).
3. PHP security advisory GHSA-w8hw-w9fx-j79w, “RCE via OOM corruption,” CVE-2026-109618, Oct. 21, 2026, [github.com/php/php-src](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w).
4. PHP security advisory GHSA-6wmf-4rv5-p3rp, “RCE via stale global state,” CVE-2026-109619, Oct. 21, 2026, [github.com/php/php-src](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp).
5. The PHP Foundation, “Today’s PHP Security Release, and How We’re Strengthening PHP Security,” Oct. 21, 2026, [thephp.foundation/blog](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/).
6. Wiz Research, Calif and OpenAI Codex Security, “PHP2Shell,” [php2shell.com](https://www.php2shell.com/), read Oct. 22, 2026.
7. Sagi Tzadik, Shir Tamari, Nir Ohfeld and Tomer Schwartz, Wiz Research, “PHP2Shell: AI uncovers critical RCE vulnerabilities affecting 70% of the Internet,” Oct. 21, 2026, [wiz.io/blog](https://www.wiz.io/blog/php2shell-php-rce).
8. Calif, “php2shell,” [calif.io/php2shell](https://calif.io/php2shell), read Oct. 22, 2026.
9. Stefan Esser, “Advisory 11/2004: PHP memory_limit remote vulnerability,” Bugtraq, July 14, 2004, [marc.info](https://marc.info/?l=bugtraq&m=108981780109154&w=2).
10. The PHP Group, PHP 5 ChangeLog, “Version 5.4.0, 01 Mar 2012,” [php.net/ChangeLog-5.php](https://www.php.net/ChangeLog-5.php#5.4.0).
11. The PHP Group, home page, [php.net](https://www.php.net/), read Oct. 22, 2026.
12. Cloudflare, “Cloudflare deploys protections against php2shell vulnerability,” Oct. 21, 2026, [blog.cloudflare.com](https://blog.cloudflare.com/php-vulnerabilities-waf-protection).
13. Matthew Prince, post on X, [x.com/eastdakota](https://x.com/eastdakota/status/2113079352682570051); text as printed by OfficeChai, Oct. 22, 2026 ([officechai.com](https://officechai.com/stories/cloudflare-ceo-says-php-exploit-attempts-went-from-thousands-to-millions-within-hours-of-disclosure/)) and Reuters [29]. The post time, 01:25 UTC Oct. 22, is read from the post’s ID.
14. Mirko Zorz, Help Net Security, “PHP2Shell: Critical PHP vulnerabilities patched, update now!,” Oct. 21, 2026, updated Oct. 22, [helpnetsecurity.com](https://www.helpnetsecurity.com/2026/10/21/php2shell-php-vulnerabilities-patched-cve-2026-109618-cve-2026-109619/): Dane Knecht’s post on X ([x.com/dok2001](https://x.com/dok2001/status/2112811965735202970)).
15. Cloudflare, “Application services,” [cloudflare.com/application-services](https://www.cloudflare.com/application-services/), read Oct. 22, 2026.
16. watchTowr, “PHP Remote Code Execution (PHP2Shell),” Oct. 21, 2026, 14:19 UTC, [watchtowr.com](https://watchtowr.com/intelligence/php-remote-code-execution-php2shell/), and “PHP RCE FAQ,” Oct. 20, 2026, [watchtowr.com](https://watchtowr.com/intelligence/php-cve-2026-109618-faq/).
17. CJ Moses, Amazon, “Amazon threat intelligence identifies PHP2Shell exploitation prior to public disclosure in MadPot,” Oct. 21, 2026, [aws.amazon.com/blogs/security](https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/).
18. Cybersecurity and Infrastructure Security Agency, “Critical Vulnerabilities in PHP Require Immediate Patching,” Oct. 21, 2026, [cisa.gov](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching).
19. BambooHR status page, “BambooHR Temporarily Unavailable: Security Precaution,” Oct. 21, 2026, [status.bamboohr.com](https://status.bamboohr.com/).
20. NOS, “Websites van overheid en in onderwijs offline vanwege lek, risico op hacks,” Oct. 21, 2026, [nos.nl](https://nos.nl/artikel/2636055-websites-van-overheid-en-in-onderwijs-offline-vanwege-lek-risico-op-hacks) (in Dutch).
21. NOS, “Signalen bij Nationaal Cyber Security Centrum van misbruik PHP-lek,” Oct. 22, 2026, [nos.nl](https://nos.nl/artikel/2636225-signalen-bij-nationaal-cyber-security-centrum-van-misbruik-php-lek) (in Dutch).
22. University of Washington IT, “PHP CVEs,” updated Oct. 22, 2026, [it.uw.edu](https://it.uw.edu/help/servicestatus/php-cves/).
23. W3Techs, “Usage statistics of PHP for websites,” data of Oct. 22, 2026, [w3techs.com](https://w3techs.com/technologies/details/pl-php).
24. W3Techs, “Usage statistics of WordPress,” data of Oct. 22, 2026, [w3techs.com](https://w3techs.com/technologies/details/cm-wordpress).
25. W3Techs, “Usage statistics of Cloudflare,” October 2026, [w3techs.com](https://w3techs.com/technologies/details/cn-cloudflare).
26. Debian security tracker, CVE-2026-109618, [security-tracker.debian.org](https://security-tracker.debian.org/tracker/CVE-2026-109618), read Oct. 22, 2026.
27. Swati Khandelwal, The Hacker News, “PHP Issues Emergency Patches for Two Critical PHP2Shell RCE Flaws as Exploit Attempts Emerge,” Oct. 21, 2026, [thehackernews.com](https://thehackernews.com/2026/10/php-issues-emergency-patches-for-two.html).
28. Lawrence Abrams, BleepingComputer, “PHP warns admins of two critical flaws, emergency patches coming tomorrow,” Oct. 20, 2026, 4:56 PM ET, [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/php-warns-admins-of-two-critical-flaws-emergency-patches-coming-tomorrow/).
29. Eduardo Baptista, Toby Sterling and Mariko Katsumura, Reuters, “Cloudflare sees millions of exploit attempts after PHP disclosure,” Oct. 22, 2026, via [globalbankingandfinance.com](https://www.globalbankingandfinance.com/cloudflare-sees-millions-exploit-attempts-php-disclosure/).
30. CERT-EU, Security Advisory 2026-018, Oct. 21, 2026, [cert.europa.eu](https://cert.europa.eu/publications/security-advisories/2026-018/).
31. UK National Cyber Security Centre, “Critical security issue affecting PHP,” Oct. 21, 2026, [ncsc.gov.uk](https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php).

The grid, the strips, the attack drawing, the attempt chart, the timeline and the ruler are drawn for this story from the sources above. The attempt chart draws Prince’s words as ranges on a log scale. Times are converted from UTC to Eastern (EDT). Translations from Dutch are ours. PHP is a trademark of the PHP Group; Cloudflare, WordPress and the other names are trademarks of their owners. No logos are reproduced.

Built by **Dustin Nimmo**, founder of [DNSC](https://dnsc.ai) in West Chester, Ohio.

Last verified Oct. 22, 2026. If a fact here is wrong, say so and it will be fixed and noted.

---

Source: https://tools.dnsc.ai/stories/php2shell/ · Generated from the page on Nov 8, 2026
