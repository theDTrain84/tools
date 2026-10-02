# Lunar Life calendar relay

**What it's for.** Lunar Life shows the moon over your real weeks. To read a calendar, the page needs the calendar's private .ics link, and browsers block a web page from fetching most of those links directly. This tiny relay fetches the link the visitor gives it and hands the calendar straight back. It stores nothing, logs nothing and passes no cookies. It only answers requests coming from tools.dustinnimmo.com, only fetches https links, only returns real calendar files, gives up after 10 seconds, and refuses anything over 2 MB.

**Cost.** Free. Cloudflare's free Workers plan covers 100,000 requests a day.

## Setup, about ten minutes, all your clicks

1. **Make a free Cloudflare account** at dash.cloudflare.com/sign-up (any email). Skip the domain prompts if it offers them.
2. In the left sidebar, open **Workers & Pages**, then **Create**, then **Create Worker** ("Hello World" is fine as the starting point).
3. Name it `lunar-relay` and click **Deploy**. It now lives at `https://lunar-relay.<your-subdomain>.workers.dev`.
4. Click **Edit code**. Select everything in the editor, delete it, and paste the full contents of `worker.js` from this folder. Click **Deploy** (top right).
5. **Test it.** Open this in your browser, with your subdomain filled in:
   `https://lunar-relay.<your-subdomain>.workers.dev/?url=https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics`
   You should see a page of text starting with `BEGIN:VCALENDAR`. That means it works.
6. **Send the workers.dev address to Mise.** We'll point Lunar Life at it. That's it.

### Optional: a nicer address (relay.dustinnimmo.com)

Only if you want it. It needs the domain's DNS moved to Cloudflare, which is a bigger change (GoDaddy keeps registering the domain, but Cloudflare would run the DNS for the whole site). The workers.dev address works just as well, and visitors never see it. Say the word and we'll walk through it together.

## Where to find your private calendar link (for testing)

- **Google Calendar:** Settings → pick the calendar on the left → "Integrate calendar" → **Secret address in iCal format**.
- **Apple iCloud:** Calendar app → right-click the calendar → Share Calendar → Public Calendar → copy the `webcal://` link (the relay accepts it).
- **Outlook:** Settings → Calendar → Shared calendars → Publish a calendar → ICS link.

Treat a secret calendar link like a password. The relay doesn't keep it, but don't post it anywhere public.
