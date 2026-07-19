"""Generators for administrative and planning categories."""

import random

from dataset_generator import config
from dataset_generator import utils
from dataset_generator.tracker import UniquenessTracker


def gen_weekly_bulletin_announcement(idx, rng, tracker):
    coordinators = utils.generate_unique_names(15, rng)
    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.4)
    swahili = utils.maybe_swahili(rng, 0.15)
    c = coordinators[idx % len(coordinators)]

    templates = [
        lambda: (
            f"📢 LONDIANI WORSHIPPERS WEEKLY BULLETIN\n"
            f"{'=' * 45}\n\n"
            f"SUNDAY SERVICE — This coming Lord's Day\n"
            f"  First Service: 7:30 AM | Second Service: 10:00 AM\n"
            f"  Venue: Main Sanctuary\n"
            f"  Preacher: Pastor Grace Cheruiyot\n\n"
            f"🔔 ANNOUNCEMENTS:\n\n"
            f"1. MIDWEEK PRAYER MEETING\n"
            f"   Wednesday, 6:00 PM at the Prayer Room.\n"
            f"   Theme: 'Standing in the Gap.' {swahili}All are welcome.\n\n"
            f"2. YOUTH CONFERENCE REGISTRATION\n"
            f"   Deadline: End of this month.\n"
            f"   Contact: {c} (0712-XXX-XXX)\n"
            f"   Venue: Youth Centre, {loc}\n\n"
            f"3. WOMEN'S GUILD MEETING\n"
            f"   Saturday at 2:00 PM, Fellowship Hall.\n"
            f"   {'We will discuss the ' + context + ' outreach initiative.' if context else 'Agenda: annual retreat planning.'}\n\n"
            f"4. CHOIR REHEARSAL\n"
            f"   Thursday & Friday, 5:30 PM.\n"
            f"   New members welcome! Karibu!\n\n"
            f"5. TITHES & OFFERINGS\n"
            f"   Please use the designated envelopes.\n"
            f"   M-Pesa Paybill: XXXXXX\n\n"
            f"{'=' * 45}\n"
            f"'For where two or three gather in my name, there am I with them.' — Matthew 18:20\n"
            f"Bwana asifiwe! See you on Sunday."
        ),
        lambda: (
            f"Dear Londiani Worshippers Family,\n\n"
            f"{swahili}Here are the updates for this week:\n\n"
            f"• SUNDAY SCHOOL TEACHERS NEEDED — We are short-handed for the "
            f"6-8 age group. If you have a heart for children, please see "
            f"{c} after service.\n\n"
            f"• HARVEST THANKSGIVING SERVICE — Scheduled for next Sunday. "
            f"Bring your first fruits! {'The ' + context + ' has been favourable this year.' if context else "Let us celebrate God's provision together."}\n\n"
            f"• COMMUNITY CLEANUP — This Saturday from 8 AM. "
            f"Meet at the church gate. Bring gloves and water.\n\n"
            f"• BIBLE STUDY — Tuesday at 10 AM, {loc} zone cell group. "
            f"Study guide will be shared via WhatsApp.\n\n"
            f"• BUILDING FUND UPDATE — We have reached 60% of our target! "
            f"Mungu akubariki for your generous giving.\n\n"
            f"Reminders:\n"
            f"  — Please switch off phones during prayer time.\n"
            f"  — Ushers: Check your roster for this week's assignments.\n"
            f"  — Hospital visitation team: Departure at 2 PM Wednesday.\n\n"
            f"Asante sana for serving the Lord together.\n"
            f"— Church Office, Londiani Worshippers"
        ),
        lambda: (
            f"⭐ THIS WEEK AT LONDIANI WORSHIPPERS ⭐\n\n"
            f"Monday:    No scheduled activities\n"
            f"Tuesday:   Bible Study — 10:00 AM (Fellowship Hall)\n"
            f"Wednesday: Prayer Meeting — 6:00 PM (Prayer Room)\n"
            f"Thursday:  Choir Practice — 5:30 PM (Main Sanctuary)\n"
            f"Friday:    Youth Alive — 7:00 PM (Youth Centre)\n"
            f"Saturday:  Women's Guild — 2:00 PM | Men's Fellowship — 4:00 PM\n"
            f"Sunday:    Services at 7:30 AM & 10:00 AM\n\n"
            f"SPECIAL NOTICES:\n\n"
            f"⟫ COUPLES' DINNER — Next Friday, 6:30 PM. "
            f"Tickets KES 1,500 per couple. Pay via M-Pesa to Paybill XXXXXX. "
            f"Coordinator: {c}.\n\n"
            f"⟫ MISSIONS SUNDAY — Two weeks from today. "
            f"Guest speaker: Rev. James Mwangi from Nakuru County. "
            f"{'Special collection for the ' + loc + ' mission station.' if 'Kipkelion' in loc or 'Fort' in loc else 'Plan to give generously towards missions.'}\n\n"
            f"⟫ {swahili}CHURCH CONSTRUCTION UPDATE — "
            f"The foundation for the new Sunday School block is complete. "
            f"Phase 2 begins next month. Total raised so far: KES 2,340,000.\n\n"
            f"Need prayer? Text your request to 07XX-XXX-XXX.\n"
            f"We are here for you. Tuko pamoja."
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    authors = ["Church Secretary", "Church Office", "Administrative Assistant", "Bulletin Editor", "Communication Team"]

    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "weekly_bulletin_announcement",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": utils.pick(authors, rng),
            "target_audience": "church members",
            "location_tag": loc,
            "language_mix": "English with Swahili phrases",
            "document_style": "announcement",
            "keywords": rng.sample([
                "bulletin", "announcements", "weekly", "service times",
                "activities", "registration", loc.split()[0].lower(),
                context or "fellowship",
            ], k=rng.randint(4, 6)),
        },
    }


def gen_financial_tithe_report(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.3)

    quarters = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
    quarter = quarters[idx % 4]
    year = rng.randint(2022, 2026)
    month = rng.randint(1, 12)

    tithes = rng.randint(45000, 280000)
    offerings = rng.randint(30000, 190000)
    missions = rng.randint(10000, 65000)
    construction = rng.randint(5000, 45000)
    welfare = rng.randint(8000, 38000)
    youth_fund = rng.randint(5000, 25000)
    total_income = tithes + offerings + missions + construction + welfare + youth_fund

    rent_utility = rng.randint(15000, 40000)
    pastor_stipend = rng.randint(25000, 50000)
    outreach_exp = rng.randint(5000, 20000)
    maintenance = rng.randint(3000, 15000)
    admin = rng.randint(2000, 8000)
    total_expenditure = rent_utility + pastor_stipend + outreach_exp + maintenance + admin
    balance = total_income - total_expenditure

    templates = [
        lambda: (
            f"LONDIANI WORSHIPPERS FINANCIAL SUMMARY\n"
            f"Period: {quarter}, {year}\n"
            f"Prepared by: Church Finance Committee\n"
            f"{'=' * 50}\n\n"
            f"INCOME:\n\n"
            f"  Tithes received:               {utils.format_kes(tithes, rng)}\n"
            f"  General offerings:              {utils.format_kes(offerings, rng)}\n"
            f"  Missions fund contributions:    {utils.format_kes(missions, rng)}\n"
            f"  Building/construction fund:     {utils.format_kes(construction, rng)}\n"
            f"  Welfare fund:                   {utils.format_kes(welfare, rng)}\n"
            f"  Youth ministry fund:            {utils.format_kes(youth_fund, rng)}\n"
            f"  ─────────────────────────────\n"
            f"  TOTAL INCOME:                   {utils.format_kes(total_income, rng)}\n\n"
            f"EXPENDITURE:\n\n"
            f"  Rent & utilities:               {utils.format_kes(rent_utility, rng)}\n"
            f"  Pastoral stipend:               {utils.format_kes(pastor_stipend, rng)}\n"
            f"  Outreach programmes:            {utils.format_kes(outreach_exp, rng)}\n"
            f"  Facility maintenance:           {utils.format_kes(maintenance, rng)}\n"
            f"  Administrative costs:           {utils.format_kes(admin, rng)}\n"
            f"  ─────────────────────────────\n"
            f"  TOTAL EXPENDITURE:              {utils.format_kes(total_expenditure, rng)}\n\n"
            f"NET BALANCE:                      {utils.format_kes(balance, rng)}\n\n"
            f"{'Note: The ' + context + ' has impacted giving patterns this quarter.' if context else 'All figures have been verified by the finance committee.'}\n"
            f"Report submitted for board review. Mungu akubariki for your faithfulness in giving."
        ),
        lambda: (
            f"Financial Report — Londiani Worshippers\n"
            f"Month of {['January','February','March','April','May','June','July','August','September','October','November','December'][month-1]} {year}\n\n"
            f"Dear Church Board,\n\n"
            f"Here is a summary of our financial position for the reporting period.\n\n"
            f"RECEIPTS:\n"
            f"• Tithes: {utils.format_kes(tithes, rng)} — This includes both Sunday collections and M-Pesa transfers.\n"
            f"• Offerings (general): {utils.format_kes(offerings, rng)}\n"
            f"• Designated giving (missions): {utils.format_kes(missions, rng)}\n"
            f"• Construction fund: {utils.format_kes(construction, rng)} — {'Pledges from the harambee are still coming in.' if rng.random() < 0.5 else 'On track with our annual target.'}\n"
            f"• Welfare and compassionate fund: {utils.format_kes(welfare, rng)}\n"
            f"• Youth ministry: {utils.format_kes(youth_fund, rng)}\n\n"
            f"Total receipts: {utils.format_kes(total_income, rng)}\n\n"
            f"DISBURSEMENTS:\n"
            f"• Utilities and rent: {utils.format_kes(rent_utility, rng)}\n"
            f"• Pastor's allowance: {utils.format_kes(pastor_stipend, rng)}\n"
            f"• Community outreach: {utils.format_kes(outreach_exp, rng)}\n"
            f"• Repairs and maintenance: {utils.format_kes(maintenance, rng)} {'— Includes repair of the church gate and plumbing in the kitchen.' if rng.random() < 0.4 else ''}\n"
            f"• Office supplies and admin: {utils.format_kes(admin, rng)}\n\n"
            f"Total disbursements: {utils.format_kes(total_expenditure, rng)}\n\n"
            f"Surplus/(Deficit): {utils.format_kes(balance, rng)}\n\n"
            f"{'We commend the congregation for consistent giving despite the challenges of the ' + context + ' season.' if context else "We thank God for His provision and the congregation's generosity."} "
            f"Detailed ledgers are available for audit upon request.\n\n"
            f"Respectfully submitted,\n— Finance Committee, Londiani Worshippers"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "financial_tithe_report",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": "Finance Committee",
            "target_audience": "church board and members",
            "location_tag": "Londiani Town",
            "language_mix": "primarily English",
            "document_style": "financial_summary",
            "keywords": rng.sample([
                "tithes", "offerings", "financial report", "expenditure",
                "construction fund", "welfare", "missions", "balance",
                context or "giving",
            ], k=rng.randint(4, 7)),
        },
    }


def gen_church_board_minutes_excerpt(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.3)

    board_members = utils.generate_unique_names(8, rng)
    chair = board_members[0]
    secretary = board_members[1]
    present_count = rng.randint(6, 12)
    absent_count = rng.randint(1, 3)

    templates = [
        lambda: (
            f"CHURCH BOARD MINUTES\n"
            f"Londiani Worshippers Church Council\n"
            f"{'=' * 55}\n\n"
            f"Date: [Meeting Date]\n"
            f"Time: 2:00 PM - 5:30 PM\n"
            f"Venue: Conference Room A\n\n"
            f"ATTENDANCE:\n"
            f"  Present: {present_count} members\n"
            f"  Absent with apology: {absent_count}\n"
            f"  Chair: {chair}\n"
            f"  Secretary: {secretary}\n\n"
            f"OPENING:\n"
            f"The meeting was opened with prayer by {board_members[2]}. "
            f"The chair welcomed all members and confirmed quorum.\n\n"
            f"AGENDA:\n\n"
            f"1. MINUTES OF PREVIOUS MEETING\n"
            f"   The minutes of the previous meeting were read and adopted. "
            f"Motion: {board_members[3]}. Second: {board_members[4]}. Carried unanimously.\n\n"
            f"2. FINANCIAL REPORT\n"
            f"   The treasurer presented the quarterly financial statement. "
            f"Total income was {utils.format_kes(rng.randint(200000, 600000), rng)} against expenditure of "
            f"{utils.format_kes(rng.randint(150000, 450000), rng)}. "
            f"Surplus: {utils.format_kes(rng.randint(30000, 150000), rng)}.\n"
            f"   RESOLUTION: The financial report is hereby adopted. "
            f"Motion: {board_members[5]}. Second: {board_members[6] if len(board_members) > 6 else board_members[3]}.\n\n"
            f"3. CHURCH CONSTRUCTION UPDATE\n"
            f"   The building committee reported that the Sunday School block "
            f"foundation is complete. Phase 2 (walls and roofing) requires an additional "
            f"{utils.format_kes(rng.randint(500000, 1200000), rng)}.\n"
            f"   RESOLUTION: Approve the release of {utils.format_kes(rng.randint(200000, 500000), rng)} from the building fund. "
            f"Motion: {board_members[2]}. Second: {board_members[4]}. Carried.\n\n"
            f"4.{' ' + context.upper() + ' RELIEF' if context else ' COMMUNITY OUTREACH'}\n"
            f"   The outreach committee proposed a relief effort for families affected by "
            f"{'the ' + context if context else 'recent challenges'} in {loc}.\n"
            f"   RESOLUTION: Allocate {utils.format_kes(rng.randint(20000, 80000), rng)} for relief supplies. "
            f"Volunteers to be mobilised through the ministry leaders.\n\n"
            f"5. PASTORAL MATTERS\n"
            f"   The pastor reported on membership growth and counselling cases (anonymised). "
            f"Recommendation to hire an assistant pastor was discussed.\n"
            f"   ACTION: The HR committee to prepare a job description and budget proposal "
            f"for review at the next meeting.\n\n"
            f"6. AOB\n"
            f"   • The church compound fence needs repair action: {board_members[3]}\n"
            f"   • Christmas programme planning to begin in October\n"
            f"   • Sound system upgrade approved in principle\n\n"
            f"CLOSING:\n"
            f"The meeting was closed with prayer by the chair at 5:30 PM.\n\n"
            f"Signed:\n"
            f"Chair: _______________ ({chair})\n"
            f"Secretary: _______________ ({secretary})"
        ),
        lambda: (
            f"EXCERPT — CHURCH BOARD MEETING\n"
            f"Londiani Worshippers\n\n"
            f"Chair: {chair} | Secretary: {secretary}\n"
            f"Present: {present_count} | Apologies: {absent_count}\n\n"
            f"KEY DECISIONS:\n\n"
            f"✅ MOTION 1: Approve the annual budget of {utils.format_kes(rng.randint(1800000, 3500000), rng)}\n"
            f"  Proposed: {board_members[3]} | Seconded: {board_members[4]} | Result: Passed\n\n"
            f"✅ MOTION 2: Purchase new PA system for {utils.format_kes(rng.randint(120000, 250000), rng)}\n"
            f"  Proposed: {board_members[5]} | Seconded: {board_members[2]} | Result: Passed\n\n"
            f"❌ MOTION 3: Change Sunday service times\n"
            f"  Proposed: {board_members[6] if len(board_members) > 6 else board_members[0]} | Result: Deferred for congregational input\n\n"
            f"✅ MOTION 4: Approve {utils.format_kes(rng.randint(30000, 75000), rng)} for community outreach in {loc}\n"
            f"  Proposed: {board_members[0]} | Seconded: {board_members[3]} | Result: Passed\n\n"
            f"ACTION ITEMS:\n"
            f"  1. {board_members[4]} — Get three quotes for the PA system by next meeting\n"
            f"  2. {board_members[2]} — Draft the assistant pastor job description\n"
            f"  3. {board_members[5]} — Coordinate {context or 'outreach'} programme logistics\n"
            f"  4. {board_members[3]} — Follow up on compound fence repair\n\n"
            f"Next meeting: First Saturday of next month, 2 PM.\n\n"
            f"— {secretary}, Board Secretary"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "church_board_minutes_excerpt",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": secretary,
            "target_audience": "church board members",
            "location_tag": "Londiani Town",
            "language_mix": "primarily English",
            "document_style": "meeting_minutes",
            "keywords": rng.sample([
                "board minutes", "resolutions", "motions", "action items",
                "financial report", "construction", context or "governance",
                "church council",
            ], k=rng.randint(4, 7)),
        },
    }


def gen_event_calendar_entry(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    coordinator = utils.random_name(rng)

    events = [
        ("Youth Alive Conference 2023", "youth aged 14-30", "Youth Centre, Londiani", 150),
        ("Women of Faith Retreat", "women of all ages", "Kipkelion Parish Hall", 80),
        ("Men's Fellowship Breakfast", "men", "Fellowship Hall, Londiani Worshippers", 45),
        ("Harvest Thanksgiving Celebration", "entire congregation and community", "Main Sanctuary", 300),
        ("Christmas Carol Night", "church family and community", "Church Compound", 200),
        ("Easter Sunrise Service", "all members", "Church Compound (outdoor)", 250),
        ("Couples' Enrichment Weekend", "married and engaged couples", "Conference Centre, Nakuru County", 30),
        ("Children's Holiday Bible Club", "children 4-14 years", "Sunday School Block", 100),
        ("Evangelism Crusade", "community of Kedowa and surrounding areas", "Kedowa Primary School field", 500),
        ("Prayer and Fasting Convention", "intercessors and prayer warriors", "Main Sanctuary", 120),
        ("Church Anniversary Celebration", "all members and former members", "Main Sanctuary and compound", 400),
        ("Leadership Summit", "ministry leaders, deacons, elders", "Conference Room A", 35),
        ("Community Health Fair", "Londiani Town community", "Church Compound", 200),
        ("Missions Awareness Sunday", "congregation", "Main Sanctuary", 280),
        ("New Year Cross-Night Service", "all church members", "Main Sanctuary", 180),
    ]

    event_name, audience, venue, expected = events[idx % len(events)]
    reg_deadline = f"202{rng.randint(2,6)}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"
    event_date = f"202{rng.randint(2,6)}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"

    templates = [
        lambda: (
            f"📅 EVENT: {event_name}\n\n"
            f"Details:\n"
            f"  Date: {event_date}\n"
            f"  Time: {rng.randint(7,18):02d}:00 — {rng.randint(8,22):02d}:00\n"
            f"  Venue: {venue}\n"
            f"  Target audience: {audience}\n"
            f"  Expected attendance: ~{expected}\n"
            f"  Coordinator: {coordinator}\n"
            f"  Registration deadline: {reg_deadline}\n\n"
            f"Description:\n"
            f"This event is organised by Londiani Worshippers and is open to "
            f"the {audience}. "
            f"{'It will feature guest speakers, worship, and practical workshops.' if 'Conference' in event_name or 'Summit' in event_name else ''}"
            f"{'There will be food, games, and a special ministration by the choir.' if 'Anniversary' in event_name or 'Celebration' in event_name or 'Thanksgiving' in event_name else ''}"
            f"{'Attendees are encouraged to come with open hearts for what God will do.' if 'Prayer' in event_name or 'Crusade' in event_name else ''}\n\n"
            f"Registration:\n"
            f"Contact {coordinator} at 07XX-XXX-XXX or register at the information desk after service.\n"
            f"{'Early bird registration available — sign up before the deadline!' if expected > 100 else ''}\n\n"
            f"Volunteer needs: Ushers ({rng.randint(5,15)}), hospitality team ({rng.randint(3,8)}), "
            f"media/technical ({rng.randint(2,5)}).\n\n"
            f"Karibu! All are welcome."
        ),
        lambda: (
            f"EVENT CALENDAR ENTRY\n"
            f"{'─' * 50}\n"
            f"Title: {event_name}\n"
            f"Date: {event_date}\n"
            f"Venue: {venue}\n"
            f"Audience: {audience}\n"
            f"Coordinator: {coordinator}\n"
            f"Expected turnout: {expected}\n"
            f"Registration closes: {reg_deadline}\n"
            f"{'─' * 50}\n\n"
            f"About this event:\n"
            f"A special gathering for {audience}, hosted by Londiani Worshippers. "
            f"The programme includes worship, teaching, fellowship, and prayer.\n\n"
            f"Logistics:\n"
            f"  • Sound and projection: Technical team to set up by 7 AM\n"
            f"  • Seating arrangement: Ushering team\n"
            f"  • Catering: Hospitality team (estimate food for {expected})\n"
            f"  • Security: {rng.randint(2, 5)} personnel assigned\n\n"
            f"Budget estimate: {utils.format_kes(rng.randint(10000, 80000), rng)}\n"
            f"Approved by: Church Board\n\n"
            f"Rain plan: {'Indoor alternative at Fellowship Hall' if 'outdoor' in venue.lower() or 'Compound' in venue or 'field' in venue else 'Venue is indoors no change needed'}\n\n"
            f"For questions, reach {coordinator} via church office."
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "event_calendar_entry",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": coordinator,
            "target_audience": audience,
            "location_tag": loc,
            "language_mix": "English with occasional Swahili",
            "document_style": "event_notice",
            "keywords": rng.sample([
                "event", "calendar", event_name.lower().split()[0],
                "registration", "venue", audience.split()[0],
                loc.split()[0].lower(),
            ], k=rng.randint(4, 7)),
        },
    }


def gen_facility_booking_request(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    event_types = [
        ("Wedding Ceremony", "Kiprono-Koech Wedding", "family and guests"),
        ("Funeral Memorial Service", "Memorial for the Late Rono Family", "mourners and family"),
        ("Choir Rehearsal — Easter Cantata", "Easter Cantata Preparation", "choir members"),
        ("Youth Camp", "Annual Youth Alive Camp", "youth aged 14-25"),
        ("Marriage Seminar", "Building Lasting Marriages Seminar", "engaged and married couples"),
        ("Women's Conference", "Women of Faith Conference", "women from Kericho County churches"),
        ("Leadership Training", "Church Leadership Workshop", "ministry leaders and deacons"),
        ("Children's Day Celebration", "Children's Sunday Extravaganza", "children and parents"),
        ("Harvest Thanksgiving", "Harvest Celebration Service", "congregation and community"),
        ("Baptism Service", "Baptism and Dedication Service", "candidates and families"),
        ("Couples' Dinner", "Valentine Couples' Banquet", "married couples"),
        ("Board Strategy Meeting", "Annual Strategic Planning Meeting", "church board members"),
        ("Prayer Conference", "24-Hour Prayer Marathon", "prayer warriors and intercessors"),
        ("Community Health Camp", "Free Medical Camp", "community members"),
        ("Christmas Cantata Rehearsal", "Christmas Programme Rehearsal", "choir and drama team"),
    ]

    event_name, event_detail, audience = event_types[idx % len(event_types)]
    requester = utils.random_name(rng)
    venue = utils.pick(config.VENUES, rng)
    expected_attendance = rng.randint(20, 300)
    setup_date = utils.random_timestamp(rng)
    event_date_str = f"202{rng.randint(2,6)}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"

    templates = [
        lambda: (
            f"FACILITY BOOKING REQUEST\n"
            f"{'=' * 50}\n\n"
            f"Request ID: FBR-{rng.randint(100,999):03d}\n"
            f"Date Submitted: {setup_date[:10]}\n\n"
            f"EVENT DETAILS:\n"
            f"  Event: {event_name}\n"
            f"  Description: {event_detail}\n"
            f"  Requested Venue: {venue}\n"
            f"  Event Date: {event_date_str}\n"
            f"  Setup Time: 8:00 AM\n"
            f"  Event Start: 10:00 AM\n"
            f"  Expected End: 4:00 PM\n"
            f"  Expected Attendance: ~{expected_attendance}\n\n"
            f"REQUESTER INFORMATION:\n"
            f"  Name: {requester}\n"
            f"  Role: Event Coordinator\n"
            f"  Phone: 07XX-XXX-XXX\n\n"
            f"SPECIAL REQUIREMENTS:\n"
            f"  [X] Sound system\n"
            f"  [X] Projector and screen\n"
            f"  {'[X]' if expected_attendance > 100 else '[ ]'} Additional chairs\n"
            f"  {'[X]' if 'Wedding' in event_name else '[ ]'} Decoration permission\n"
            f"  [X] Kitchen access for meal preparation\n"
            f"  {'[X]' if 'Youth' in event_name else '[ ]'} Overnight accommodation\n\n"
            f"BUDGET ESTIMATE: {utils.format_kes(rng.randint(5000, 45000), rng)}\n\n"
            f"APPROVAL STATUS: ☐ Pending\n\n"
            f"Comments:\n"
            f"Please confirm availability of {venue} by end of this week. "
            f"{'We may need the outdoor area as well if attendance exceeds our expectation.' if expected_attendance > 80 else ''}\n\n"
            f"— {requester}"
        ),
        lambda: (
            f"Booking Request Form\n"
            f"Londiani Worshippers Church\n\n"
            f"I am writing to request the use of the {venue} for the following event:\n\n"
            f"Event Name: {event_name}\n"
            f"Organised by: {requester}\n"
            f"Date: {event_date_str}\n"
            f"Time: {rng.randint(7,18):02d}:00 — {rng.randint(8,21):02d}:00\n"
            f"Expected attendees: {expected_attendance}\n"
            f"Target audience: {audience}\n\n"
            f"Equipment needed:\n"
            f"  1. Microphones (2 handheld, 1 lapel)\n"
            f"  2. PA system\n"
            f"  3. {'Projector' if 'Seminar' in event_name or 'Training' in event_name or 'Camp' in event_name else 'Pulpit and communion table'}\n\n"
            f"Catering: {'Yes — lunch for all attendees' if expected_attendance < 60 else 'Light refreshments only'}\n"
            f"Cleaning: We will arrange cleaning after the event.\n\n"
            f"I understand and agree to abide by the church facility use policy.\n"
            f"Please contact me at 07XX-XXX-XXX to confirm.\n\n"
            f"Thank you and God bless.\n— {requester}"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "facility_booking_request",
        "timestamp": setup_date,
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": requester,
            "target_audience": "church administration",
            "location_tag": loc,
            "language_mix": "primarily English",
            "document_style": "administrative_request",
            "keywords": rng.sample([
                "booking", "facility", event_name.lower().split()[0],
                "venue", "event", "request", "scheduling",
            ], k=rng.randint(4, 6)),
        },
    }


def gen_volunteer_roster_notice(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    swahili = utils.maybe_swahili(rng, 0.1)

    teams_list = list(config.VOLUNTEER_TEAMS)
    team = teams_list[idx % len(teams_list)]
    team_lead = utils.random_name(rng)

    members = utils.generate_unique_names(rng.randint(4, 10), rng)
    sundays = ["1st Sunday", "2nd Sunday", "3rd Sunday", "4th Sunday", "5th Sunday"]
    assigned_sunday = utils.pick(sundays, rng)

    templates = [
        lambda: (
            f"VOLUNTEER ROSTER — {team.upper()} TEAM\n"
            f"Londiani Worshippers\n"
            f"{'=' * 55}\n\n"
            f"Team Lead: {team_lead}\n"
            f"Assignment: {assigned_sunday} of each month\n\n"
            f"ROSTER FOR THIS MONTH:\n\n"
            f"First Service (7:30 AM):\n"
            f"  • {members[0]}\n"
            f"  • {members[1] if len(members) > 1 else 'Volunteer needed'}\n\n"
            f"Second Service (10:00 AM):\n"
            f"  • {members[2] if len(members) > 2 else 'Volunteer needed'}\n"
            f"  • {members[3] if len(members) > 3 else 'Volunteer needed'}\n"
            f"  • {members[4] if len(members) > 4 else 'Volunteer needed'}\n\n"
            f"DUTY REMINDERS:\n"
            f"  ✓ Arrive at least 20 minutes before service starts\n"
            f"  ✓ Check in with the team lead at the designated station\n"
            f"  ✓ Wear your volunteer badge\n"
            f"  ✓ If unable to serve, find a replacement and inform {team_lead}\n\n"
            f"{'SWAP NEEDED: ' + members[0] + ' is unavailable this Sunday. Can someone cover? Please WhatsApp the group.' if rng.random() < 0.3 else ''}\n\n"
            f"{swahili}Thank you for serving the Lord through this ministry. "
            f"Your dedication makes a difference every Sunday.\n\n"
            f"— {team_lead}, {team} Team Lead"
        ),
        lambda: (
            f"📢 {team.upper()} TEAM — SERVICE ROSTER\n\n"
            f"Hello team! Here is your schedule:\n\n"
            f"DATE: {assigned_sunday}\n"
            f"TEAM LEAD: {team_lead}\n\n"
            f"ASSIGNMENTS:\n"
            f"  1. {members[0]} — {loc if rng.random() < 0.3 else 'Main entrance'}\n"
            f"  2. {members[1] if len(members) > 1 else 'OPEN'} — Side entrance\n"
            f"  3. {members[2] if len(members) > 2 else 'OPEN'} — {'Back row area' if team == 'Ushers' else 'Sound booth'}\n"
            f"  4. {members[3] if len(members) > 3 else 'OPEN'} — {'Parking lot' if team == 'Parking' else 'Altar area'}\n\n"
            f"CHECKLIST:\n"
            f"  □ Report by 7:10 AM (first service) or 9:40 AM (second service)\n"
            f"  □ Coordinate with other teams at the 7:00 AM huddle\n"
            f"  □ Ensure all equipment/supplies are in place before service\n"
            f"  □ Debrief briefly after service\n\n"
            f"Need to swap? Contact {team_lead} directly. "
            f"Please do not just skip — every role matters for a smooth service.\n\n"
            f"{swahili}Asante sana for your commitment! "
            f"If anyone wants to join the {team.lower()} team, speak to {team_lead} after service.\n\n"
            f"Tuko pamoja! 💪"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "volunteer_roster_notice",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": team_lead,
            "target_audience": f"{team.lower()} team volunteers",
            "location_tag": loc,
            "language_mix": "primarily English",
            "document_style": "roster_notice",
            "keywords": rng.sample([
                "volunteer", "roster", team.lower(), "schedule",
                "service duty", "team", "assignment",
            ], k=rng.randint(4, 6)),
        },
    }
