#!/usr/bin/env python3
"""Generates civic/data-centers-on-the-ballot/index.html from the desk's data.json.
Numbers are never typed by hand: every count, share and margin comes from the file."""
import json, html, re
D = json.load(open('/Users/dustinnimmo/DNSC/thesis/pitches/2026-11-04/datacenters/data.json'))
OUT = '/Users/dustinnimmo/DNSC/tools-site/civic/data-centers-on-the-ballot/index.html'

# ---------- sources: numbered in order of first citation ----------
SRC = {
 'bp_roster': ('Ballotpedia, &ldquo;Data center-related ballot measures, 2026,&rdquo; the roster of 41 November 3 questions with election-night counts', 'https://ballotpedia.org/Data_center-related_ballot_measures,_2026'),
 'bp_news': ('Ballotpedia News, &ldquo;Voters in ten states will vote on data center-related ballot measures November 3,&rdquo; November 3, 2026', 'https://news.ballotpedia.org/2026/11/03/voters-in-ten-states-will-vote-on-data-center-related-ballot-measures-november-3/'),
 'redbud': ('Redbud Consulting, &ldquo;Data Centers on the Ballot,&rdquo; results file generated November 4, 2026, 10:22 AM ET; adds Americus, Kansas, and Eliot, Sabattus, Brownfield and Freedom, Maine, to the roster', 'https://datacentersontheballot.com/'),
 'railway': ('&ldquo;Data centers and AI on the ballot,&rdquo; a public dashboard compiled November 3, 2026, which lists the official results page for each jurisdiction', 'https://dashboard-production-c2fc.up.railway.app/'),
 'doe': ('U.S. Department of Energy, &ldquo;DOE Releases New Report Evaluating Increase in Electricity Demand from Data Centers,&rdquo; December 20, 2024, summarizing the Lawrence Berkeley National Laboratory report', 'https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers'),
 'eia_jan': ('U.S. Energy Information Administration, press release, January 13, 2026, on the Short-Term Energy Outlook', 'https://www.eia.gov/pressroom/releases/press582.php'),
 'eia_tie': ('U.S. Energy Information Administration, Today in Energy, May 19, 2026, on servers&rsquo; share of commercial-sector electricity', 'https://www.eia.gov/todayinenergy/detail.php?id=67704'),
 'eia_steo': ('U.S. Energy Information Administration, Short-Term Energy Outlook, September 2026', 'https://www.eia.gov/outlooks/steo/archives/sep26.pdf'),
 'sc_pdf': ('Supreme Court of Ohio, <i>State ex rel. Blankenship v. Trenton City Council</i>, 2026-Ohio-3406, No. 2026-1035, decided September 1, 2026, slip opinion', 'https://www.supremecourt.ohio.gov/rod/docs/pdf/0/2026/2026-Ohio-3406.pdf'),
 'courtnews': ('Court News Ohio, case summary, <i>State ex rel. Blankenship v. Trenton City Council</i>, September 1, 2026', 'https://courtnewsohio.gov/cases/2026/SCO/0901/261035.asp'),
 # Ohio counties
 'butler': ('Butler County Board of Elections, unofficial results, November 3, 2026, Issue 17 City of Trenton, 8 of 8 precincts', 'https://liveresults.boe.ohio.gov/ENR/butlerohenr/24/en/Index_24.html'),
 'champaign': ('Champaign County Board of Elections, unofficial results, November 3, 2026 (PDF)', 'https://www.boe.ohio.gov/champaign/c/elecres/20261103results.pdf'),
 'miami': ('Miami County Board of Elections, unofficial results, November 3, 2026, general report (PDF)', 'https://www.boe.ohio.gov/miami/c/elecres/20261103results.pdf'),
 'trumbull': ('Trumbull County Board of Elections, election summary, November 3, 2026 (PDF)', 'https://boe.co.trumbull.oh.gov/pdfs/Election%20Summary.pdf'),
 'defiance': ('Defiance County Board of Elections, unofficial results, November 3, 2026 (PDF)', 'https://www.boe.ohio.gov/defiance/c/elecres/20261103results.pdf'),
 'ashtabula': ('Ashtabula County Board of Elections, unofficial results, November 3, 2026 (PDF)', 'https://www.boe.ohio.gov/ashtabula/c/elecres/20261103results.pdf'),
 'licking': ('Licking County Board of Elections, unofficial cumulative results, November 3, 2026 (PDF)', 'https://www.boe.ohio.gov/licking/c/elecres/20261103results.pdf'),
 'wyandot': ('Wyandot County Board of Elections, unofficial results, November 3, 2026 (scanned PDF)', 'https://www.boe.ohio.gov/wyandot/c/elecres/20261103results.pdf'),
 'adams': ('Adams County Board of Elections, unofficial results, November 3, 2026 (scanned PDF)', 'https://www.boe.ohio.gov/adams/c/elecres/20261103results.pdf'),
 'clinton': ('Clinton County Board of Elections, unofficial cumulative results, November 3, 2026 (PDF)', 'https://www.boe.ohio.gov/clinton/c/elecres/20261103results.pdf'),
 'delaware': ('Delaware County Board of Elections, unofficial summary report, November 3, 2026 (scanned PDF)', 'https://vote.delawarecountyohio.gov/wp-content/uploads/2026/11/Delawares-Unofficial-Summary-Report.pdf'),
 'lucas': ('Lucas County Board of Elections, results page', 'https://www.lucascountyohiovotes.gov/'),
 'franklin_oh': ('Franklin County Board of Elections, results page', 'https://vote.franklincountyohio.gov/'),
 'lake': ('Lake County Board of Elections, election results page', 'https://www.lakecountyohio.gov/boe/election-results/'),
 'huron': ('Huron County Board of Elections, unofficial canvass, November 3, 2026 (PDF)', 'https://www.huron.boe.ohio.gov/wp-content/uploads/Huron-County-Unofficial-Canvass-11-3-2026.pdf'),
 'pickaway': ('Pickaway County Board of Elections, results file for November 3, 2026 (PDF; the file at this link was still the pre-count zero report when this desk fetched it)', 'https://www.boe.ohio.gov/pickaway/c/elecres/20261103results.pdf'),
 # national official
 'lavote': ('Los Angeles County Registrar-Recorder/County Clerk, election results, November 3, 2026', 'https://results.lavote.gov/#year=2026&election=4348'),
 'volusia': ('Volusia County Supervisor of Elections, 2026 general election results', 'https://app.enhancedvoting.com/results/public/volusia-county-fl/elections/2026GeneralElection'),
 'bloomington': ('Bloomington Election Commission (Illinois), results feed, November 3, 2026', 'https://results.enr.clarityelections.com/IL/Bloomington/127392/'),
 'madison_il': ('Madison County Clerk (Illinois), results feed, November 3, 2026', 'https://results.enr.clarityelections.com/IL/Madison/127555/'),
 'will_il': ('Will County Clerk (Illinois), results feed, November 3, 2026', 'https://results.enr.clarityelections.com/IL/Will/127394/'),
 'morgan_il': ('Morgan County Clerk (Illinois); the clerk posts no results online', 'https://morgancounty-il.com/wp/departments/county-clerk/'),
 'butler_ks': ('Butler County, Kansas, election results, November 3, 2026', 'https://www.livevoterturnout.com/ENR/butlerksenr/4/en/Index_4.html'),
 'lyon_ks': ('Lyon County, Kansas, &ldquo;Unofficial Final&rdquo; results, November 3, 2026 (PDF)', 'https://www.lyoncountyks.gov/DocumentCenter/View/2423'),
 'franklin_ks': ('Franklin County, Kansas, election results page', 'https://www.franklincoks.org/1067/Election-Results'),
 'northberwick': ('Town of North Berwick, Maine, general election results, November 2026 (scanned PDF)', 'https://www.townofnorthberwick.org/DocumentCenter/View/1599/General-Election-November-4-2026'),
 'peru': ('Town of Peru, Maine', 'https://townofperumaine.org/'),
 'wells': ('Town of Wells, Maine, election results (scanned PDF)', 'https://www.wellstown.org/DocumentCenter/View/8557'),
 'wiscasset': ('Town of Wiscasset, Maine, Town Clerk, elections', 'https://www.wiscasset.gov/192/Town-Clerk-Elections'),
 'eliot': ('Town of Eliot, Maine, moderator&rsquo;s return of votes cast, November 3, 2026 (scanned PDF)', 'https://www.eliotme.gov/DocumentCenter/View/3997/Election-Results-November-3-2026---Eliot-Maine-PDF'),
 'sabattus': ('Town of Sabattus, Maine, clerk&rsquo;s return of votes, municipal election, November 3, 2026 (scanned PDF)', 'https://storage.googleapis.com/juniper-media-library/571/2026/11/Sabattus%20-%20Clerk%20Return%20of%20Votes%20-%20Municipal%20Election.pdf'),
 'brownfield': ('Town of Brownfield, Maine, town warrants and reports', 'https://www.brownfieldmaine.gov/1196/Past-Town-Warrants-Reports'),
 'freedom': ('Town of Freedom, Maine', 'https://www.freedomme.org/'),
 'nd_sos': ('North Dakota Secretary of State, election results, Cass County, November 3, 2026', 'https://resultsnd.sos.nd.gov/#bucket=results&filter=SW&contest=22055&location=cass+county'),
 'routefifty': ('Route Fifty, &ldquo;Voters reject data centers in local ballot initiatives,&rdquo; November 2026, quoting the North Dakota Secretary of State on Harwood', 'https://www.route-fifty.com/artificial-intelligence/2026/11/voters-reject-data-centers-local-ballot-initiatives/417033/'),
 'cumberland_nj': ('Cumberland County Clerk (New Jersey), results feed, November 3, 2026', 'https://results.enr.clarityelections.com/NJ/Cumberland/127562/'),
 'clark_nv': ('Clark County, Nevada, Election Department, results', 'https://elections.clarkcountynv.gov/electionresultsTV/'),
 'rock_wi': ('Rock County, Wisconsin, County Clerk, election results, November 3, 2026', 'https://www.co.rock.wi.us/departments/county-clerk/election-information/election-results-november-3-2026'),
 # Ohio press, roster
 'fortune': ('Fortune, &ldquo;Ohio data center ballot measures,&rdquo; November 4, 2026 (21 measures in 18 municipalities)', 'https://fortune.com/2026/11/04/ohio-data-center-ballot-measures-midterm-elections/'),
 'nbc4': ('NBC4 Columbus, &ldquo;Columbus-area communities vote on data center issues,&rdquo; live results, November 3 to 4, 2026', 'https://www.nbc4i.com/news/your-local-election-hq/columbus-area-communities-vote-on-data-center-issues-live-results/'),
 'ideastream': ('Ideastream Public Media, &ldquo;Northeast Ohio communities cast votes against data centers,&rdquo; November 4, 2026', 'https://www.ideastream.org/government-politics/2026-11-04/northeast-ohio-communities-cast-votes-against-data-centers'),
 # Trenton
 'wcpo': ('WCPO, &ldquo;Public hearing canceled after Trenton withdraws annexation petition for proposed Amazon data center,&rdquo; September 2026', 'https://www.wcpo.com/news/local-news/in-your-community/butler-county/public-hearing-canceled-after-trenton-withdraws-annexation-petition-for-proposed-amazon-data-center'),
 'wvxu_annex': ('WVXU, &ldquo;Madison Township objects to Trenton annexation for hyperscale data center,&rdquo; August 25, 2026', 'https://www.wvxu.org/local-news/2026-08-25/madison-township-trenton-annex-hyperscale-data-center'),
 'wvxu_mora': ('WVXU, &ldquo;Butler County approves data center moratorium,&rdquo; June 17, 2026', 'https://www.wvxu.org/environment/2026-06-17/butler-county-approves-data-center-moratorium'),
 'jn_mora': ('Journal-News, &ldquo;&lsquo;We have to understand what we are committing to&rsquo;: Butler County approves 6-month data center moratorium,&rdquo; June 2026', 'https://www.journal-news.com/local/we-have-to-understand-what-we-are-committing-to-butler-county-approves-6-month-data/article_cdf1ab44-e310-5697-8a14-ebbf0311f198.html'),
 'wyso': ('WYSO, &ldquo;Trenton approves 15-year tax abatement for data center,&rdquo; July 9, 2026', 'https://www.wyso.org/2026-07-09/trenton-approves-15-year-tax-abatement-for-data-center'),
 'dcd': ('Data Center Dynamics, &ldquo;Prologis details plans for data center campus outside Cincinnati, Ohio&rdquo;', 'https://www.datacenterdynamics.com/en/news/prologis-details-plans-for-data-center-campus-outside-cincinnati-ohio/'),
 # statehouse
 'hb646': ('Ohio House of Representatives, H.B. 646, 136th General Assembly, status and history', 'https://ohiohouse.gov/legislation/136/hb646/status'),
 'sb374': ('Ohio Senate, S.B. 374, 136th General Assembly, status and history', 'https://ohiosenate.gov/legislation/136/sb374/status'),
 'hb710': ('Ohio House of Representatives, H.B. 710, 136th General Assembly, status and history', 'https://ohiohouse.gov/legislation/136/hb710/status'),
 'hb957': ('Ohio House of Representatives, H.B. 957, 136th General Assembly, status and history', 'https://ohiohouse.gov/legislation/136/hb957/status'),
 'orc122': ('Ohio Revised Code 122.175, tax exemption for sale, storage, use, or other consumption of computer data center equipment', 'https://codes.ohio.gov/ohio-revised-code/section-122.175'),
 'jobsohio': ('JobsOhio, &ldquo;Data Center Tax Exemption,&rdquo; program page', 'https://www.jobsohio.com/incentives-programs/data-center-tax-exemption'),
 'puco': ('Public Utilities Commission of Ohio, bulletin on the AEP Ohio data center tariff order, Case No. 24-508-EL-ATA, July 9, 2025', 'https://content.govdelivery.com/accounts/OHPUC/bulletins/3e8bb79'),
 'powermag': ('POWER, &ldquo;Regulator Approves AEP Ohio&rsquo;s Landmark Data Center Tariff,&rdquo; July 2025, on the terms of the order', 'https://www.powermag.com/regulator-approves-aep-ohios-landmark-data-center-tariff/'),
 'summit': ('Ohio AI Summit, agenda, November 18, 2026, Columbus State Community College', 'https://www.ohioaisummit.org/agenda'),
 'orc3505': ('Ohio Revised Code 3505.32, canvass of election returns', 'https://codes.ohio.gov/ohio-revised-code/section-3505.32'),
}
ORDER = []
def num(k):
    if k not in SRC: raise KeyError(k)
    if k not in ORDER: ORDER.append(k)
    return ORDER.index(k) + 1
def c(*keys):
    return '<span class="c">' + ''.join(f'<a href="#s{num(k)}">[{num(k)}]</a>' for k in keys) + '</span>'

def fmt(n): return f'{n:,}'
def pct(x): return f'{x:.1f}'

# ---------- rows ----------
ALLOW_KINDS = ('advisory (allow)', 'allow', 'zoning referendum', 'referendum on development agreement')
def limit_is_no(kind): return kind.startswith(ALLOW_KINDS)
def shares(m):
    y, n = m['yes'], m['no']
    if y is None: return None
    tot = y + n
    lim = n if limit_is_no(m['kind']) else y
    return dict(py=y / tot * 100, lim=lim / tot * 100, margin=(n - y) if limit_is_no(m['kind']) else (y - n))

def kind_chip(kind):
    k = kind
    if k.startswith('ban (size cap'): return ('Size cap', 'cap')
    if k.startswith('ban (charter') or k == 'ban': return ('Ban', 'ban')
    if k.startswith('ban'): return ('Ban', 'ban')
    if k.startswith('moratorium'): return ('Moratorium', 'mor')
    if k.startswith('voter-approval'): return ('Voter approval', 'vote')
    if k.startswith('zoning referendum'): return ('Rezoning referendum', 'ref')
    if k.startswith('zoning (adopt'): return ('Adopt zoning', 'zon')
    if k.startswith('advisory (allow)'): return ('Advisory: allow?', 'adv')
    if k.startswith('advisory (limit)'): return ('Advisory: limit?', 'adv')
    if k.startswith('tax-incentive'): return ('Incentive terms', 'tax')
    if k.startswith('referendum on development'): return ('Agreement referendum', 'ref')
    if k.startswith('review requirement'): return ('Review requirement', 'rev')
    if k.startswith('allow'): return ('Allow as a use', 'allow')
    return (k, 'other')

STATE_NAME = {'OH': 'Ohio', 'ME': 'Maine', 'IL': 'Illinois', 'KS': 'Kansas', 'CA': 'California', 'FL': 'Florida', 'ND': 'North Dakota', 'NJ': 'New Jersey', 'NV': 'Nevada', 'WI': 'Wisconsin'}

# Ohio: place names his way, official source keys, tracker flag
OH_SRC = {'Butler': 'butler', 'Champaign': 'champaign', 'Miami': 'miami', 'Trumbull': 'trumbull', 'Defiance': 'defiance', 'Ashtabula': 'ashtabula', 'Licking': 'licking', 'Wyandot': 'wyandot', 'Adams': 'adams', 'Clinton': 'clinton', 'Delaware': 'delaware', 'Lucas': 'lucas', 'Franklin': 'franklin_oh', 'Lake': 'lake', 'Huron': 'huron', 'Pickaway': 'pickaway'}
def oh_name(j):
    m = re.match(r'(.+?) \((city|village)\)', j)
    if m: return ('City of ' if m.group(2) == 'city' else 'Village of ') + m.group(1)
    return j  # townships
def oh_tracker(m): return m['status'].startswith('tracker')

OH_EFFECT = {  # plain words, from the data's effect lines
 'Trenton (city)': 'Charter amendment: no data center above 25 megawatts of monthly demand or peak load. The Prologis campus already under construction is outside its reach.',
 'Urbana (city)': 'Charter amendment: no data centers built in the city.',
 'Piqua (city)': 'Charter amendment: no data center built in the city.',
 'Hubbard (city)': 'Initiated ordinance: no data centers inside city limits, with no megawatt line.',
 'Defiance (city)': 'Charter amendment: no data center above 25 megawatts of demand or peak load.',
 'Conneaut (city)': 'Charter amendment: no data center above 25 megawatts of monthly demand or peak load.',
 'Pataskala (city)': 'Charter amendment: no large-scale data centers built in the city.',
 'Granville (village)': 'Charter amendment: no data centers built in the village.',
 'Upper Sandusky (city)': 'Charter amendment, placed by council: no data center built in the city.',
 'Monroe Township': 'Adopts township zoning for the unincorporated area, which gives the trustees say over where a data center may go on farmland.',
 'Sprigg Township': 'Adopts township zoning for the unincorporated area, which gives the trustees say over where a data center may go on farmland.',
 'Sunbury (city)': 'Charter amendment: no data center above 25 megawatts; aimed at a proposed Amazon hyperscale project.',
 'Oregon (city)': 'Charter amendment: no data center above 25 megawatts of monthly demand or peak load.',
 'Grove City (city)': 'Charter amendment: a public vote before any development, expansion or property transfer of 50 or more contiguous acres, 20 or more megawatts of peak demand, or 500,000 or more gallons of water a day.',
 'Perry (village)': 'Ordinance: a hyperscale data center developer seeking a tax abatement or other incentive must post financial guarantees; also size and noise limits.',
 'Monroeville (village)': 'Advisory, nonbinding: should the village allow data center development? Yes meant allow.',
 'Ashville (village)': 'Referendum by petition: yes kept the term summary guiding the village&rsquo;s negotiations with EdgeConneX for two data centers; no rejected it.',
}
WILM = {'O-26-04': '65.29 acres at 1957 SR 730', 'O-26-05': '191.12 acres at McGuinn Road', 'O-26-06': '119.373 acres at SR 730', 'O-26-07': '170.11 acres at US 68 South'}

NAT_NAME = {
 'Alhambra (Los Angeles County)': ('City of Alhambra', 'Los Angeles County', 'lavote'),
 'Edgewater (Volusia County)': ('City of Edgewater', 'Volusia County', 'volusia'),
 'Bloomington (city; own election board)': ('City of Bloomington', 'McLean County; the city runs its own election board', 'bloomington'),
 'Chouteau Township (Madison County)': ('Chouteau Township', 'Madison County', 'madison_il'),
 'Granite City Township (Madison County)': ('Granite City Township', 'Madison County', 'madison_il'),
 'Nameoki Township (Madison County)': ('Nameoki Township', 'Madison County', 'madison_il'),
 'Venice Township (Madison County)': ('Venice Township', 'Madison County', 'madison_il'),
 'Joliet Township (Will County)': ('Joliet Township', 'Will County', 'will_il'),
 'Morgan County': ('Morgan County', 'countywide', 'morgan_il'),
 'El Dorado (Butler County)': ('City of El Dorado', 'Butler County', 'butler_ks'),
 'Emporia (Lyon County)': ('City of Emporia', 'Lyon County', 'lyon_ks'),
 'Americus (Lyon County)': ('City of Americus', 'Lyon County', 'lyon_ks'),
 'Ottawa (Franklin County)': ('City of Ottawa', 'Franklin County', 'franklin_ks'),
 'North Berwick (York County)': ('Town of North Berwick', 'York County', 'northberwick'),
 'Peru (Oxford County)': ('Town of Peru', 'Oxford County', 'peru'),
 'Wells (York County)': ('Town of Wells', 'York County', 'wells'),
 'Wiscasset (Lincoln County)': ('Town of Wiscasset', 'Lincoln County', 'wiscasset'),
 'Eliot (York County)': ('Town of Eliot', 'York County', 'eliot'),
 'Sabattus (Androscoggin County)': ('Town of Sabattus', 'Androscoggin County', 'sabattus'),
 'Brownfield (Oxford County)': ('Town of Brownfield', 'Oxford County', 'brownfield'),
 'Freedom (Waldo County)': ('Town of Freedom', 'Waldo County', 'freedom'),
 'Harwood (Cass County)': ('City of Harwood', 'Cass County', 'nd_sos'),
 'Downe Township (Cumberland County)': ('Downe Township', 'Cumberland County', 'cumberland_nj'),
 'Boulder City (Clark County)': ('Boulder City', 'Clark County', 'clark_nv'),
 'Janesville (Rock County)': ('City of Janesville', 'Rock County', 'rock_wi'),
}
NAT_EFFECT = {
 'Alhambra (Los Angeles County)': 'Measure DB: no data centers in the city.',
 'Edgewater (Volusia County)': 'Charter Amendment No. 4: no approval, construction, expansion or operation of new data centers in the city.',
 'Bloomington (city; own election board)': 'Advisory: should the city impose a moratorium on large data centers? Yes meant limit.',
 'Chouteau Township (Madison County)': 'Advisory: should officials permit new data centers? Yes meant allow.',
 'Granite City Township (Madison County)': 'Advisory: should officials permit new data centers? Yes meant allow.',
 'Nameoki Township (Madison County)': 'Advisory: should officials permit new data centers? Yes meant allow.',
 'Venice Township (Madison County)': 'Advisory: should officials permit new data centers? Yes meant allow.',
 'Joliet Township (Will County)': 'Advisory: should the township approve construction of AI data centers? Yes meant allow.',
 'Morgan County': 'Advisory: should the county restrict data center construction and operation? Yes meant limit.',
 'El Dorado (Butler County)': 'No high-impact data centers or Type 2 and 3 battery storage for ten years.',
 'Emporia (Lyon County)': 'Ballot Question 2: no high-impact data centers (above 10 megawatts or 100,000 gallons of water a day). A court has the ban on hold while it decides whether the subject can be set by citizen petition.',
 'Americus (Lyon County)': 'No high-impact data centers or large battery storage.',
 'Ottawa (Franklin County)': 'Question 2: no data centers above 25 megawatts for ten years. Its validity is still before the district court.',
 'North Berwick (York County)': 'Question 2: no data centers of 25,000 square feet or more.',
 'Peru (Oxford County)': 'Article 2: a 180-day moratorium on data center development and permits.',
 'Wells (York County)': 'Article 5: a 180-day moratorium on data center development; also voids recent permits.',
 'Wiscasset (Lincoln County)': 'Question 2: a six-month moratorium on applications for new or expanded data centers.',
 'Eliot (York County)': 'Question 5: a 180-day moratorium on data centers of any size.',
 'Sabattus (Androscoggin County)': 'A temporary moratorium, to May 2027, on data centers of 10,000 square feet or 20 megawatts or more.',
 'Brownfield (Oxford County)': 'Question 1: a 180-day moratorium on data centers of 5,000 square feet or more.',
 'Freedom (Waldo County)': 'A temporary moratorium on data centers of any size.',
 'Harwood (Cass County)': 'Home rule charter amendment: independent review and a public hearing before approval of large industrial projects, data centers included. It would have reached future projects; the approved Applied Digital campus was outside it.',
 'Downe Township (Cumberland County)': 'Advisory: do residents support data center development? Yes meant support.',
 'Boulder City (Clark County)': 'Question 1: add data centers as an approved use in the Eldorado Valley Transfer Area. Yes meant allow.',
 'Janesville (Rock County)': 'A public vote before the city leases, sells or approves development of the former GM/JATCO site for any project above $450 million; tied to a proposed $8 billion data center.',
}
TRACKER_SRC = {  # which tracker read gave the number for tracker-only rows
 'ballotpedia': 'bp_roster', 'redbud': 'redbud'}
def nat_tracker_key(m):
    return 'bp_roster' if 'ballotpedia' in m['tracker_url'] else 'redbud'

def row_html(name, meta, kind, effect, m, src_keys, tracker, official_url, state_tag=''):
    chip, cls = kind_chip(kind)
    s = shares(m)
    lim_no = limit_is_no(kind)
    cites = c(*src_keys)
    official = f'<a class="off" href="{html.escape(official_url)}" rel="noopener">official results page</a>'
    tr = '<i class="tr" title="Count read from a tracker; the official sheet could not be reached by this desk">tracker only</i>' if tracker else ''
    if s is None:
        return f'''<div class="row pend">
  <div class="who"><b>{name}</b><span>{meta} {cites}</span><span>{official}</span></div>
  <div class="kind"><i class="{cls}">{chip}</i>{effect}</div>
  <div class="bar none" aria-hidden="true"></div>
  <div class="nums"><span><small>count</small>none posted yet</span></div>
  <div class="res">No count yet</div>
</div>'''
    won = m.get('restrict_won', m.get('restrict_side_won'))
    ycls = 'lim' if not lim_no else 'dc'
    ncls = 'dc' if not lim_no else 'lim'
    res = 'Limits data centers won' if won else 'Data center side won'
    rcls = 'won' if won else 'lost'
    return f'''<div class="row {rcls}">
  <div class="who"><b>{name}</b><span>{meta} {cites}</span><span>{official} {tr}</span></div>
  <div class="kind"><i class="{cls}">{chip}</i>{effect}</div>
  <div class="bar" role="img" aria-label="Yes {pct(s['py'])} percent, no {pct(100-s['py'])} percent; the side that limits data centers took {pct(s['lim'])} percent"><span class="y {ycls}" style="width:{s['py']:.2f}%"></span><span class="n {ncls}" style="width:{100-s['py']:.2f}%"></span></div>
  <div class="nums"><span><small>yes</small>{'<b>' if m['yes']>m['no'] else ''}{fmt(m['yes'])}{'</b>' if m['yes']>m['no'] else ''}</span><span><small>no</small>{'<b>' if m['no']>m['yes'] else ''}{fmt(m['no'])}{'</b>' if m['no']>m['yes'] else ''}</span><span><small>limiting side</small><span class="pc">{pct(s['lim'])}%</span></span><span><small>margin</small>{'+' if s['margin']>0 else '&minus;'}{fmt(abs(s['margin']))}</span></div>
  <div class="res">{res}</div>
</div>'''

oh = D['ohio']['measures']; nat = D['national']
# counts
states = sorted(set(m['state'] for m in nat))
n_states = len(states) + 1
n_total = len(oh) + len(nat)
with_res = [m for m in oh + nat if m['yes'] is not None]
n_res = len(with_res)
n_won = sum(1 for m in with_res if m.get('restrict_won', m.get('restrict_side_won')))
lost = [m for m in with_res if not m.get('restrict_won', m.get('restrict_side_won'))]
pending = [m for m in nat if m['yes'] is None]
assert n_total == 46 and n_states == 10 and n_res == 44 and n_won == 43 and len(lost) == 1 and len(pending) == 2
oh_places = len(set(m['jurisdiction'] for m in oh))
assert oh_places == 18 and all(m['restrict_won'] for m in oh)
harwood = lost[0]
tracker_rows = [m for m in oh if oh_tracker(m)] + [m for m in nat if m['status'].startswith('tracker')]
n_tracker = len(tracker_rows)
sprigg = next(m for m in oh if m['jurisdiction'] == 'Sprigg Township')
trenton = next(m for m in oh if m['jurisdiction'] == 'Trenton (city)')
granville = next(m for m in oh if m['jurisdiction'] == 'Granville (village)')
piqua = next(m for m in oh if m['jurisdiction'] == 'Piqua (city)')
wilm = [m for m in oh if m['jurisdiction'] == 'Wilmington (city)']
monroeville = next(m for m in oh if m['jurisdiction'] == 'Monroeville (village)')
grove = next(m for m in oh if m['jurisdiction'] == 'Grove City (city)')
perry = next(m for m in oh if m['jurisdiction'] == 'Perry (village)')
bystate = {}
for m in nat: bystate.setdefault(m['state'], []).append(m)
state_order = ['OH'] + sorted(bystate, key=lambda s: (-len(bystate[s]), s))

# ---------- hero waffle (SVG) ----------
def waffle(w=372, tile=10.5, pitch=13, label_w=32, right_w=60, row_h=22, top=8, font=10):
    rows = []
    y = top
    for st in state_order:
        ms = oh if st == 'OH' else bystate[st]
        wonn = sum(1 for m in ms if m['yes'] is not None and m.get('restrict_won', m.get('restrict_side_won')))
        counted = sum(1 for m in ms if m['yes'] is not None)
        rows.append(f'<text x="0" y="{y+tile-1}" class="wl">{st}</text>')
        x = label_w
        for m in ms:
            if m['yes'] is None:
                rows.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="2" class="wp"/>')
            elif m.get('restrict_won', m.get('restrict_side_won')):
                rows.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="2" class="wg"/>')
            else:
                rows.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="2" class="wd"/>')
            x += pitch
        lab = f'{wonn} of {counted}' if counted == len(ms) else f'{wonn} of {counted}, {len(ms)-counted} pending'
        rows.append(f'<text x="{w}" y="{y+tile-1}" text-anchor="end" class="wn">{lab}</text>')
        y += row_h
    h = y + 2
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Forty-six small squares in ten rows, one row per state. Forty-three are filled in for the side that limits data centers, one in North Dakota is filled in for the data-center side, and two in Maine are outlined with no count yet.">' + ''.join(rows) + '</svg>'

# ---------- national board ----------
board = []
for st in state_order:
    ms = oh if st == 'OH' else bystate[st]
    counted = [m for m in ms if m['yes'] is not None]
    wonn = sum(1 for m in counted if m.get('restrict_won', m.get('restrict_side_won')))
    hd = f'{wonn} of {len(counted)}' + (f', {len(ms)-len(counted)} with no count yet' if len(counted) < len(ms) else '')
    board.append(f'<div class="st" id="st-{st.lower()}"><h3><span class="ab">{st}</span>{STATE_NAME[st]}<span class="ct">{len(ms)} question{"s" if len(ms)>1 else ""} &middot; limiting side {hd}</span></h3>')
    if st == 'OH':
        for m in ms:
            name = oh_name(m['jurisdiction'])
            if m['jurisdiction'] == 'Wilmington (city)':
                ordn = m['title'].split()[-1]
                name = f'City of Wilmington, Ordinance {ordn}'
                effect = f'Yes kept council&rsquo;s rezoning of {WILM[ordn]} from Rural Residential to Light Industrial for a data center project; no repealed it.'
            else:
                effect = OH_EFFECT[m['jurisdiction']]
            meta = f'{m["county"]} County' + (f' &middot; {m["issue"]}' if m['issue'] else '') + f' &middot; {html.escape(m["precincts"].split(" (")[0])}'
            keys = [OH_SRC[m['county']]] + (['redbud'] if oh_tracker(m) else [])
            board.append(row_html(name, meta, m['kind'], effect, m, keys, oh_tracker(m), m['source']))
    else:
        for m in ms:
            name, cty, key = NAT_NAME[m['jurisdiction']]
            meta = f'{cty} &middot; {html.escape(m["precincts"].split(" (")[0])}' if m['precincts'] not in ('not stated',) else cty
            tracker = m['status'].startswith('tracker')
            keys = [key]
            if tracker or m['status'].startswith('official JSON'): keys.append(nat_tracker_key(m))
            if m['jurisdiction'] == 'Harwood (Cass County)': keys.append('routefifty')
            board.append(row_html(name, meta, m['kind'], NAT_EFFECT[m['jurisdiction']], m, keys, tracker, m['source_official']))
    board.append('</div>')
BOARD = '\n'.join(board)

# ---------- Ohio dot plot ----------
def dot_row(name, meta, kind, m, keys, tracker, note=''):
    s = shares(m); chip, cls = kind_chip(kind)
    tr = ' <i class="tr">tracker only</i>' if tracker else ''
    lim_label = 'no' if limit_is_no(kind) else 'yes'
    return f'''<li class="dr">
  <div class="dn"><b>{name}</b><span>{meta} &middot; <i class="{cls}">{chip}</i>{tr} {c(*keys)}</span></div>
  <div class="dt" role="img" aria-label="{pct(s['lim'])} percent for the side that limits data centers"><span class="dot" style="left:{(s['lim']-50)/50*100:.2f}%"></span></div>
  <div class="dv"><span><small>{lim_label} (limits)</small><b>{fmt(m['no'] if limit_is_no(kind) else m['yes'])}</b></span><span><small>{'yes' if limit_is_no(kind) else 'no'}</small>{fmt(m['yes'] if limit_is_no(kind) else m['no'])}</span><span><small>share</small><b>{pct(s['lim'])}%</b></span><span><small>margin</small>+{fmt(s['margin'])}</span></div>
  {('<p class="dnote">'+note+'</p>') if note else ''}
</li>'''
oh_sorted = sorted([m for m in oh if m['jurisdiction'] != 'Wilmington (city)'], key=lambda m: -shares(m)['lim'])
dots = []
for m in oh_sorted:
    name = oh_name(m['jurisdiction']); chip, cls = kind_chip(m['kind'])
    meta = f'{m["county"]} County' + (f' &middot; {m["issue"]}' if m['issue'] else '')
    keys = [OH_SRC[m['county']]] + (['redbud'] if oh_tracker(m) else [])
    note = ''
    if m['jurisdiction'] == 'Granville (village)':
        note = f'Ballotpedia&rsquo;s election-night table printed Granville inverted and partial, 205 yes to 938 no. The Licking County sheet reads {fmt(m["yes"])} yes to {fmt(m["no"])} no. {c("licking","bp_roster")}'
    if m['jurisdiction'] == 'Sprigg Township':
        note = f'The closest margin in Ohio: {fmt(m["yes"]-m["no"])} votes of {fmt(m["yes"]+m["no"])} cast on the question. {c("adams")}'
    if m['jurisdiction'] == 'Piqua (city)':
        note = f'Ballotpedia&rsquo;s table carried a partial count, 1,912 to 908; the Miami County general report reads {fmt(m["yes"])} to {fmt(m["no"])}. {c("miami","bp_roster")}'
    if m['jurisdiction'] == 'Grove City (city)':
        note = f'Ballotpedia&rsquo;s table carried a partial count, 6,110 to 4,976. {c("bp_roster")}'
    # Wilmington block placed by share among the rest
    dots.append((shares(m)['lim'], dot_row(name, meta, m['kind'], m, keys, oh_tracker(m), note)))
# Wilmington block
wl = []
for m in wilm:
    ordn = m['title'].split()[-1]; s = shares(m)
    wl.append(f'<li class="dr sub"><div class="dn"><b>Ordinance {ordn}</b><span>{WILM[ordn]} &middot; yes kept the rezoning, no repealed it</span></div><div class="dt" role="img" aria-label="{pct(s["lim"])} percent no"><span class="dot" style="left:{(s["lim"]-50)/50*100:.2f}%"></span></div><div class="dv"><span><small>no (limits)</small><b>{fmt(m["no"])}</b></span><span><small>yes</small>{fmt(m["yes"])}</span><span><small>share</small><b>{pct(s["lim"])}%</b></span><span><small>margin</small>+{fmt(s["margin"])}</span></div></li>')
wavg = sum(shares(m)['lim'] for m in wilm) / 4
wblock = f'''<li class="dr group"><div class="dn"><b>City of Wilmington, four rezoning referenda</b><span>Clinton County &middot; <i class="ref">Rezoning referendum</i> {c("clinton")}</span></div>
<p class="dnote">Council rezoned four parcels, {", ".join(WILM[k] for k in ["O-26-04","O-26-05","O-26-06"])} and {WILM["O-26-07"]}, from Rural Residential to Light Industrial for a data center project. Petitioners put each ordinance to the voters. A yes vote kept the rezoning; a no vote repealed it. All four were repealed, each by about four to one. Ballotpedia&rsquo;s election-night table appears to have coded the no side as yes for these four. {c("clinton","bp_roster")}</p>
<ul class="dsub">{''.join(wl)}</ul></li>'''
dots.append((wavg, wblock))
dots.sort(key=lambda t: -t[0])
DOTS = '\n'.join(h for _, h in dots)

# Ohio tracker list
oh_tr_names = [oh_name(m['jurisdiction']) for m in oh if oh_tracker(m)]
oh_ver = len(oh) - len(oh_tr_names)

# ---------- Trenton ----------
T = D['ohio']['trenton']; SC = T['supreme_court']
# ---------- bills ----------
B = {b['bill']: b for b in D['ohio']['bills']}
# ---------- context ----------
CX = D['context']; SUM = D['ohio']['summit']

ts = shares(trenton); hs = shares(harwood)

# ---------- page ----------
TITLE = f'{n_total} data-center questions were on local ballots in ten states on November 3. Of the {n_res} with a count, voters took the side that limits data centers in {n_won}. Ohio had {len(oh)} of the questions, in {oh_places} places, and the limiting side won all {len(oh)}.'
LEDE = f'The one exception was the City of Harwood, North Dakota, where a charter amendment requiring review of large industrial projects failed, {fmt(harwood["yes"])} to {fmt(harwood["no"])}. Two Maine towns, Brownfield and Freedom, had posted no count by Wednesday morning. Every count on this page is unofficial until the canvasses close.'
OG_DESC = f'What a data center is and why a town votes on one; all {n_total} questions by state with the official count; Ohio&rsquo;s {len(oh)} in detail; the City of Trenton&rsquo;s Issue 17, the Supreme Court case that put it on the ballot, the annexation and the county moratorium; the four bills at the statehouse and the state&rsquo;s tax deal. Unofficial results.'

page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Data centers on the ballot</title>
<meta name="description" content="{html.escape(re.sub('&rsquo;', "'", TITLE + ' ' + OG_DESC))}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DNSC">
<meta property="og:title" content="{html.escape(TITLE)}">
<meta property="og:description" content="{html.escape(re.sub('&rsquo;', "'", LEDE))}">
<meta property="og:url" content="https://tools.dnsc.ai/civic/data-centers-on-the-ballot/">
<meta property="og:image" content="https://tools.dnsc.ai/assets/share/data-centers-on-the-ballot.jpg?v=20261104">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A drawn tally: forty-six small squares in ten rows, one row per state; forty-three filled in for the side that limits data centers, one in North Dakota for the data-center side, two in Maine outlined with no count yet.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(TITLE)}">
<meta name="twitter:description" content="{html.escape(re.sub('&rsquo;', "'", LEDE))}">
<meta name="twitter:image" content="https://tools.dnsc.ai/assets/share/data-centers-on-the-ballot.jpg?v=20261104">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=Public+Sans:ital,wght@0,400;0,500;0,700;0,800;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* Data centers on the ballot: a cool paper page built as a tally sheet. The side that limits data centers in evergreen, the data-center side in indigo; gold only as hairlines. Light only. */
:root{{
  --ground:#F3F6F8;--sheet:#ffffff;--ink:#161B21;--ink-2:#38414A;--ink-3:#5A636C;
  --rule:#C3CBD3;--rule-2:#E3E7EB;--gold:#C9A24A;
  --g:#146C4E;--g-1:#DCEFE6;--g-2:#A9D6C1;--d:#4F55B8;--d-1:#E3E4F7;--x:#B42318;--o:#4A5A68;--o-1:#E6EBEF;
  --face:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --serif:"Fraunces",Georgia,"Times New Roman",serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  color-scheme:light;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;color:var(--ink);background:var(--ground);font-family:var(--face);font-size:1.0625rem;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums lining-nums}}
::selection{{background:var(--g-1)}}
a{{color:var(--g);text-decoration-thickness:1.5px;text-underline-offset:.18em}}
a:hover{{text-decoration-thickness:3px}}
:focus-visible{{outline:3px solid var(--g);outline-offset:3px}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px 48px}}
@media (max-width:420px){{.wrap{{padding-inline:16px}}}}
.dnsc-back{{font-family:var(--mono);font-size:12.5px;letter-spacing:.04em;padding:10px 20px;border-bottom:1px solid rgba(127,127,127,.25);background:rgba(127,127,127,.06)}}
.dnsc-back a{{color:inherit;opacity:.8;text-decoration:none}}
.dnsc-back span{{opacity:.35;margin:0 10px}}
.top{{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:10px 24px;padding:22px 0 12px;border-bottom:2px solid var(--ink)}}
.brand{{display:flex;align-items:center;gap:12px}}
.brand svg{{width:38px;height:38px;flex:none}}
.brand .nm{{font-weight:800;font-size:1rem;letter-spacing:.12em;text-transform:uppercase;line-height:1.3}}
.brand .nm span{{display:block;font-weight:500;font-size:.9rem;letter-spacing:0;text-transform:none;color:var(--ink-2)}}
.ref{{font-family:var(--mono);font-size:.8rem;letter-spacing:.04em;color:var(--ink-3);text-align:right;line-height:1.5}}
.ref span{{display:block}}
@media (max-width:700px){{.ref{{text-align:left}}}}
.kick,.k{{font-family:var(--serif);font-style:italic;font-weight:500;font-size:calc(.8125rem*.95 + 2px);letter-spacing:0;color:var(--ink-3);margin:0 0 8px}}
.kick::before,.k::before{{content:"";display:inline-block;width:18px;height:1.5px;background:var(--gold);vertical-align:.3em;margin-right:8px}}
.c{{font-family:var(--mono);font-size:.74em;letter-spacing:.02em;white-space:nowrap;vertical-align:.12em}}
.c a{{color:var(--ink-3);text-decoration:none;padding:0 1px}}
.c a:hover{{color:var(--g);text-decoration:underline}}
p{{max-width:65ch;text-wrap:pretty}}

/* hero: the headline on the left, the tally on the right */
.hero{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:0 48px;align-items:center;padding:40px 0 10px}}
.hero>.ha{{grid-column:1;grid-row:1;align-self:end}}.hero>.hb{{grid-column:1;grid-row:2;align-self:start}}.hero>.tally{{grid-column:2;grid-row:1/3}}
@media (max-width:860px){{.hero{{grid-template-columns:minmax(0,1fr);gap:22px;padding-top:26px}}.hero>.ha,.hero>.hb,.hero>.tally{{grid-column:1;grid-row:auto}}}}
.hero h1{{font-family:var(--serif);font-weight:600;font-size:clamp(1.6rem,3.5vw,2.5rem);line-height:1.12;letter-spacing:-.015em;margin:0 0 18px;text-wrap:balance;max-width:none}}
.hero h1 .g{{color:var(--g)}}.hero h1 .d{{color:var(--d)}}
.lede{{font-weight:400;font-size:clamp(1.04rem,1.7vw,1.18rem);line-height:1.5;color:var(--ink-2);margin:0;max-width:58ch}}
.cares{{margin:16px 0 0;max-width:56ch;font-size:1.02rem;line-height:1.5;color:var(--ink);padding-left:12px;border-left:3px solid var(--gold)}}
.stamp{{margin:16px 0 0;font-family:var(--mono);font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);max-width:none}}
.tally{{margin:0;background:var(--sheet);border:1.5px solid var(--ink);border-radius:20px;padding:16px 16px 14px;max-width:380px;justify-self:center;width:100%}}
.tally svg{{display:block;width:100%;height:auto}}
.tally .wl{{font:500 10px var(--mono);fill:var(--ink-3);letter-spacing:.04em}}
.tally .wn{{font:400 9px var(--mono);fill:var(--ink-3)}}
.tally .wg{{fill:var(--g);stroke:var(--g);stroke-width:1}}
.tally .wd{{fill:var(--d);stroke:var(--d);stroke-width:1}}
.tally .wp{{fill:none;stroke:var(--ink-3);stroke-width:1;stroke-dasharray:2 2}}
.tally .big{{display:block;font:800 clamp(1.7rem,3vw,2.3rem)/1 var(--face);letter-spacing:-.03em;color:var(--ink);margin:12px 0 4px}}
.tally .big b{{color:var(--g)}}
.tally p{{margin:0;font-size:.9rem;line-height:1.42;color:var(--ink-2)}}
.tally p+p{{margin-top:8px}}
.tally .lg{{display:flex;flex-wrap:wrap;gap:6px 14px;margin:10px 0 0;font-size:.78rem;color:var(--ink-3)}}
.tally .lg i{{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin-right:5px}}
.tally .lg .a i{{background:var(--g)}}.tally .lg .b i{{background:var(--d)}}.tally .lg .p i{{border:1px dashed var(--ink-3)}}
@media (max-width:860px){{.tally{{max-width:none;justify-self:stretch}}}}

/* jump bar */
.jump{{position:sticky;top:0;z-index:5;margin:26px -20px 0;padding:8px 20px;background:rgba(243,246,248,.92);backdrop-filter:blur(6px);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}}
.jump::-webkit-scrollbar{{display:none}}
.jump ul{{display:flex;gap:6px;margin:0;padding:0;list-style:none;white-space:nowrap}}
.jump a{{display:inline-block;font-family:var(--mono);font-size:.76rem;letter-spacing:.02em;color:var(--ink-2);text-decoration:none;padding:7px 10px;border-radius:999px;border:1px solid transparent;min-height:34px}}
.jump a:hover{{border-color:var(--rule);background:var(--sheet);color:var(--ink)}}
@media (max-width:420px){{.jump{{margin-inline:-16px;padding-inline:16px}}}}

/* chapter heads */
.ch{{margin:72px 0 22px;max-width:64ch;scroll-margin-top:60px}}
.ch h2{{font-family:var(--face);font-weight:800;font-size:clamp(1.4rem,3vw,2.05rem);line-height:1.12;letter-spacing:-.025em;margin:0;text-wrap:balance}}
.ch .dek{{margin:10px 0 0;color:var(--ink-2);max-width:64ch}}
@media (max-width:520px){{.ch{{margin-top:56px}}}}
h3{{font:800 1.08rem/1.25 var(--face);margin:26px 0 10px}}
.prose p{{margin:0 0 14px;color:var(--ink-2)}}
.prose p b{{color:var(--ink)}}

/* what a data center is: a drawn building and three figures */
.dc{{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:18px 32px;align-items:start;margin:18px 0 0;max-width:900px}}
@media (max-width:760px){{.dc{{grid-template-columns:minmax(0,1fr)}}}}
.dc figure{{margin:0;background:var(--sheet);border:1.5px solid var(--ink);border-radius:20px;padding:14px}}
.dc figure svg{{display:block;width:100%;height:auto}}
.dc figcaption{{margin-top:8px;font-size:.82rem;line-height:1.4;color:var(--ink-3)}}
.figs{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0}}
.figs div{{background:var(--sheet);border:1.5px solid var(--ink);border-radius:14px;padding:12px 12px 10px;min-width:0}}
.figs .n{{display:block;font:800 clamp(1.3rem,2.4vw,1.75rem)/1.05 var(--face);letter-spacing:-.03em;color:var(--g);overflow-wrap:anywhere}}
.figs span.l{{display:block;margin-top:6px;font-size:.84rem;line-height:1.35;color:var(--ink-2)}}
@media (max-width:560px){{.figs{{grid-template-columns:minmax(0,1fr)}}}}

/* the kinds of question: a glossary ledger */
.kinds{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 18px;margin:18px 0 0;padding:0;list-style:none;max-width:900px}}
@media (max-width:700px){{.kinds{{grid-template-columns:minmax(0,1fr)}}}}
.kinds li{{background:var(--sheet);border:1.5px solid var(--ink);border-radius:16px;padding:12px 14px 10px;min-width:0}}
.kinds li i{{font-style:normal;font-weight:800;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;display:inline-block;padding:1px 6px;border-radius:5px;margin:0 0 6px}}
.kinds li p{{margin:0;font-size:.94rem;line-height:1.45;color:var(--ink-2)}}
.kinds li p b{{color:var(--ink)}}
.kinds li .ex{{display:block;margin-top:6px;font-family:var(--mono);font-size:.7rem;letter-spacing:.02em;color:var(--ink-3);line-height:1.45}}
i.ban,i.cap{{color:var(--g);background:var(--g-1)}}
i.mor{{color:#0F5F6B;background:#D9EEF1}}
i.vote,i.rev{{color:#6A4A00;background:#F6ECCF}}
i.ref,i.zon{{color:#3F5A84;background:#E1E9F6}}
i.adv{{color:var(--ink-2);background:var(--o-1)}}
i.tax,i.allow{{color:var(--d);background:var(--d-1)}}
i.tr{{font-style:normal;font-family:var(--mono);font-weight:500;font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--x);border:1px solid var(--x);border-radius:4px;padding:0 5px;margin-left:4px;vertical-align:1px;white-space:nowrap}}

/* the national board: a tally sheet by state */
.board{{margin:22px 0 0;background:var(--sheet);border:1.5px solid var(--ink);border-radius:20px;padding:6px 16px 10px;position:relative}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 18px;padding:10px 0 8px;font-size:.84rem;color:var(--ink-2);border-bottom:1px solid var(--rule)}}
.legend i{{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:-2px;margin-right:6px}}
.legend .lg i{{background:var(--g)}}.legend .ld i{{background:var(--d)}}
.legend .l5 i{{width:2px;height:16px;background:var(--ink);border-radius:0;vertical-align:-4px}}
.st h3{{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:18px 0 2px;padding:10px 0 8px;border-bottom:2px solid var(--ink);font-size:1.05rem;position:sticky;top:50px;background:var(--sheet);z-index:2}}
.st h3 .ab{{font-family:var(--serif);font-weight:600;font-size:1.5rem;letter-spacing:.02em;color:var(--g);min-width:2.2ch}}
.st h3 .ct{{font-family:var(--mono);font-weight:400;font-size:.72rem;letter-spacing:.02em;color:var(--ink-3);margin-left:auto}}
@media (max-width:560px){{.st h3 .ct{{margin-left:0;flex-basis:100%}}}}
.row{{display:grid;grid-template-columns:minmax(0,190px) minmax(0,1fr) minmax(0,150px) minmax(0,256px) 118px;gap:4px 16px;align-items:center;padding:12px 0;border-bottom:1px solid var(--rule-2)}}
.st .row:last-child{{border-bottom:0}}
.row .who b{{display:block;font-size:.98rem;line-height:1.25;color:var(--ink)}}
.row .who span{{display:block;font-family:var(--mono);font-size:.7rem;letter-spacing:.02em;color:var(--ink-3);margin-top:3px;line-height:1.5}}
.row .who .off{{color:var(--ink-3);text-decoration-thickness:1px}}
.row .kind{{font-size:.86rem;line-height:1.38;color:var(--ink-2)}}
.row .kind i{{font-style:normal;font-weight:800;font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;display:inline-block;padding:1px 6px;border-radius:5px;margin-right:6px}}
.row .bar{{position:relative;display:flex;height:20px;background:var(--rule-2);border-radius:5px;overflow:hidden;min-width:0}}
.row .bar span{{display:block;height:100%;flex:none}}
.row .bar .lim{{background:var(--g)}}.row .bar .dc{{background:var(--d)}}
.row .bar::after{{content:"";position:absolute;left:50%;top:-2px;bottom:-2px;width:2px;background:var(--ink)}}
.row .bar.none{{background:repeating-linear-gradient(135deg,var(--rule-2) 0 6px,var(--sheet) 6px 12px)}}
.row .bar.none::after{{display:none}}
.row .nums{{display:grid;grid-template-columns:repeat(4,minmax(0,auto));gap:0 10px;font-family:var(--mono);font-size:.78rem;color:var(--ink-2);white-space:nowrap}}
.row .nums b{{font-weight:500;color:var(--ink)}}
.row .nums .pc{{font-weight:500;color:var(--ink)}}
.row .nums small{{display:block;font-size:.62rem;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-3)}}
.row .res{{font-family:var(--mono);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;font-weight:500;text-align:right;line-height:1.35}}
.row.won .res{{color:var(--g)}}.row.lost .res{{color:var(--d)}}.row.pend .res{{color:var(--ink-3)}}
.row.lost{{background:var(--d-1);margin:0 -16px;padding-inline:16px;border-radius:0}}
@media (max-width:1000px){{.row{{grid-template-columns:minmax(0,1fr) minmax(0,1fr) 118px;grid-template-areas:"who kind res" "bar bar bar" "nums nums nums"}}.row .who{{grid-area:who}}.row .kind{{grid-area:kind}}.row .res{{grid-area:res}}.row .bar{{grid-area:bar;margin-top:6px}}.row .nums{{grid-area:nums;margin-top:4px}}}}
@media (max-width:600px){{.row{{grid-template-columns:minmax(0,1fr) 104px;grid-template-areas:"who res" "kind kind" "bar bar" "nums nums"}}.row .nums{{grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 10px}}.board{{padding-inline:12px}}.row.lost{{margin:0 -12px;padding-inline:12px}}.row .res{{font-size:.64rem}}}}
.tnote{{margin:12px 0 0;font-size:.9rem;line-height:1.45;color:var(--ink-2);max-width:72ch}}

/* Ohio's 21: a dot plot, one line per place */
.dots{{margin:22px 0 0;padding:0;list-style:none;background:var(--sheet);border:1.5px solid var(--ink);border-radius:20px;padding:6px 16px 10px}}
.axis{{display:grid;grid-template-columns:minmax(0,260px) minmax(0,1fr) minmax(0,300px);gap:4px 16px;padding:10px 0 8px;border-bottom:1px solid var(--rule);font-family:var(--mono);font-size:.7rem;letter-spacing:.03em;color:var(--ink-3)}}
.axis .ax{{display:flex;justify-content:space-between}}
.dr{{display:grid;grid-template-columns:minmax(0,260px) minmax(0,1fr) minmax(0,300px);gap:4px 16px;align-items:center;padding:11px 0;border-bottom:1px solid var(--rule-2)}}
.dots>.dr:last-child{{border-bottom:0}}
.dr .dn b{{display:block;font-size:.96rem;line-height:1.25;color:var(--ink)}}
.dr .dn span{{display:block;font-family:var(--mono);font-size:.7rem;letter-spacing:.02em;color:var(--ink-3);margin-top:3px;line-height:1.5}}
.dr .dn span i{{font-style:normal;font-family:var(--face);font-weight:800;font-size:.64rem;letter-spacing:.06em;text-transform:uppercase;display:inline-block;padding:0 5px;border-radius:4px}}
.dr .dt{{position:relative;height:22px;min-width:0;background:linear-gradient(to right,var(--rule-2),var(--g-2));border-radius:4px}}
.dr .dt::before{{content:"";position:absolute;left:0;top:-3px;bottom:-3px;width:2px;background:var(--ink)}}
.dr .dt .dot{{position:absolute;top:50%;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:var(--g);border:2.5px solid var(--sheet);box-shadow:0 0 0 1.5px var(--g)}}
.dr .dv{{display:grid;grid-template-columns:repeat(4,minmax(0,auto));gap:0 10px;font-family:var(--mono);font-size:.78rem;color:var(--ink-2);white-space:nowrap}}
.dr .dv b{{font-weight:500;color:var(--ink)}}
.dr .dv small{{display:block;font-size:.62rem;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-3)}}
.dr .dnote{{grid-column:1/-1;margin:4px 0 0;font-size:.88rem;line-height:1.45;color:var(--ink-2);max-width:80ch}}
.dr.group{{display:block}}
.dr.group>.dn{{margin-bottom:4px}}
.dsub{{list-style:none;margin:8px 0 0;padding:0 0 0 14px;border-left:2px solid var(--rule)}}
.dsub .dr{{padding:8px 0}}
.dsub .dr:last-child{{border-bottom:0}}
.dsub .dr .dn b{{font-size:.9rem;font-weight:700}}
@media (max-width:980px){{.axis{{display:none}}.dr{{grid-template-columns:minmax(0,1fr);gap:6px}}.dr .dv{{grid-template-columns:repeat(4,minmax(0,auto))}}}}
@media (max-width:520px){{.dr .dv{{grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 10px}}.dots{{padding-inline:12px}}}}
.maxis{{display:none;font-family:var(--mono);font-size:.7rem;letter-spacing:.03em;color:var(--ink-3);padding:10px 0 8px;border-bottom:1px solid var(--rule)}}
@media (max-width:980px){{.maxis{{display:block}}}}

/* Trenton: a big count and a docket */
.tr2{{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:22px 36px;align-items:start;margin:18px 0 0}}
@media (max-width:860px){{.tr2{{grid-template-columns:minmax(0,1fr)}}}}
.count{{background:var(--sheet);border:1.5px solid var(--ink);border-radius:20px;padding:16px 18px 14px;position:sticky;top:60px}}
@media (max-width:860px){{.count{{position:static}}}}
.count .n{{display:block;font:800 clamp(2.2rem,5vw,3.4rem)/1 var(--face);letter-spacing:-.04em;color:var(--g)}}
.count .n small{{display:block;font:800 clamp(1.1rem,2vw,1.4rem)/1.1 var(--face);letter-spacing:-.02em;color:var(--ink-3);margin-top:4px}}
.count .n small b{{color:var(--d)}}
.count p{{margin:10px 0 0;font-size:.92rem;line-height:1.45;color:var(--ink-2)}}
.count .line{{margin-top:12px;padding-top:12px;border-top:1px solid var(--rule)}}
.count .line b{{display:block;font:800 1.5rem/1.05 var(--face);letter-spacing:-.03em;color:var(--ink)}}
.docket{{list-style:none;margin:0;padding:0;position:relative}}
.docket::before{{content:"";position:absolute;left:5px;top:6px;bottom:6px;width:2px;background:var(--rule)}}
.docket li{{position:relative;padding:0 0 18px 26px}}
.docket li::before{{content:"";position:absolute;left:0;top:7px;width:12px;height:12px;border-radius:50%;background:var(--sheet);border:2.5px solid var(--g)}}
.docket li.open::before{{border-color:var(--ink-3);border-style:dashed}}
.docket time,.docket .when{{display:block;font-family:var(--mono);font-size:.76rem;letter-spacing:.03em;color:var(--g);margin-bottom:2px}}
.docket li.open .when{{color:var(--ink-3)}}
.docket p{{margin:0 0 6px;color:var(--ink-2);max-width:62ch}}
.docket p b{{color:var(--ink)}}
.docket p:last-child{{margin:0}}

/* statehouse: four bill cards and the deal */
.bills{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0 0}}
@media (max-width:960px){{.bills{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:520px){{.bills{{grid-template-columns:minmax(0,1fr)}}}}
.bill{{background:var(--sheet);border:1.5px solid var(--ink);border-radius:16px;padding:12px 14px 10px;min-width:0;display:flex;flex-direction:column}}
.bill .no{{font-family:var(--serif);font-weight:600;font-size:1.35rem;letter-spacing:-.01em;color:var(--ink)}}
.bill .ti{{margin:2px 0 8px;font-weight:700;font-size:.92rem;line-height:1.3;color:var(--ink)}}
.bill p{{margin:0 0 8px;font-size:.88rem;line-height:1.45;color:var(--ink-2)}}
.bill .stt{{margin-top:auto;font-family:var(--mono);font-size:.7rem;letter-spacing:.03em;color:var(--ink-3);line-height:1.5;padding-top:8px;border-top:1px solid var(--rule-2)}}
.bill .stt b{{display:block;font-weight:500;color:var(--ink)}}
.deal{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:22px 0 0}}
@media (max-width:860px){{.deal{{grid-template-columns:minmax(0,1fr)}}}}
.deal div{{background:var(--sheet);border:1.5px solid var(--ink);border-radius:16px;padding:14px 16px 12px;min-width:0}}
.deal h3{{margin:0 0 8px;font-size:1rem}}
.deal p{{margin:0 0 8px;font-size:.92rem;line-height:1.45;color:var(--ink-2)}}
.deal p:last-child{{margin:0}}
.deal p b{{color:var(--ink)}}

/* next: a short rail */
.entries{{display:grid;gap:14px;margin:0;padding:0;list-style:none;max-width:72ch}}
.entries li{{display:grid;grid-template-columns:13ch 1fr;gap:14px;align-items:start;min-width:0;padding:14px 0 0;border-top:1px solid var(--rule)}}
.entries time,.entries .when{{font-family:var(--mono);font-size:.78rem;color:var(--g);padding-top:4px;white-space:nowrap}}
.entries .what{{min-width:0}}
.entries .what p{{margin:0 0 8px;color:var(--ink-2)}}
.entries .what p:last-child{{margin-bottom:0}}
.entries .what p b{{color:var(--ink)}}
@media (max-width:520px){{.entries li{{grid-template-columns:1fr;gap:4px}}.entries time,.entries .when{{padding-top:0}}}}
.note{{background:var(--sheet);border:1.5px solid var(--ink);border-radius:16px;padding:14px 18px;margin:22px 0 0;max-width:72ch}}
.note p{{margin:0 0 8px;color:var(--ink-2)}}
.note p:last-child{{margin:0}}
.note b{{color:var(--ink)}}

/* sources */
.srcs{{margin-top:72px;max-width:860px;scroll-margin-top:60px}}
ol.src{{margin:0;padding-left:1.8em;font-size:.92rem;line-height:1.5;color:var(--ink-2)}}
ol.src li{{overflow-wrap:anywhere;margin-bottom:7px;scroll-margin-top:60px}}
ol.src li:target{{background:var(--g-1);outline:2px solid var(--g-1)}}
.tm{{font-size:.85rem;color:var(--ink-3);margin:12px 0 0}}
footer{{margin-top:44px;padding-top:18px;border-top:2px solid var(--ink);max-width:860px}}
footer p{{margin:0;font-size:1rem;line-height:1.6;color:var(--ink-2)}}
footer p.sm{{margin-top:8px;font-size:.92rem;color:var(--ink-3)}}

/* motion: only when allowed; without it every element is static and visible */
.mo .rise{{opacity:0;transform:translateY(12px);transition:opacity .5s ease,transform .7s cubic-bezier(.16,1,.3,1)}}
.mo .rise.on{{opacity:1;transform:none}}
.mo .tally rect{{opacity:0;transition:opacity .25s ease}}
.mo .tally.on rect{{opacity:1}}
.mo .row .bar span{{transition:width .9s cubic-bezier(.16,1,.3,1)}}
.mo .st:not(.on) .row .bar span{{width:0!important}}
.mo .dr .dot{{transition:left .9s cubic-bezier(.16,1,.3,1)}}
.mo .dots:not(.on) .dr .dot{{left:0!important}}
@media (prefers-reduced-motion:reduce){{.mo .rise{{opacity:1!important;transform:none!important;transition:none!important}}.mo .tally rect{{opacity:1!important}}}}
@media print{{.mo *{{opacity:1!important;transform:none!important}}}}
</style>
<link rel="icon" href="/assets/favicon.png">
</head>
<body>
<div class="dnsc-back"><a href="https://tools.dnsc.ai/">&larr; The Well</a><span>&middot;</span><a href="https://dnsc.ai">dnsc.ai</a></div>
<div class="wrap">

<header class="top">
  <div class="brand">
    <svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="16" fill="none" stroke="#161B21" stroke-width="2.4"/><g fill="#161B21"><circle cx="20" cy="7" r="2.6"/><circle cx="32.4" cy="16" r="2.6"/><circle cx="27.6" cy="30.5" r="2.6"/><circle cx="12.4" cy="30.5" r="2.6"/><circle cx="7.6" cy="16" r="2.6"/></g></svg>
    <div class="nm">DNSC<span>From the public record</span></div>
  </div>
  <div class="ref"><span>Data centers on the ballot &middot; November 4, 2026</span><span>Understanding the week, from the record</span></div>
</header>

<!-- 1 · the headline and the tally -->
<section class="hero">
  <div class="ha">
    <p class="kick">Ten states &middot; {n_total} local ballot questions &middot; November 3, 2026</p>
    <h1>{n_total} data-center questions were on local ballots in ten states on November 3. Of the {n_res} with a count, <span class="g">voters took the side that limits data centers in {n_won}.</span> Ohio had {len(oh)} of the questions, in {oh_places} places, and the limiting side won all {len(oh)}.</h1>
    <p class="lede">The one exception was the City of Harwood, North Dakota, where a charter amendment requiring review of large industrial projects failed, {fmt(harwood["yes"])} to {fmt(harwood["no"])}. {c("nd_sos","routefifty")} Two Maine towns, Brownfield and Freedom, had posted no count by Wednesday morning. {c("redbud")} The roster is Ballotpedia&rsquo;s 41 questions plus five Maine and Kansas towns added by a second tracker; the counts are the county and town sheets where this desk could reach them, and a tracker&rsquo;s read where it could not. {c("bp_roster","bp_news","redbud","railway")} Every count on this page is unofficial until the canvasses close.</p>
  </div>
  <figure class="tally rise">
    {waffle()}
    <span class="big"><b>{n_won}</b> of {n_res}</span>
    <p>Each square is one question. Filled green: the side that limits data centers won. Filled indigo: the data-center side won, once, in Harwood. Dashed: no count yet.</p>
    <p class="lg"><span class="a"><i></i>limits won</span><span class="b"><i></i>data-center side won</span><span class="p"><i></i>no count yet</span></p>
  </figure>
  <div class="hb">
    <p class="cares">A data center is a building full of computers that stores and serves the internet&rsquo;s websites, apps and AI models, and it draws electricity and cooling water around the clock. The questions below asked a town or city whether to forbid one, cap its size, pause permits, require a public vote, keep or repeal a rezoning, or set terms on a tax break.</p>
    <p class="stamp"><time datetime="2026-11-04">Posted November 4, 2026</time> &middot; Unofficial results; Ohio&rsquo;s canvass closes November 24</p>
  </div>
</section>

<nav class="jump" aria-label="Sections of this story">
  <ul>
    <li><a href="#what">What a data center is</a></li>
    <li><a href="#board">The board, {n_total} questions</a></li>
    <li><a href="#ohio">Ohio&rsquo;s {len(oh)}</a></li>
    <li><a href="#trenton">Trenton</a></li>
    <li><a href="#statehouse">The statehouse</a></li>
    <li><a href="#next">What happens next</a></li>
    <li><a href="#srcs">Sources</a></li>
  </ul>
</nav>

<!-- 2 · who cares: what a data center is, why a town votes on one, what each question does -->
<section class="ch prose" id="what">
  <p class="k">What the words mean</p>
  <h2>Data centers used 4.4 percent of U.S. electricity in 2023. A town votes on one because zoning, a city charter and a tax break are all local decisions.</h2>
  <p class="dek">The building, the power it draws, and the eight kinds of question that were on the ballot.</p>
</section>
<div class="dc">
  <figure class="rise">
    <svg viewBox="0 0 300 190" role="img" aria-label="A drawn data center: a long single-story building with rows of server racks inside, a substation feeding it power from the left, and cooling water piped in from below.">
      <defs><pattern id="rk" width="10" height="8" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="8" height="6" rx="1" fill="none" stroke="#161B21" stroke-width=".9"/></pattern></defs>
      <text x="8" y="16" style="font:500 10px IBM Plex Mono,monospace;fill:#5A636C;letter-spacing:.04em">one building, drawn to show the parts</text>
      <!-- substation -->
      <g stroke="#4F55B8" stroke-width="1.6" fill="none"><rect x="12" y="78" width="40" height="40" rx="3"/><path d="M20 118v10M32 118v10M44 118v10M14 78l8-14h16l8 14M32 64V52"/><path d="M52 98h20" stroke-dasharray="3 3"/></g>
      <text x="32" y="140" text-anchor="middle" style="font:500 8.5px IBM Plex Mono,monospace;fill:#4F55B8">power in</text>
      <!-- building -->
      <g><rect x="72" y="58" width="216" height="80" rx="3" fill="#fff" stroke="#161B21" stroke-width="1.8"/><rect x="80" y="70" width="200" height="56" fill="url(#rk)"/><path d="M72 58l10-12h206l-10 12" fill="#F3F6F8" stroke="#161B21" stroke-width="1.8" stroke-linejoin="round"/></g>
      <text x="180" y="152" text-anchor="middle" style="font:500 8.5px IBM Plex Mono,monospace;fill:#38414A">rows of servers: storage, websites, apps, AI models</text>
      <!-- cooling water -->
      <g stroke="#146C4E" stroke-width="1.6" fill="none"><path d="M120 138v22h120v-22" /><path d="M130 176c6-6 12-6 18 0s12 6 18 0 12-6 18 0 12 6 18 0 12-6 18 0" stroke-linecap="round"/></g>
      <text x="180" y="170" text-anchor="middle" style="font:500 8.5px IBM Plex Mono,monospace;fill:#146C4E">cooling water</text>
      <!-- heat out -->
      <g stroke="#B42318" stroke-width="1.4" fill="none" stroke-linecap="round"><path d="M100 40c3-6-3-10 0-16M120 40c3-6-3-10 0-16M140 40c3-6-3-10 0-16"/></g>
      <text x="120" y="20" text-anchor="middle" style="font:500 8.5px IBM Plex Mono,monospace;fill:#B42318" dy="0">heat out</text>
    </svg>
    <figcaption>The parts a town&rsquo;s question reaches: how big the building may be, how much power it may draw, how much water, and whether it may be built at all.</figcaption>
  </figure>
  <div>
    <p>Every search, message, video, cloud file and AI answer runs on a computer somewhere, and that somewhere is a data center: a warehouse-sized building of server racks that runs day and night. The Department of Energy&rsquo;s December 2024 report, prepared by Lawrence Berkeley National Laboratory, put U.S. data centers at about 176 terawatt-hours of electricity in 2023, 4.4 percent of everything the country used, up from 58 terawatt-hours in 2014, and projected 6.7 to 12 percent of U.S. electricity by 2028. {c("doe")} The Energy Information Administration said in January 2026 that the country was in its strongest four-year run of electricity demand growth since 2000, fueled by data centers; in May it put servers at about 7 percent of commercial-sector electricity in 2025; and its September outlook has U.S. electricity sales at 4,135 billion kilowatt-hours in 2026 and 4,211 billion in 2027, driven by data centers and manufacturing. {c("eia_jan","eia_tie","eia_steo")}</p>
    <div class="figs rise">
      <div><span class="n">176 TWh</span><span class="l">U.S. data centers&rsquo; electricity in 2023, 4.4 percent of the national total {c("doe")}</span></div>
      <div><span class="n">6.7 to 12%</span><span class="l">the report&rsquo;s projected share of U.S. electricity by 2028, 325 to 580 TWh {c("doe")}</span></div>
      <div><span class="n">4,135</span><span class="l">billion kilowatt-hours of U.S. electricity sales forecast for 2026, 4,211 in 2027 {c("eia_steo")}</span></div>
    </div>
    <p style="margin-top:16px">A town votes on one because the decisions that let a data center be built are local. Where a building may go is zoning. What a city may do at all is written in its charter, which voters can amend by petition; in Ohio, the state constitution sets the signatures needed at 10 percent of the votes cast at the last general municipal election, the rule the Supreme Court of Ohio applied in the Trenton case below. {c("sc_pdf")} A council&rsquo;s rezoning ordinance can be sent to the voters by petition. And a property tax abatement or a sales-tax exemption is an agreement a council or a state authority signs, which voters can condition. A megawatt is a measure of power demand; five of Ohio&rsquo;s amendments draw their line at 25 megawatts, the same line the state&rsquo;s utility regulator used in 2025 for its data-center tariff. {c("butler","defiance","ashtabula","lucas","delaware","puco")}</p>
  </div>
</div>
<ul class="kinds">
  <li><i class="ban">Charter ban</i><p>Adds a line to the city&rsquo;s charter forbidding data centers. The charter is the city&rsquo;s own constitution; a future council cannot repeal the line without another public vote.</p><span class="ex">Urbana, Piqua, Pataskala, Granville, Upper Sandusky, Edgewater, Alhambra</span></li>
  <li><i class="cap">Size cap in megawatts</i><p>Forbids only data centers above a power line, 25 megawatts in the five Ohio amendments; smaller server rooms stay legal. A yes vote limits.</p><span class="ex">Trenton, Defiance, Conneaut, Oregon, Sunbury; Ottawa, Kansas; Emporia&rsquo;s 10 MW</span></li>
  <li><i class="mor">Moratorium</i><p>A pause on data-center permits and applications for a set time, 180 days in most of the Maine towns, while the town writes rules.</p><span class="ex">Peru, Wells, Wiscasset, Eliot, Sabattus, Brownfield, Freedom (Maine); Bloomington&rsquo;s advisory asks for one</span></li>
  <li><i class="vote">Voter-approval requirement</i><p>Large projects go to a public vote before the city may approve them. The building is still allowed; the decision moves from council to the ballot.</p><span class="ex">Grove City (50 acres, 20 MW or 500,000 gallons a day); Janesville ($450 million on the former GM site)</span></li>
  <li><i class="ref">Rezoning referendum</i><p>Council already rezoned the land; petitioners put that ordinance to the voters. Yes keeps the rezoning, no repeals it, so here a no vote is the side that limits.</p><span class="ex">Wilmington&rsquo;s four ordinances; Ashville&rsquo;s referendum on a negotiating term sheet works the same way</span></li>
  <li><i class="adv">Advisory question</i><p>Nonbinding. It tells officials what residents want and changes no law. Some asked &ldquo;allow?&rdquo; and some asked &ldquo;limit?&rdquo;, so the limiting side is no on the first and yes on the second.</p><span class="ex">Five Illinois townships and Morgan County; Monroeville; Downe Township</span></li>
  <li><i class="tax">Tax-abatement terms, or allow</i><p>Sets conditions a developer must meet to get an incentive, or asks outright whether to add data centers as an allowed use. On an allow question, no is the side that limits.</p><span class="ex">Perry&rsquo;s financial guarantees; Boulder City&rsquo;s land-use question</span></li>
  <li><i class="zon">Adopt township zoning</i><p>Two Adams County townships had no zoning at all. Adopting it gives the trustees a say over where a data center may go on farmland. A review requirement, Harwood&rsquo;s question, adds an independent review and a hearing before approval.</p><span class="ex">Monroe Township, Sprigg Township; Harwood, North Dakota</span></li>
</ul>

<!-- 3 · the national board -->
<section class="ch" id="board">
  <p class="k">The board</p>
  <h2>{n_won} of {n_res}. The limiting side took between {pct(min(shares(m)['lim'] for m in with_res if m.get('restrict_won', m.get('restrict_side_won'))))} and {pct(max(shares(m)['lim'] for m in with_res))} percent everywhere it won. In Harwood it took {pct(hs['lim'])}.</h2>
  <p class="dek">All {n_total} questions, grouped by state, Ohio first. Each bar splits yes from no; the green part is the side that limits data centers, the indigo part the data-center side, so an &ldquo;allow&rdquo; question that failed reads green. Rows marked <i class="tr">tracker only</i> carry a tracker&rsquo;s read of the count because the county or town sheet could not be reached by this desk; {n_tracker} of the {n_res} counted rows are marked. {c("bp_roster","redbud","railway")}</p>
</section>
<div class="board">
  <div class="legend"><span class="lg"><i></i>Side that limits data centers</span><span class="ld"><i></i>Data-center side</span><span class="l5"><i></i>50 percent</span></div>
{BOARD}
</div>
<p class="tnote">&ldquo;Limiting side&rdquo; is the votes cast for the side that limits data centers, divided by yes plus no. On a ban, cap, moratorium, voter-approval, review or &ldquo;limit?&rdquo; advisory question that side is yes; on an &ldquo;allow?&rdquo; advisory, an allow question, a rezoning referendum or Ashville&rsquo;s agreement referendum it is no. Margin is the limiting side&rsquo;s lead. Ballotpedia&rsquo;s election-night table appears to have coded the no side as yes for Wilmington&rsquo;s four referenda, and it ran Granville inverted; the county sheets are used here. {c("clinton","licking","bp_roster")} Counts in California and Nevada continue as mail ballots arrive. {c("lavote","clark_nv")} Emporia&rsquo;s and Ottawa&rsquo;s bans are before Kansas courts on whether the subject can be set by petition. {c("lyon_ks","franklin_ks","redbud")} The six Illinois and New Jersey rows read from county feeds carry the tracker&rsquo;s reading of those same feeds. {c("bloomington","madison_il","will_il","cumberland_nj","bp_roster")}</p>

<!-- 4 · Ohio's 21 -->
<section class="ch" id="ohio">
  <p class="k">Ohio&rsquo;s {len(oh)}</p>
  <h2>{len(oh)} questions in {oh_places} places, from Conneaut on Lake Erie to Sprigg Township on the Ohio River. The limiting side won all {len(oh)}, by {pct(shares(sprigg)['lim'])} percent in Sprigg Township and {pct(shares(monroeville)['lim'])} in the Village of Monroeville.</h2>
  <p class="dek">One dot per place, set where the limiting side landed between 50 and 100 percent. {oh_ver} of the {len(oh)} counts were read from the county boards&rsquo; own sheets; {len(oh_tr_names)} come from a tracker and are marked. {c("fortune","nbc4","ideastream","redbud")}</p>
</section>
<ul class="dots rise">
  <li class="axis" aria-hidden="true"><span>place &middot; county &middot; kind</span><span class="ax"><span>50%</span><span>75%</span><span>100%</span></span><span>count</span></li>
  <li class="maxis" aria-hidden="true">dot: the limiting side&rsquo;s share, 50% at the left edge, 100% at the right</li>
{DOTS}
</ul>
<p class="tnote">The Village of Monroeville&rsquo;s question was advisory and asked whether to allow data centers; {fmt(monroeville["no"])} voted no and {fmt(monroeville["yes"])} yes. {c("huron")} The City of Piqua also recalled three city commissioners the same night; the recall counts are in a separate county report this desk did not obtain. {c("miami")} Tracker-only in Ohio: {", ".join(oh_tr_names[:-1])} and {oh_tr_names[-1]}; the Pickaway County file at the board&rsquo;s link was still the pre-count zero report when fetched. {c("pickaway","redbud")}</p>

<!-- 5 · Trenton -->
<section class="ch" id="trenton">
  <p class="k">Butler County &middot; City of Trenton</p>
  <h2>Issue 17 passed {fmt(trenton["yes"])} to {fmt(trenton["no"])}. The Supreme Court of Ohio put it on the ballot on September 1, after council declined to certify a petition with {SC["holding"].split("petition had ")[1].split(" valid")[0]} valid signatures where {SC["holding"].split("so ")[1].split(" signatures")[0]} were needed.</h2>
  <p class="dek">The charter amendment, the case, the annexation the city withdrew, the county&rsquo;s moratorium and the campus already under construction.</p>
</section>
<div class="tr2">
  <div class="count rise">
    <span class="n">{fmt(trenton["yes"])}<small>to <b>{fmt(trenton["no"])}</b></small></span>
    <p>Issue 17, City of Trenton, proposed charter amendment. {pct(ts['lim'])} percent yes, 8 of 8 precincts, unofficial. {c("butler")}</p>
    <div class="line"><b>25 MW</b><p>The amendment adds a section to Article IX of the charter prohibiting construction of data centers with aggregate monthly demand or peak load above 25 megawatts. The Prologis campus already under construction is outside it. The full text was not obtained by this desk; the opinion and the ballot summary describe it. {c("sc_pdf","butler")}</p></div>
  </div>
  <ol class="docket">
    <li><time datetime="2025-10">October 2025</time><p><b>141 acres sold.</b> The City of Trenton sold 141 acres to Prologis at about $55,000 an acre, about $7.7 million, as reported by Data Center Dynamics and WYSO. {c("dcd","wyso")}</p></li>
    <li><time datetime="2026-06-16">June 16, 2026</time><p><b>The county moratorium.</b> The Butler County commissioners voted unanimously for a six-month moratorium, effective immediately, on the approval, establishment, construction or permitting of any data center in the six townships under county zoning: Hanover, Lemon, Madison, Milford, Oxford and Ross. It runs to about mid-December 2026. The resolution number was not found in the county&rsquo;s online records. {c("wvxu_mora","jn_mora")}</p></li>
    <li><time datetime="2026-07">July 2026</time><p><b>The tax abatement.</b> Council approved a Community Reinvestment Area agreement with Prologis: a 15-year, 75 percent property tax abatement for a campus of four single-story buildings, roughly 880,000 to 1,000,000 square feet in all, with an on-site substation. {c("wyso","dcd")}</p></li>
    <li><time datetime="2026-08">August 2026</time><p><b>The annexation.</b> Trenton petitioned to annex about 601 acres in Madison and St. Clair townships, 358 of them in St. Clair, through the expedited process for a significant economic development project, an Amazon Web Services campus. Both townships filed objections. {c("wvxu_annex","wcpo")}</p></li>
    <li><time datetime="2026-09-01">September 1, 2026</time><p><b>The Supreme Court.</b> In <i>State ex rel. Blankenship v. Trenton City Council</i>, 2026-Ohio-3406, No. 2026-1035, the court granted a limited writ of mandamus. Council&rsquo;s refusal to certify the charter petition was unlawful: under Article XVIII, Section 9 of the Ohio Constitution the threshold is 10 percent of the votes cast at the last general municipal election, 1,277 votes in November 2025, so 128 signatures, and the petition carried 336 valid ones. The court ordered the amendment to the voters at a special election 60 to 120 days after the certifying ordinance. Council then certified it for November 3. {c("sc_pdf","courtnews")}</p></li>
    <li><time datetime="2026-09">Mid-September 2026</time><p><b>The annexation withdrawn.</b> One day before the county commissioners&rsquo; public hearing, Trenton withdrew the annexation petition. The petitioners asked that any hearing be moved to a regular commissioners&rsquo; meeting on or after November 10, 2026, and reserved the right to refile. {c("wcpo")}</p></li>
    <li><time datetime="2026-11-03">November 3, 2026</time><p><b>Issue 17.</b> {fmt(trenton["yes"])} yes, {fmt(trenton["no"])} no. {c("butler")}</p></li>
    <li class="open"><span class="when">Open</span><p>No new annexation petition or hearing date was on the county agenda when this desk looked. The county moratorium ends in about mid-December. A reported capacity figure for the Prologis campus appears in press coverage only; no city or county document stating it was obtained, so none is printed here. {c("wcpo","wvxu_mora","dcd")}</p></li>
  </ol>
</div>

<!-- 6 · the statehouse and the state's deal -->
<section class="ch" id="statehouse">
  <p class="k">Columbus</p>
  <h2>Four bills sit in committee. One passed the House in March. The state&rsquo;s sales-tax exemption for data-center equipment, and the utility regulator&rsquo;s 2025 tariff, are the deal the bills would change.</h2>
  <p class="dek">Status from the House and Senate bill pages, 136th General Assembly, as of November 4. {c("hb646","sb374","hb710","hb957")}</p>
</section>
<div class="bills">
  <div class="bill rise"><span class="no">H.B. 646</span><p class="ti">Create the Data Center Study Commission</p><p>Creates a state Data Center Study Commission. The Senate&rsquo;s June substitute grew into a rewrite of about 50 pages touching the sales-tax exemption, water and energy use.</p><p class="stt">Introduced January 14, 2026 &middot; passed the House March 18 &middot; reported by Senate Energy June 10, informally passed, recommitted<b>In the Senate: recommitted to the Energy Committee {c("hb646")}</b></p></div>
  <div class="bill rise"><span class="no">S.B. 374</span><p class="ti">Prohibit new data center sales tax exemptions</p><p>Amends ORC 122.175 so the Tax Credit Authority may grant no new data-center sales-tax exemptions. Its House companion is H.B. 957.</p><p class="stt">Introduced March 11, 2026<b>Senate Finance Committee since March 25 {c("sb374")}</b></p></div>
  <div class="bill rise"><span class="no">H.B. 710</span><p class="ti">Prohibit public support, limit construction of, new data centers</p><p>Would bar public incentives for new data centers and limit their construction; amends 163.01 and enacts 9.71, 9.711 and 4933.71.</p><p class="stt">Introduced February 24, 2026<b>House General Government Committee since February 25 {c("hb710")}</b></p></div>
  <div class="bill rise"><span class="no">H.B. 957</span><p class="ti">Prohibit new data center sales tax exemption agreements</p><p>The House companion to S.B. 374: no new exemption agreements after October 1, 2026.</p><p class="stt">Introduced May 27, 2026<b>House Ways and Means Committee since June 3 {c("hb957")}</b></p></div>
</div>
<div class="deal">
  <div class="rise"><h3>The sales-tax exemption</h3><p>Ohio Revised Code 122.175 lets the Ohio Tax Credit Authority grant a full or partial sales and use tax exemption on computer data center equipment, and on its delivery, installation and repair, under an agreement with the operator. {c("orc122")} JobsOhio lists the exemption among the state&rsquo;s incentive programs. {c("jobsohio")} S.B. 374 and H.B. 957 would end new agreements; the Senate&rsquo;s version of H.B. 646 would trim the exemption. {c("sb374","hb957","hb646")}</p></div>
  <div class="rise"><h3>The utility regulator&rsquo;s tariff</h3><p>On July 9, 2025, the Public Utilities Commission of Ohio adopted the stipulation among AEP Ohio, commission staff and the Consumers&rsquo; Counsel in Case No. 24-508-EL-ATA: new data-center customers above 25 megawatts pay for at least 85 percent of their subscribed capacity for up to 12 years, with exit fees, and AEP was ordered to file the tariffs and lift its moratorium on new data-center connections. {c("puco","powermag")}</p></div>
  <div class="rise"><h3>November 18, Columbus</h3><p>The third Ohio AI Summit meets at Columbus State Community College&rsquo;s Mitchell Hall. Its 10:20 AM session, &ldquo;AI and Ohio&rsquo;s Innovation Infrastructure Advantage,&rdquo; is described on the agenda as covering &ldquo;data centers and energy systems&rdquo; through &ldquo;advanced manufacturing and the companies supplying critical equipment.&rdquo; The listed speakers are the City of Westerville&rsquo;s economic development director, Vertiv&rsquo;s chief innovation officer and Google&rsquo;s head of data center market development for the Midwest. {c("summit")}</p></div>
</div>

<!-- 7 · what happens next -->
<section class="ch" id="next">
  <p class="k">What happens next</p>
  <h2>Ohio&rsquo;s canvass runs November 14 to 24. Trenton&rsquo;s annexation hearing, if refiled, comes on or after November 10. The county moratorium ends in about mid-December. Two Maine towns still owe a count.</h2>
</section>
<ul class="entries">
  <li><time datetime="2026-11-10">Nov. 10</time><div class="what"><p><b>Trenton&rsquo;s annexation.</b> The earliest date the petitioners asked for a rescheduled hearing before the Butler County commissioners. No new petition or hearing was on the county agenda when this desk looked. {c("wcpo")}</p></div></li>
  <li><time datetime="2026-11-14">Nov. 14 to 24</time><div class="what"><p><b>The official canvass in Ohio.</b> Each county board begins its canvass between the eleventh and fifteenth day after the election and finishes by the twenty-first; for November 3 that is November 14 to 24. Provisional and late-arriving absentee ballots are counted then, and every Ohio number above can move. The other nine states run their own calendars. {c("orc3505")}</p></div></li>
  <li><time datetime="2026-11-18">Nov. 18</time><div class="what"><p><b>The Ohio AI Summit</b> in Columbus, with its 10:20 AM infrastructure session. {c("summit")}</p></div></li>
  <li><time datetime="2026-12">Mid-December</time><div class="what"><p><b>Butler County&rsquo;s moratorium</b> on data centers in the six county-zoned townships reaches six months from June 16. {c("wvxu_mora","jn_mora")}</p></div></li>
  <li><span class="when">Pending</span><div class="what"><p><b>Brownfield and Freedom, Maine,</b> had posted no count on their moratorium questions by Wednesday morning. {c("brownfield","freedom","redbud")} Emporia&rsquo;s and Ottawa&rsquo;s bans in Kansas wait on the district courts. {c("lyon_ks","franklin_ks","redbud")} California&rsquo;s and Nevada&rsquo;s counts continue as mail ballots arrive. {c("lavote","clark_nv")}</p></div></li>
</ul>
<div class="note rise">
  <p><b>Where to check a count yourself.</b> Every row on the board links to the official results page for its county or town, and every Ohio county board posts its sheet at boe.ohio.gov or its own site. The two trackers that kept the roster are Ballotpedia&rsquo;s measure page and Redbud Consulting&rsquo;s datacentersontheballot.com; a third dashboard lists the official page for each jurisdiction. {c("bp_roster","redbud","railway")}</p>
</div>

<!-- sources -->
<section class="srcs" id="srcs" aria-labelledby="srcH">
  <p class="k" id="srcH">Sources</p>
  <ol class="src">
__SOURCES__
  </ol>
  <p class="tm">Results are unofficial until each county, town or state office certifies its canvass. The tally, the board and the dot plot are drawn for this story from the sources above; shares and margins are computed from the counts as posted. Rows marked tracker only carry a tracker&rsquo;s reading of a count whose official sheet this desk could not reach on November 4; the official page is linked on each so a reader can check it.</p>
</section>

<footer>
  <p>Built by <b>Dustin Nimmo</b>, founder of <a href="https://dnsc.ai">DNSC</a> in West&nbsp;Chester, Ohio.</p>
  <p class="sm">Last verified Nov. 4, 2026, against the county and town results pages listed above. If a fact here is wrong, say so and it will be fixed and noted.</p>
  <p class="sm ai-twin">For AIs: <a href="index.md">this page as text</a> &middot; <a href="/llms.txt">site index</a></p>
</footer>
</div>
<script>
(function(){{
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce||!('IntersectionObserver' in window))return;
  document.documentElement.classList.add('mo');
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('on');io.unobserve(e.target);}}}});}},{{threshold:.08}});
  document.querySelectorAll('.rise,.st').forEach(function(el){{io.observe(el);}});
  var t=document.querySelector('.tally');
  if(t){{var rs=t.querySelectorAll('rect');rs.forEach(function(r,i){{r.style.transitionDelay=(i*18)+'ms';}});}}
}})();
</script>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "4cca1d9e1eab422b9abffe2ffd5a9399"}}'></script><!-- End Cloudflare Web Analytics -->
</body></html>
'''

# sources list in citation order
def host(u):
    h = re.sub(r'^https?://(www\.)?', '', u).split('/')[0]
    return h
src_li = []
for i, k in enumerate(ORDER, 1):
    t, u = SRC[k]
    src_li.append(f'    <li id="s{i}">{t}, <a href="{html.escape(u)}">{host(u)}</a>.</li>')
page = page.replace('__SOURCES__', '\n'.join(src_li))
# renumber citations in order of first appearance on the page
body = page.split('<ol class="src">')[0]
seen = []
for m in re.finditer(r'href="#s(\d+)"', body):
    k = int(m.group(1))
    if k not in seen: seen.append(k)
assert len(seen) == len(ORDER), (len(seen), len(ORDER))
remap = {old: i + 1 for i, old in enumerate(seen)}
def fix_cite(m): return f'<a href="#s{remap[int(m.group(1))]}">[{remap[int(m.group(1))]}]</a>'
head, tail = page.split('<ol class="src">')
head = re.sub(r'<a href="#s(\d+)">\[\d+\]</a>', fix_cite, head)
lis = re.findall(r'    <li id="s(\d+)">(.*?)</li>', tail, flags=re.S)
lis = sorted(((remap[int(n)], t) for n, t in lis))
tail_items = '\n'.join(f'    <li id="s{n}">{t}</li>' for n, t in lis)
tail = re.sub(r'(    <li id="s\d+">.*</li>)', lambda m: tail_items, tail, count=1, flags=re.S)
page = head + '<ol class="src">' + tail
# sort citation groups within each span so they read ascending
def sort_group(m):
    items = re.findall(r'<a href="#s(\d+)">\[\d+\]</a>', m.group(1))
    items = sorted(set(int(x) for x in items))
    return '<span class="c">' + ''.join(f'<a href="#s{n}">[{n}]</a>' for n in items) + '</span>'
page = re.sub(r'<span class="c">((?:<a href="#s\d+">\[\d+\]</a>)+)</span>', sort_group, page)
unused = [k for k in SRC if k not in ORDER]
if unused: print('UNUSED SOURCES:', unused)
assert '—' not in page, 'em dash'
open(OUT, 'w').write(page)
CARD = f"""<!doctype html>
<html><head><meta charset="utf-8">
<!-- Share card for civic/data-centers-on-the-ballot, 1200x630. Render: node render.cjs (writes ../../../assets/share/data-centers-on-the-ballot.jpg). Drawn tally only; no logos, no faces. Subjects stay inside x 180..1020. -->
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,500&family=Public+Sans:wght@400;500;700;800&family=IBM+Plex+Mono:wght@400;500&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1200px;height:630px;overflow:hidden;background:#F3F6F8;font-family:"Public Sans",sans-serif;color:#161B21}}
.a{{position:absolute}}
.k{{font-family:"Fraunces",serif;font-style:italic;font-weight:500;font-size:17px;color:#5A636C}}
.k::before{{content:"";display:inline-block;width:20px;height:2px;background:#C9A24A;vertical-align:.3em;margin-right:9px}}
h1{{font-family:"Fraunces",serif;font-weight:600;font-size:36px;line-height:1.12;letter-spacing:-.015em;width:560px}}
h1 .g{{color:#146C4E}}
.sub{{font-weight:400;font-size:17px;line-height:1.42;color:#38414A;width:540px}}
.box{{background:#fff;border:2px solid #161B21;border-radius:22px;padding:16px;width:330px}}
.box svg{{display:block;width:100%;height:auto}}
.wl{{font:500 10px "IBM Plex Mono",monospace;fill:#5A636C;letter-spacing:.04em}}
.wn{{font:400 9px "IBM Plex Mono",monospace;fill:#5A636C}}
.wg{{fill:#146C4E;stroke:#146C4E;stroke-width:1}}.wd{{fill:#4F55B8;stroke:#4F55B8;stroke-width:1}}.wp{{fill:none;stroke:#5A636C;stroke-width:1;stroke-dasharray:2 2}}
.big{{display:block;font:800 40px/1 "Public Sans",sans-serif;letter-spacing:-.03em;color:#161B21;margin:12px 0 4px}}
.big b{{color:#146C4E}}
.box p{{font-size:13.5px;line-height:1.4;color:#38414A}}
.m{{font-family:"IBM Plex Mono",monospace;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5A636C}}
</style></head><body>
<p class="a k" style="left:180px;top:62px">From the record &middot; ten states &middot; November 3, 2026</p>
<h1 class="a" style="left:180px;top:98px">{n_total} data-center questions were on local ballots in ten states. <span class="g">Of the {n_res} with a count, voters took the side that limits data centers in {n_won}.</span> Ohio had {len(oh)} of them, in {oh_places} places, and the limiting side won all {len(oh)}.</h1>
<p class="a sub" style="left:180px;top:410px">The one exception was the City of Harwood, North Dakota, {fmt(harwood["yes"])} to {fmt(harwood["no"])}. Two Maine towns had no count yet. Unofficial until the canvasses close.</p>
<p class="a m" style="left:180px;top:548px">DNSC &middot; tools.dnsc.ai &middot; Data centers on the ballot</p>
<figure class="a box" style="left:790px;top:120px">
  {waffle()}
  <span class="big"><b>{n_won}</b> of {n_res}</span>
  <p>One square per question. Green: the limiting side won. Indigo: the data-center side won. Dashed: no count yet.</p>
</figure>
<script>document.fonts.ready.then(function(){{setTimeout(function(){{document.body.setAttribute('data-ready','1')}},300)}});</script>
</body></html>
"""
import os
open(os.path.dirname(OUT) + '/share/card.html', 'w').write(CARD)
rc = open('/Users/dustinnimmo/DNSC/tools-site/civic/school-levies-2026/share/render.cjs').read().replace('school-levies-2026', 'data-centers-on-the-ballot').replace('card-slv-', 'card-dcb-')
open(os.path.dirname(OUT) + '/share/render.cjs', 'w').write(rc)
print('wrote', OUT, len(page), 'bytes;', len(ORDER), 'sources')
print('TITLE:', TITLE)
print('LEDE:', LEDE)
