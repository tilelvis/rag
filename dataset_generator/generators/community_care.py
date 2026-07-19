"""Generators for community, care, and personal categories."""

import random

from dataset_generator import config
from dataset_generator import utils
from dataset_generator.tracker import UniquenessTracker


def gen_ministry_leader_update(idx, rng, tracker):
    ministries = list(config.MINISTRY_NAMES)
    ministry = ministries[idx % len(ministries)]
    leader = utils.random_name(rng)
    tracker.add_name(leader)

    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.5)
    swahili = utils.maybe_swahili(rng, 0.15)

    templates = [
        lambda: (
            f"MINISTRY UPDATE: {ministry.upper()}\n"
            f"Submitted by: {leader}, Ministry Leader\n"
            f"Reporting Period: Last Quarter\n\n"
            f"Greetings, Church Board and Pastoral Team,\n\n"
            f"{swahili}Here is our quarterly update on the activities and progress "
            f"of the {ministry}.\n\n"
            f"KEY HIGHLIGHTS:\n\n"
            f"1. Membership: We currently have {rng.randint(12, 65)} active members. "
            f"This is a {rng.choice(['15% increase', 'steady maintenance', 'slight decrease of 5%'])} from last quarter.\n\n"
            f"2. Activities Completed:\n"
            f"   • Hosted a fellowship in {loc} with {rng.randint(25, 120)} attendees\n"
            f"   • {'Completed the ' + context + ' awareness campaign' if context else 'Organized three prayer and fasting days'}\n"
            f"   • Visited {rng.randint(3, 8)} home fellowships\n"
            f"   • Conducted {rng.randint(2, 5)} training sessions for new members\n\n"
            f"3. Challenges:\n"
            f"   • Low attendance on weekdays due to {context or 'work schedules and distance'}\n"
            f"   • Need for more volunteers in the {rng.randint(2, 5)} sub-committees\n"
            f"   • Budget constraints limiting outreach to surrounding areas\n\n"
            f"4. Upcoming Plans:\n"
            f"   • Retreat planned for next month at a venue near {loc}\n"
            f"   • Joint service with neighbouring churches in Kericho County\n"
            f"   • Leadership training workshop\n\n"
            f"5. Prayer Requests:\n"
            f"   • Wisdom for the leadership team\n"
            f"   • More labourers for the harvest\n"
            f"   • Unity and love among members\n\n"
            f"Tuko pamoja in Christ.\n— {leader}"
        ),
        lambda: (
            f"From the desk of {leader}\n"
            f"{ministry} — Monthly Report\n\n"
            f"Dear Pastor and Church Family,\n\n"
            f"God has been faithful! {swahili}Let me share what He has been doing through "
            f"our {ministry} this past month.\n\n"
            f"WHAT WE DID:\n"
            f"✓ Held {rng.randint(3, 6)} regular meetings\n"
            f"✓ Participated in the Sunday service programme\n"
            f"✓ {'Assisted families affected by the ' + context if context else 'Provided support to 4 families in need'}\n"
            f"✓ Organized a special event at {loc} that drew {rng.randint(30, 80)} people\n\n"
            f"TESTIMONY:\n"
            f"One of our members shared how the {ministry.lower()} helped them navigate "
            f"a difficult season. They said, \"I was ready to give up, but the "
            f"prayers and support of this group kept me going.\" Bwana asifiwe!\n\n"
            f"NEEDS:\n"
            f"  → We need Bibles for new members (approximately {rng.randint(5, 15)})\n"
            f"  → Transport support for visits to distant zones like {loc}\n"
            f"  → A dedicated meeting space (currently sharing with another ministry)\n\n"
            f"NEXT MONTH'S FOCUS:\n"
            f"  • Evangelism drive in the {loc} area\n"
            f"  • Mentorship programme launch\n\n"
            f"Asante sana for your continued support and prayers.\n— {leader}, {ministry}"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    audiences = ["church board and pastoral team", "ministry members", "congregation"]
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "ministry_leader_update",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": leader,
            "target_audience": utils.pick(audiences, rng),
            "location_tag": loc,
            "language_mix": "English with occasional Swahili",
            "document_style": "ministry_report",
            "keywords": rng.sample([
                "ministry update", ministry.lower(), "activities",
                "challenges", "prayer requests", "volunteers",
                loc.split()[0].lower(), context or "fellowship",
            ], k=rng.randint(4, 7)),
        },
    }


def gen_community_outreach_log(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.6)
    swahili = utils.maybe_swahili(rng, 0.12)

    outreach_types = [
        ("Hospital Visitation", "hospital visit", "patients and staff"),
        ("Home Fellowship Outreach", "home fellowship", "neighbourhood families"),
        ("Prison Ministry Visit", "prison ministry", "inmates at Londiani Prison"),
        ("School Visit and Mentorship", "school visit", "students and teachers"),
        ("Food Distribution Drive", "food distribution", "vulnerable families"),
        ("Elderly Care Visit", "elderly care", "senior citizens"),
        ("Community Cleanup Campaign", "cleanup", "Londiani Town residents"),
        ("Tree Planting Initiative", "tree planting", "environmental volunteers"),
        ("Market Day Evangelism", "evangelism", "market traders and shoppers"),
        ("Water Project Support", "water project", "Koru and Kedowa communities"),
        ("Youth Empowerment Workshop", "youth empowerment", "unemployed youth"),
        ("Health Awareness Campaign", "health awareness", "community members"),
        ("Orphanage Visit", "orphanage visit", "children at Sunshine Home"),
        ("Boda Boda Chaplaincy", "chaplaincy", "boda boda riders"),
        ("Interfaith Community Dialogue", "interfaith dialogue", "faith leaders in Kipkelion"),
    ]

    outreach_name, activity, target = outreach_types[idx % len(outreach_types)]
    team_lead = utils.random_name(rng)
    team_size = rng.randint(3, 15)
    people_reached = rng.randint(10, 200)

    templates = [
        lambda: (
            f"COMMUNITY OUTREACH LOG\n"
            f"{'=' * 45}\n"
            f"Activity: {outreach_name}\n"
            f"Date: [Report Date]\n"
            f"Location: {loc}\n"
            f"Team Lead: {team_lead}\n"
            f"Team Size: {team_size} volunteers\n"
            f"{'=' * 45}\n\n"
            f"NARRATIVE:\n\n"
            f"{swahili}The team departed from the church compound at 8:30 AM and "
            f"arrived at {loc} at approximately 9:15 AM. "
            f"We began with a time of prayer and then divided into {rng.randint(2, 4)} groups.\n\n"
            f"Group 1 focused on {activity}, engaging with approximately "
            f"{people_reached // 3} {target.split(' and ')[0] if ' and ' in target else target}.\n"
            f"Group 2 handled distribution of materials and supplies.\n"
            f"{'Group 3 conducted a brief worship session and shared the gospel.' if team_size > 8 else ''}\n\n"
            f"KEY OBSERVATIONS:\n"
            f"  • {'The ' + context + ' has significantly affected the livelihood of residents.' if context else 'There is great spiritual hunger in the community.'}\n"
            f"  • Many families expressed gratitude for the church's presence\n"
            f"  • {rng.randint(3, 12)} people gave their lives to Christ during the outreach\n"
            f"  • Follow-up is needed for {rng.randint(5, 20)} individuals who requested prayer\n\n"
            f"MATERIALS DISTRIBUTED:\n"
            f"  - Food packages: {rng.randint(20, 80)}\n"
            f"  - Tracts and Bibles: {rng.randint(15, 50)}\n"
            f"  - Clothing items: {rng.randint(10, 40)}\n\n"
            f"FOLLOW-UP ACTIONS:\n"
            f"  □ Schedule return visit within two weeks\n"
            f"  □ Connect new converts with a local cell group\n"
            f"  □ Report to the Outreach Committee by Friday\n\n"
            f"Tuko pamoja for the Kingdom.\n— {team_lead}"
        ),
        lambda: (
            f"OUTREACH REPORT — {outreach_name.upper()}\n\n"
            f"Where: {loc}\n"
            f"When: [Date] | Who: {team_lead} + {team_size} team members\n"
            f"People reached: ~{people_reached}\n\n"
            f"WHAT HAPPENED:\n\n"
            f"We had a powerful time of {activity} today! {swahili}"
            f"The community in {loc} was very receptive. "
            f"{"Many were struggling because of the " + context + ", and they were touched by the church's gesture of love." if context else 'People opened up about their struggles and we were able to pray with many of them.'}\n\n"
            f"HIGHLIGHTS:\n"
            f"  → Shared the Word of God with {people_reached} people\n"
            f"  → Distributed relief items to {rng.randint(10, 30)} families\n"
            f"  → Prayed with {rng.randint(5, 15)} individuals for various needs\n"
            f"  → {rng.randint(2, 8)} people committed to joining a local fellowship\n\n"
            f"CHALLENGES:\n"
            f"  ✗ Poor road access to some homesteads\n"
            f"  ✗ Insufficient supplies — demand exceeded what we carried\n"
            f"  ✗ {'Weather was unfavourable due to the ' + context if context and 'rain' in context else 'Short time limited our reach'}\n\n"
            f"RECOMMENDATIONS:\n"
            f"  1. Increase budget allocation for community outreach\n"
            f"  2. Visit {loc} monthly instead of quarterly\n"
            f"  3. Partner with other churches in the area\n\n"
            f"Mungu akubariki! The harvest is plentiful.\n— {team_lead}"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "community_outreach_log",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": team_lead,
            "target_audience": target,
            "location_tag": loc,
            "language_mix": "English with occasional Swahili",
            "document_style": "outreach_report",
            "keywords": rng.sample([
                "outreach", activity, "community", "evangelism",
                "volunteer", "follow-up", loc.split()[0].lower(),
                context or "service",
            ], k=rng.randint(4, 7)),
        },
    }


def gen_counseling_intake_summary(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)

    presenting_issues = [
        ("grief and loss", "Client is mourning the loss of a close family member. "
         "Reports difficulty sleeping and loss of appetite since the passing three months ago. "
         "Expresses anger at God and confusion about faith."),
        ("addiction recovery", "Client acknowledges dependence on alcohol for the past several years. "
         "Reports desire to stop but has experienced multiple relapses. "
         "Family relationships have been severely affected."),
        ("parenting challenges", "Client describes ongoing conflict with teenage children. "
         "Reports feeling overwhelmed and unsure how to maintain authority while showing love. "
         "One child has dropped out of school."),
        ("marriage preparation", "Couple is preparing for marriage and wishes to address "
         "communication patterns and financial expectations before the wedding. "
         "Both come from different church backgrounds."),
        ("conflict resolution", "Client is in a prolonged dispute with a family member over "
         "inheritance and property. The conflict has created a deep rift and is affecting "
         "spiritual life and church attendance."),
        ("financial stress", "Client reports overwhelming debt and inability to meet basic needs. "
         "Has been borrowing from multiple sources. Feels hopeless and ashamed. "
         "Is employed but income is insufficient."),
        ("unemployment and identity", "Client lost employment eight months ago and has been unable "
         "to find new work. Reports feelings of worthlessness and question about God's plan. "
         "Has withdrawn from social activities at church."),
        ("faith struggles", "Client describes a period of spiritual dryness lasting over a year. "
         "Reports inability to pray or read the Bible. Attends church out of habit "
         "but feels no connection to God."),
        ("marital conflict", "Couple reports frequent arguments and emotional distance. "
         "Communication has broken down. Both express love but feel unheard. "
         "Children are being affected by the tension at home."),
        ("anxiety and worry", "Client experiences persistent worry about the future, "
         "health, and family safety. Reports physical symptoms including headaches "
         "and chest tightness. Difficulty concentrating at work."),
        ("trauma recovery", "Client is a survivor of a violent incident. Experiences "
         "flashbacks and avoids certain locations. Has not shared the experience "
         "with family members. Seeks spiritual and emotional healing."),
        ("blended family adjustment", "Client recently married into a blended family. "
         "Reports challenges with step-children's acceptance and conflicting "
         "parenting styles. Seeking guidance on building a united household."),
        ("loneliness and isolation", "Client is a widow living alone in a rural area near "
         f"{loc}. Children live far away. Reports deep loneliness and loss of purpose. "
         "Attends church but does not feel connected to others."),
        ("academic pressure and burnout", "Client is a university student facing intense "
         "academic pressure. Reports anxiety about exams and fear of failure. "
         "Has considered dropping out. Spiritual life has suffered."),
        ("chronic illness and faith", "Client was recently diagnosed with a chronic condition. "
         "Struggling to understand how God allows suffering. Questions about healing "
         "and the purpose of prayer in illness."),
    ]

    issue, description = presenting_issues[idx % len(presenting_issues)]

    counselors = [
        "Pastoral Counsellor A", "Lay Counsellor B", "Counselling Team Lead",
        "Pastoral Care Coordinator", "Church Counsellor C",
    ]
    counselor = utils.pick(counselors, rng)
    sessions_completed = rng.randint(1, 8)

    templates = [
        lambda: (
            f"COUNSELLING INTAKE SUMMARY — CONFIDENTIAL\n"
            f"{'=' * 55}\n"
            f"Case Reference: CND-{rng.randint(100,999):03d}\n"
            f"Counsellor: {counselor}\n"
            f"Sessions completed: {sessions_completed}\n"
            f"Presenting concern: {issue}\n"
            f"{'=' * 55}\n\n"
            f"PRESENTING ISSUE:\n"
            f"{description}\n\n"
            f"ASSESSMENT:\n"
            f"Client appeared {rng.choice(['distressed', 'calm but withdrawn', 'anxious', 'cooperative and open', 'guarded initially'])}. "
            f"Verbal communication was {rng.choice(['clear and coherent', 'somewhat fragmented', 'measured and thoughtful', 'emotional with periods of silence'])}. "
            f"Client expressed willingness to engage in the counselling process.\n\n"
            f"GOALS IDENTIFIED:\n"
            f"  1. Process the presenting concern in a safe and supportive environment\n"
            f"  2. Develop healthy coping strategies grounded in biblical truth\n"
            f"  3. Restore and strengthen spiritual connection\n"
            f"  4. Improve relational dynamics where applicable\n\n"
            f"APPROACH:\n"
            f"  • Biblically-integrated counselling with active listening\n"
            f"  • Scripture meditation and prayer as part of each session\n"
            f"  • Referral to professional therapist if symptoms persist beyond church counselling scope\n\n"
            f"SESSION NOTES (Summary):\n"
            f"Session 1: Intake and rapport building. Client shared history reluctantly. "
            f"Prayed together at close.\n"
            f"{'Session 2: Client showed slight improvement in openness. Discussed coping mechanisms.' if sessions_completed > 1 else ''}\n"
            f"{'Session 3+: Ongoing support. Client reports incremental progress.' if sessions_completed > 2 else ''}\n\n"
            f"DISPOSITION:\n"
            f"  ☐ Continue counselling\n"
            f"  ☐ Refer to professional therapist\n"
            f"  ☐ Spiritual direction recommended\n\n"
            f"NOTE: All identifying information has been removed. "
            f"This document is stored securely and is accessible only to authorised counselling staff.\n\n"
            f"— {counselor}"
        ),
        lambda: (
            f"Intake Form — Counselling Ministry, Londiani Worshippers\n"
            f"CONFIDENTIAL — DO NOT DISTRIBUTE\n\n"
            f"Ref #: CND-{rng.randint(200,999):03d}\n"
            f"Counsellor assigned: {counselor}\n"
            f"Presenting issue: {issue}\n\n"
            f"CLIENT NARRATIVE:\n"
            f"{description}\n\n"
            f"OBSERVATIONS:\n"
            f"  Affect: {rng.choice(['sad', 'anxious', 'flat', 'tearful', 'hopeful despite pain'])}\n"
            f"  Engagement level: {rng.choice(['high — client is motivated', 'moderate — willing but hesitant', 'low — initially resistant'])}\n"
            f"  Risk assessment: {rng.choice(['no immediate risk', 'low risk — monitoring recommended', 'moderate concern — referral considered'])}\n\n"
            f"AGREED FOCUS AREAS:\n"
            f"  → Understanding the situation through a biblical lens\n"
            f"  → Developing practical steps forward\n"
            f"  → Building a support network within the church community\n\n"
            f"SESSION COUNT: {sessions_completed} to date\n"
            f"NEXT APPOINTMENT: To be scheduled\n\n"
            f"Every person is created in the image of God and deserves "
            f"dignity, compassion, and confidentiality.\n\n"
            f"— {counselor}"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "counseling_intake_summary",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": counselor,
            "target_audience": "counselling team (confidential)",
            "location_tag": "Londiani Town",
            "language_mix": "primarily English",
            "document_style": "clinical_summary",
            "keywords": rng.sample([
                "counselling", "intake", issue.split()[0], issue.split()[-1],
                "confidential", "assessment", "pastoral care",
            ], k=rng.randint(4, 6)),
        },
    }


def gen_prayer_request_wall(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    swahili = utils.maybe_swahili(rng, 0.18)

    request_types = [
        ("thanksgiving", "Thanksgiving for passing exams! After months of "
         f"prayer and hard study, I received my results and I passed all subjects. "
         f"{swahili}God is faithful! I want to encourage every student do not give up."),
        ("healing", "Please pray for my mother who is admitted at Londiani District Hospital. "
         f"She has been sick for two weeks now. {'The doctors are still running tests.' if rng.random() < 0.5 else 'She has a heart condition.'} "
         f"We trust God for complete healing. Bwana asifiwe."),
        ("exams", "Praying for my KCSE exams starting next month. I am nervous but I know "
         f"God is with me. My family in {loc} is supporting me but finances are tight. "
         f"Please remember me in your prayers."),
        ("employment", "I have been looking for work for over a year now. "
         f"I am a trained teacher but there are no vacancies. {'It has been hard especially during the ' + utils.pick(config.LOCAL_CONTEXT, rng) + ' season.' if rng.random() < 0.5 else ''} "
         f"Please pray that God opens a door. Mungu akubariki."),
        ("travel", "My husband is traveling to Nairobi for a job interview on Tuesday. "
         f"Please pray for safe journey on the Molo Road and for favour in the interview. "
         f"{swahili}We trust God for this opportunity."),
        ("family", "Pray for unity in my family. There is tension between my siblings "
         f"over our late father's property near {loc}. "
         f"It has divided us and I am heartbroken. We need God's intervention."),
        ("pregnancy", "We are expecting our first child! Please pray for a safe pregnancy "
         f"and delivery. My wife has had complications before so we are trusting God "
         f"completely. {'The doctor in ' + loc + ' is monitoring her closely.' if loc != 'Londiani Town' else ''} "
         f"Asante sana for standing with us."),
        ("harvest", "Thank God with us for a bountiful maize harvest this season! "
         f"After the rains were delayed, we thought we would lose everything. "
         f"{'The ' + utils.pick(config.LOCAL_CONTEXT, rng) + ' has been good to us.' if rng.random() < 0.5 else 'He never fails.'} "
         f"{swahili}Bwana asifiwe!"),
        ("business", "Pray for my small shop in {loc}. Business has been very slow "
         f"this quarter and I am struggling to pay rent. I believe God will provide "
         f"but I need your prayers for strength and wisdom."),
        ("spiritual growth", "I have been feeling distant from God lately. "
         f"I go to church but my heart feels empty. Please pray that the Lord "
         f"draws me close again. {swahili}I want to experience His presence like before."),
        ("housing", "We are being asked to vacate our rental house by end of month. "
         f"We have nowhere to go. Please pray that God provides a home for our family "
         f"of five. {'I work on a tea farm near ' + loc + ' but the pay is not enough for a new deposit.' if rng.random() < 0.5 else ''}"),
        ("addiction", "Pray for my brother who is struggling with alcohol. "
         f"He wants to change but keeps falling back. The family is hurting. "
         f"We believe God can deliver him completely. Tuko pamoja in prayer."),
        ("peace", "Please pray for peace in our community. There have been tensions "
         f"between neighbouring farms near {loc} over grazing land. "
         f"We need wisdom and reconciliation. Mungu watie amani."),
        ("education", "My daughter has received a scholarship offer to study at university! "
         f"We are so grateful. {swahili}Please pray for provision for the remaining fees "
         f"and for her adjustment to campus life. God is good!"),
        ("ministry", "Pray for our evangelism team as we plan to reach {loc} "
         f"next month. We need boldness, resources, and open hearts. "
         f"The harvest is plentiful but the labourers are few. Amen."),
    ]

    req_type, text = request_types[idx % len(request_types)]
    text = text.replace("{loc}", loc)

    templates = [
        lambda: (
            f"🙏 PRAYER REQUEST\n\n"
            f"{text}\n\n"
            f"— Submitted by: A church member"
        ),
        lambda: (
            f"Prayer Wall — Londiani Worshippers\n\n"
            f"Request Type: {req_type}\n\n"
            f"{text}\n\n"
            f"[Posted anonymously via the prayer request box]"
        ),
        lambda: (
            f"{text}\n\n"
            f"Please lift this in your prayer time. "
            f"If you have a word of encouragement, leave it on the prayer wall or "
            f"send via WhatsApp. Tuko pamoja."
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "prayer_request_wall",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": "anonymous church member",
            "target_audience": "prayer team and congregation",
            "location_tag": loc,
            "language_mix": "English with Swahili phrases",
            "document_style": "personal_submission",
            "keywords": rng.sample([
                "prayer request", req_type, "intercession", "faith",
                loc.split()[0].lower(), "community",
            ], k=rng.randint(3, 6)),
        },
    }


def gen_visitor_welcome_followup(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    followup_person = utils.random_name(rng)
    visitor_initials = f"{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[rng.randint(0,25)]}.{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[rng.randint(0,25)]}."

    channels = ["SMS", "WhatsApp message", "Email", "Welcome letter", "SMS"]
    channel = channels[idx % len(channels)]

    templates = [
        # SMS
        lambda: (
            f"[SMS to {visitor_initials}]\n\n"
            f"Karibu! Thank you for worshipping with us at Londiani Worshippers today. "
            f"We would love to connect with you. Feel free to join our WhatsApp group "
            f"or call 07XX-XXX-XXX for any questions. Mungu akubariki! — {followup_person}"
        ),
        # WhatsApp
        lambda: (
            f"[WhatsApp message to {visitor_initials}]\n\n"
            f"Hello! 😊 This is {followup_person} from Londiani Worshippers. "
            f"We were so glad to see you in service today! "
            f"{'I hope the message spoke to your heart.' if rng.random() < 0.5 else 'It was a blessing to have you with us.'} "
            f"We have a newcomers' class every Wednesday at 6 PM — it's a great way to "
            f"learn more about our church family. Would you be interested? "
            f"Also, here's a link to our weekly bulletin and events calendar. "
            f"Feel free to ask me anything! Tuko pamoja. 🙏"
        ),
        # Email
        lambda: (
            f"Subject: Welcome to Londiani Worshippers!\n\n"
            f"Dear {visitor_initials},\n\n"
            f"Greetings in the name of our Lord Jesus Christ!\n\n"
            f"Thank you for visiting Londiani Worshippers this past Sunday. "
            f"We are delighted that you chose to worship with us, and we pray that "
            f"you felt the presence of God in our midst.\n\n"
            f"We would love to get to know you better and help you find your place "
            f"in our church family. Here are a few ways to connect:\n\n"
            f"  • Newcomers' Class: Every Wednesday at 6:00 PM in the Fellowship Hall\n"
            f"  • Cell Groups: We have home fellowships across {loc} and surrounding areas\n"
            f"  • Ministry Opportunities: From choir to children's church, there is a place for everyone\n\n"
            f"If you have any prayer requests, please do not hesitate to share them with us. "
            f"You can reply to this email or call our church office at 052-XXX-XXX.\n\n"
            f"Once again, karibu! We look forward to seeing you again soon.\n\n"
            f"May the Lord bless you and keep you.\n\n"
            f"Warm regards,\n{followup_person}\nVisitor Follow-up Team\nLondiani Worshippers"
        ),
        # Welcome letter (formal)
        lambda: (
            f"LONDIANI WORSHIPPERS\n"
            f"P.O. Box XXX, Londiani\n"
            f"Kericho County, Kenya\n\n"
            f"Date: [Current Date]\n\n"
            f"{visitor_initials}\n"
            f"[Address on file]\n\n"
            f"Dear {visitor_initials},\n\n"
            f"On behalf of the entire congregation of Londiani Worshippers, I write to "
            f"express our joy at your visit with us. It is always a blessing when the "
            f"Lord brings new people into our fellowship, and we trust that your time "
            f"with us was uplifting.\n\n"
            f"Londiani Worshippers is a community of believers committed to glorifying God, "
            f"making disciples, and serving our neighbours in {loc} and beyond. "
            f"We would be honoured to walk alongside you in your faith journey.\n\n"
            f"As a next step, I encourage you to:\n"
            f"  1. Attend our membership class, held quarterly\n"
            f"  2. Join one of our cell groups in your area\n"
            f"  3. Explore our various ministry opportunities\n\n"
            f"Please do not hesitate to contact the church office if you have any questions "
            f"or needs. We are here for you.\n\n"
            f"May the peace of God, which transcends all understanding, guard your heart "
            f"and mind in Christ Jesus (Philippians 4:7).\n\n"
            f"Yours in Christ,\n\n"
            f"{followup_person}\n"
            f"Pastor, Londiani Worshippers"
        ),
        # Short SMS
        lambda: (
            f"[SMS to {visitor_initials}]\n\n"
            f"Bwana asifiwe! Thanks for visiting Londiani Worshippers. "
            f"{'We pray for safe travels back to ' + loc + '.' if loc != 'Londiani Town' else 'We hope to see you again next Sunday.'} "
            f"Any questions? Call or WhatsApp 07XX-XXX-XXX. God bless! — {followup_person}"
        ),
        # Warm conversational WhatsApp
        lambda: (
            f"[WhatsApp message to {visitor_initials}]\n\n"
            f"Hey there! 👋 This is {followup_person} from Londiani Worshippers. "
            f"Just wanted to say karibu sana for joining us today! "
            f"{'My family and I really enjoyed meeting you after service.' if rng.random() < 0.5 else 'I noticed it was your first time — I hope you felt at home.'} "
            f"We have a small group that meets near {loc} on Tuesday evenings for Bible study and chai. "
            f"It's super casual — would you like to come? No pressure at all! 😊 "
            f"Also, if there's anything you need prayer for, just let me know. "
            f"Mungu akubariki! — {followup_person}"
        ),
        # Follow-up email with next steps
        lambda: (
            f"Subject: Great to meet you at Londiani Worshippers!\n\n"
            f"Hi {visitor_initials},\n\n"
            f"It was wonderful having you at Londiani Worshippers this past Sunday! "
            f"We hope the service encouraged your heart.\n\n"
            f"I wanted to personally follow up and share a few things that might help you settle in:\n\n"
            f"📌 Our Service Times:\n"
            f"   First Service: 7:30 AM | Second Service: 10:00 AM\n\n"
            f"📌 Midweek Activities:\n"
            f"   • Bible Study: Tuesday, 10:00 AM\n"
            f"   • Prayer Meeting: Wednesday, 6:00 PM\n"
            f"   • Youth Alive: Friday, 7:00 PM\n\n"
            f"📌 Connect:\n"
            f"   Join our church WhatsApp group for updates: [Link]\n"
            f"   Church website: [Link]\n\n"
            f"If you have children, our Sunday School programme runs during both services "
            f"and they would love to welcome your kids!\n\n"
            f"Please feel free to reach out anytime. I would love to grab a cup of chai "
            f"and get to know you better.\n\n"
            f"Blessings,\n{followup_person}\nLondiani Worshippers Follow-up Team"
        ),
        # Brief formal SMS
        lambda: (
            f"[SMS to {visitor_initials}]\n\n"
            f"Thank you for visiting Londiani Worshippers. We are praying for you this week. "
            f"Service times: 7:30 AM & 10:00 AM. Office: 052-XXX-XXX. God bless you. "
            f"— {followup_person}"
        ),
        # Friendly WhatsApp with testimony invitation
        lambda: (
            f"[WhatsApp to {visitor_initials}]\n\n"
            f"Karibu at Londiani Worshippers! 🎉 {followup_person} here. "
            f"We're so glad you came! Next Sunday we have a special testimony Sunday — "
            f"members will be sharing what God has done in their lives. It's always powerful! "
            f"Would love to see you there. Services at 7:30 and 10 AM. "
            f"{'If you need directions from ' + loc + ', just ask!' if loc != 'Londiani Town' else ''} "
            f"Asante sana and God bless! 🙏✨"
        ),
        # Pastoral welcome letter
        lambda: (
            f"Dear {visitor_initials},\n\n"
            f"Grace and peace to you from God our Father and the Lord Jesus Christ.\n\n"
            f"I am writing to personally welcome you to Londiani Worshippers. "
            f"Visiting a new church can feel overwhelming, and I want you to know "
            f"that we are genuinely glad you came. You are not a number to us — "
            f"you are a person created in the image of God, and we honour your presence.\n\n"
            f"Our prayer is that you will find Londiani Worshippers to be a place where:\n"
            f"  • You encounter God through His Word and worship\n"
            f"  • You find genuine community and belonging\n"
            f"  • You are equipped to fulfil God's purpose for your life\n\n"
            f"{'I understand you travelled from ' + loc + ' to join us — that speaks of your hunger for God, and He will honour that.' if loc != 'Londiani Town' else ''}\n\n"
            f"I would love to meet you personally. Please introduce yourself after any Sunday service "
            f"or schedule a visit through the church office.\n\n"
            f"Mungu akubariki abundantly.\n\n"
            f"Your pastor,\n{followup_person}\nLondiani Worshippers"
        ),
        # SMS with event invite
        lambda: (
            f"[SMS to {visitor_initials}]\n\n"
            f"Hi from Londiani Worshippers! Great having u with us. "
            f"This Friday we have a special worship night 7pm-9pm at the church. Karibu! "
            f"Questions? WhatsApp {followup_person} at 07XX-XXX-XXX. Bwana asifiwe!"
        ),
        # Welcome card text
        lambda: (
            f"WELCOME CARD — LONDIANI WORSHIPPERS\n\n"
            f"Dear {visitor_initials},\n\n"
            f"We are thrilled that you chose to worship with us!\n\n"
            f"At Londiani Worshippers, we believe:\n"
            f"  ♥ God loves you — John 3:16\n"
            f"  ♥ You have a purpose — Jeremiah 29:11\n"
            f"  ♥ You belong here — Romans 12:5\n\n"
            f"Next Steps:\n"
            f"  □ Fill in a visitor card (available at the information desk)\n"
            f"  □ Attend a newcomers' tea with the pastor\n"
            f"  □ Join a cell group near {loc}\n\n"
            f"Contact: {followup_person} — 07XX-XXX-XXX\n"
            f"Church Office: 052-XXX-XXX\n\n"
            f"Karibu home! 🏠"
        ),
        # Email with resource links
        lambda: (
            f"Subject: Your visit to Londiani Worshippers + Resources Inside\n\n"
            f"Hello {visitor_initials},\n\n"
            f"Thank you for being our guest this past Sunday at Londiani Worshippers. "
            f"We trust you experienced the love of God and the warmth of His people.\n\n"
            f"To help you on your journey, here are some resources:\n\n"
            f"📖 Daily Devotional: [Link — sent every morning via WhatsApp]\n"
            f"🎵 Worship Playlist: [Link — songs from our Sunday service]\n"
            f"📋 Church Calendar: [Link — upcoming events and activities]\n"
            f"🙏 Prayer Requests: Submit via 07XX-XXX-XXX or the prayer wall\n\n"
            f"If you are looking for a church home, we would be honoured to walk with you. "
            f"Our membership class is coming up next month — details to follow.\n\n"
            f"May God bless your week abundantly.\n\n"
            f"In His service,\n{followup_person}\nLondiani Worshippers"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "visitor_welcome_followup",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": followup_person,
            "target_audience": "new visitors",
            "location_tag": loc,
            "language_mix": "English with Swahili phrases" if "Karibu" in raw_text or "akubariki" in raw_text else "primarily English",
            "document_style": channel.lower().replace(" ", "_"),
            "keywords": rng.sample([
                "visitor", "follow-up", "welcome", channel.lower(),
                "newcomer", "connection", loc.split()[0].lower(),
            ], k=rng.randint(4, 6)),
        },
    }
