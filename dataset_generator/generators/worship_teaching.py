"""Generators for worship and teaching categories."""

import random

from dataset_generator import config
from dataset_generator import utils
from dataset_generator.tracker import UniquenessTracker


def gen_sermon_transcript_snippet(idx, rng, tracker):
    pastor_names = [
        "Rev. Samuel Kiprono", "Pastor Grace Cheruiyot", "Bishop David Rotich",
        "Pastor Esther Kurgat", "Rev. Joshua Koech", "Pastor Naomi Bett",
        "Pastor Elijah Ruto", "Rev. Priscilla Kipkemoi", "Pastor Daniel Langat",
        "Pastor Ruth Kiptoo", "Rev. Isaac Kemboi", "Pastor Deborah Sang",
        "Pastor Solomon Kiprop", "Rev. Lydia Maiyo", "Pastor Miriam Kiptanui",
    ]
    pastor = pastor_names[idx % len(pastor_names)]
    tracker.add_name(pastor)

    scripture1 = utils.random_scripture(rng)
    tracker.add_scripture(scripture1)
    scripture2 = utils.random_scripture(rng)
    while scripture2 in tracker.used_scriptures:
        scripture2 = utils.random_scripture(rng)
    tracker.add_scripture(scripture2)

    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.6)
    swahili = utils.maybe_swahili(rng, 0.2)

    structures = [
        lambda: (
            f"{swahili}Turn with me to {scripture1}. "
            f"When we read this passage, we see a God who does not abandon His people. "
            f"Someone in the back says 'Amen!' and I agree with you, brother. "
            f"You know, last week I was visiting a family near {loc}, "
            f"and they told me how the Lord provided during the {context or 'difficult season'}. "
            f"{"The " + context + " had made things very hard for them, yet they testified of God's faithfulness." if context else "Things were difficult, yet they testified of God's faithfulness."} "
            f"\n\n\"{scripture2}\" let that sink in for a moment. "
            f"The congregation responds: \"Bwana asifiwe!\" "
            f"\n\nLet me ask you: when was the last time you trusted God in the middle of a storm? "
            f"Not after the storm. In the storm. "
            f"There is a difference between praising God on the mountain "
            f"and trusting Him in the valley. {swahili}Let us pray. "
            f"Father, we come before You with hearts that are willing but sometimes weak. "
            f"Strengthen us. Help us to trust Your Word even when our circumstances shout otherwise. "
            f"In Jesus' name we pray. Amen."
        ),
        lambda: (
            f"Good morning, Londiani Worshippers! {swahili}"
            f"Before I read the text, let me tell you a story. "
            f"There was a farmer in {loc} who planted his maize right before the "
            f"{'long rains failed' if context == 'rainy season' else context + ' brought challenges' if context else 'drought came'}. "
            f"His neighbours laughed. But he said, 'My God will provide.' "
            f"And He did not the way the farmer expected, but He did. "
            f"\n\nNow, {scripture1}. "
            f"This is not just a verse for Sunday. This is a verse for Monday morning "
            f"when the children need school fees and the shamba has not produced enough. "
            f"This is a verse for the hospital bedside. "
            f"This is a verse for the marriage that feels like it is crumbling. "
            f"\n\nPaul writes in {scripture2} that nothing can separate us from the love of God. "
            f"Nothing. Not unemployment. Not sickness. Not even our own doubts. "
            f"Mungu akubariki, church! Will you believe that today? "
            f"Shout it out if you believe it! [Congregation: Amen!] "
            f"Practical application: I want every family here to write down one promise "
            f"from Scripture and put it on your doorpost this week. "
            f"Let the Word of God be the first thing you see every morning. Amen."
        ),
        lambda: (
            f"{swahili}Our text today is found in {scripture1}. "
            f"I want to share three truths from this passage. "
            f"\n\nFirst: God sees you. Even in {loc}, even in your small prayer corner, "
            f"He sees you. Hagar called Him 'El Roi' the God who sees. "
            f"\n\nSecond: God hears you. {'I know some of you are praying about the ' + context + '.' if context else 'I know some of you have been praying for a long time.'} "
            f"Do not give up. {scripture2} reminds us that our prayers are not wasted. "
            f"\n\nThird: God will answer. Not always the way we expect. "
            f"Sometimes the answer is 'yes', sometimes 'wait', sometimes 'I have something better'. "
            f"But He answers. "
            f"\n\nNow I want us to take a moment of silence. "
            f"[Pause] "
            f"Whatever you are carrying today lay it at the feet of Jesus. "
            f"Shall we pray together? Father, You are our refuge and strength, "
            f"an ever-present help in trouble. We trust You. We lean on You. "
            f"Bwana asifiwe. In the mighty name of Jesus, amen."
        ),
    ]

    raw_text = structures[idx % len(structures)]()

    styles = ["expository", "narrative", "devotional", "pastoral", "topical"]
    audiences = ["congregation", "church members", "believers", "parishioners", "worship community"]
    language_mixes = ["primarily English", "English with Swahili phrases", "English with occasional Swahili"]

    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "sermon_transcript_snippet",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": pastor,
            "target_audience": utils.pick(audiences, rng),
            "location_tag": loc,
            "language_mix": utils.pick(language_mixes, rng),
            "document_style": utils.pick(styles, rng),
            "keywords": rng.sample([
                "sermon", "preaching", scripture1.split()[0].lower(),
                "faith", "trust", "prayer", "application", "teaching",
                loc.split()[0].lower() if loc.split() else "londiani",
            ], k=rng.randint(4, 7)),
        },
    }


def gen_bible_study_guide(idx, rng, tracker):
    facilitators = utils.generate_unique_names(15, rng)
    scripture_main = utils.random_scripture_range(rng)
    tracker.add_scripture(scripture_main)
    memory_verse = utils.random_scripture(rng)
    while memory_verse in tracker.used_scriptures:
        memory_verse = utils.random_scripture(rng)
    tracker.add_scripture(memory_verse)

    loc = utils.pick(config.LOCATIONS, rng)
    context = utils.maybe_local_context(rng, 0.4)
    swahili = utils.maybe_swahili(rng, 0.12)

    topics = [
        ("Walking in Faith During Uncertain Times", "faith", "believers"),
        ("The Power of Persistent Prayer", "prayer", "prayer warriors"),
        ("Forgiveness: Setting Yourself Free", "forgiveness", "all members"),
        ("God's Provision in Seasons of Need", "provision", "families"),
        ("Building Strong Marriages God's Way", "marriage", "couples"),
        ("Overcoming Fear with God's Word", "fear", "youth and adults"),
        ("The Fruit of the Spirit in Daily Life", "fruit of the Spirit", "disciples"),
        ("Serving Others: The Heart of Ministry", "service", "ministry leaders"),
        ("Finding Purpose in Your Wilderness Season", "purpose", "young adults"),
        ("Standing on God's Promises", "promises", "church community"),
        ("The Armor of God: Spiritual Warfare", "spiritual warfare", "believers"),
        ("Contentment in Every Circumstance", "contentment", "all members"),
        ("Hearing God's Voice in a Noisy World", "discernment", "seekers"),
        ("Generosity: Living with Open Hands", "generosity", "givers"),
        ("Restoring Broken Relationships", "restoration", "families and couples"),
    ]

    topic, theme, audience = topics[idx % len(topics)]
    facilitator = facilitators[idx % len(facilitators)]

    templates = [
        lambda: (
            f"📖 BIBLE STUDY GUIDE\n"
            f"Topic: {topic}\n"
            f"Main Text: {scripture_main}\n"
            f"Memory Verse: {memory_verse}\n"
            f"Facilitator: {facilitator}\n"
            f"{'=' * 50}\n\n"
            f"OBJECTIVES:\n"
            f"By the end of this study, participants should be able to:\n"
            f"  1. Explain what the Bible teaches about {theme}\n"
            f"  2. Identify practical ways to apply the lesson in daily life\n"
            f"  3. Encourage one another through Scripture-based discussion\n\n"
            f"INTRODUCTION:\n"
            f"{swahili}As we open God's Word today, let us remember that "
            f"the Bible is not just an ancient book it is a living word "
            f"that speaks to our present situation. "
            f"{'Many of us in ' + loc + ' are facing challenges related to the ' + context + '.' if context else 'Each of us carries a burden that only God can lighten.'} "
            f"But God's truth remains our anchor.\n\n"
            f"SCRIPTURE READING:\n"
            f"Read {scripture_main} aloud together. Take turns verse by verse.\n\n"
            f"DISCUSSION QUESTIONS:\n"
            f"  i.   What stands out to you most from this passage?\n"
            f"  ii.  How does this text challenge our understanding of {theme}?\n"
            f"  iii. Can you share a personal experience related to this topic?\n"
            f"  iv.  What specific action will you take this week based on this study?\n\n"
            f"REFLECTION PROMPT:\n"
            f"Spend 5 minutes in silent meditation on {memory_verse}. "
            f"Write down one insight the Holy Spirit gives you.\n\n"
            f"CLOSING PRAYER:\n"
            f"Lord, help us to be doers of Your Word and not hearers only. "
            f"May the truth we have learned today transform our hearts and actions. "
            f"In Jesus' name. Amen."
        ),
        lambda: (
            f"BIBLE STUDY — {topic.upper()}\n\n"
            f"Passage: {scripture_main}\n"
            f"Memory Verse: {memory_verse}\n\n"
            f"Welcome, friends! {swahili}Today we dive into one of the most "
            f"practical topics in the Christian walk: {theme}.\n\n"
            f"STUDY OBJECTIVE:\n"
            f"To understand how God's Word guides us in {theme}, "
            f"and to leave this session with at least one concrete step of obedience.\n\n"
            f"WARM-UP QUESTION:\n"
            f"Think about your life this past week. Where did you see God at work?\n"
            f"(Share in pairs for 3 minutes)\n\n"
            f"READ & REFLECT:\n"
            f"  • Read {scripture_main} slowly\n"
            f"  • Underline words or phrases that the Holy Spirit highlights to you\n"
            f"  • Discuss in your small group\n\n"
            f"KEY QUESTIONS:\n"
            f"  1. What does this passage reveal about God's character?\n"
            f"  2. What does it reveal about human nature?\n"
            f"  3. What command or promise do we find here?\n"
            f"  4. How does this apply to our context in {loc}?\n"
            f"  {'5. How does the ' + context + ' season affect our trust in God?' if context else '5. What practical step will you take this week?'}\n\n"
            f"MEMORY VERSE CHALLENGE:\n"
            f"\"{memory_verse}\" Can you memorize this by next week?\n\n"
            f"PRAYER:\n"
            f"Father, open our eyes that we may see wonderful things from Your law. "
            f"Amen. See you next Wednesday!"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "bible_study_guide",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": facilitator,
            "target_audience": audience,
            "location_tag": loc,
            "language_mix": "primarily English",
            "document_style": "instructional",
            "keywords": rng.sample([
                "bible study", theme, "scripture", "discussion",
                "reflection", "memory verse", loc.split()[0].lower(),
            ], k=rng.randint(4, 7)),
        },
    }


def gen_sunday_school_curriculum(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    age_groups = [
        "3-5 years (Nursery)", "6-8 years (Lower Primary)", "9-11 years (Upper Primary)",
        "12-14 years (Junior Teens)", "3-5 years (Nursery)", "6-8 years (Lower Primary)",
        "9-11 years (Upper Primary)", "12-14 years (Junior Teens)",
        "3-5 years (Nursery)", "6-8 years (Lower Primary)",
        "9-11 years (Upper Primary)", "12-14 years (Junior Teens)",
        "3-5 years (Nursery)", "6-8 years (Lower Primary)", "9-11 years (Upper Primary)",
    ]

    bible_stories = [
        ("Creation — God Made the World", "Genesis 1:1-31",
         "Children will learn that God created everything and it was good.",
         "Genesis 1:1 — 'In the beginning God created the heavens and the earth.'",
         "Creation collage: Draw or paste pictures of things God made on a big poster"),
        ("Noah's Ark — Trusting God in the Storm", "Genesis 6:9-22",
         "Children will understand that obeying God brings safety even when others doubt.",
         "Genesis 7:16 — 'Then the Lord shut him in.'",
         "Ark craft: Build a small ark using cardboard boxes and toy animals"),
        ("David and Goliath — Courage from God", "1 Samuel 17:1-50",
         "Children will learn that with God, even the smallest person can face big challenges.",
         "1 Samuel 17:45 — 'You come against me with sword but I come against you in the name of the Lord.'",
         "Slingshot craft: Make a simple slingshot from string and cardboard circles"),
        ("The Birth of Jesus — God's Greatest Gift", "Luke 2:1-20",
         "Children will celebrate that Jesus is God's gift to the world.",
         "Luke 2:11 — 'Today in the town of David a Saviour has been born to you.'",
         "Nativity scene: Colour and arrange nativity figures on a display board"),
        ("The Good Samaritan — Loving Your Neighbour", "Luke 10:25-37",
         "Children will learn that everyone is our neighbour and we should show kindness.",
         "Luke 10:27 — 'Love your neighbour as yourself.'",
         "Neighbourhood map: Draw a map of your neighbourhood and mark ways to help others"),
        ("Jonah and the Big Fish — Running from God", "Jonah 1-4",
         "Children will understand that we cannot hide from God and should obey Him.",
         "Jonah 2:2 — 'In my distress I called to the Lord, and He answered me.'",
         "Big fish puppet: Make a whale puppet from a paper bag and retell the story"),
        ("Feeding the 5,000 — Sharing What We Have", "John 6:1-14",
         "Children will learn that God can multiply our small offerings when we give generously.",
         "John 6:11 — 'Jesus then took the loaves, gave thanks, and distributed.'",
         "Bread basket: Make a paper basket with five loaves and two fish cutouts"),
        ("Daniel in the Lions' Den — Faithful Prayer", "Daniel 6:1-23",
         "Children will learn the importance of praying faithfully even when it is difficult.",
         "Daniel 6:10 — 'Three times a day he got down on his knees and prayed.'",
         "Lion mask: Create lion masks from paper plates and yarn"),
        ("The Lost Sheep — God Never Gives Up on Us", "Luke 15:1-7",
         "Children will understand that God loves each one of us and searches for us when we wander.",
         "Luke 15:6 — 'Rejoice with me; I have found my lost sheep.'",
         "Cotton ball sheep: Make sheep from cotton balls and construction paper"),
        ("Peter Walks on Water — Keeping Our Eyes on Jesus", "Matthew 14:22-33",
         "Children will learn to trust Jesus even when circumstances are frightening.",
         "Matthew 14:29 — 'Come, he said. Then Peter got down out of the boat and walked on the water.'",
         "Water scene: Create a diorama of the storm and Peter walking on water"),
        ("Ruth and Naomi — Loyalty and Love", "Ruth 1-4",
         "Children will learn about loyalty, kindness, and how God provides through relationships.",
         "Ruth 1:16 — 'Where you go I will go, and where you stay I will stay.'",
         "Wheat craft: Make wheat bundles from straw or paper strips"),
        ("The Wise and Foolish Builders — Building on the Rock", "Matthew 7:24-27",
         "Children will understand that obeying Jesus' words is like building a house on solid rock.",
         "Matthew 7:24 — 'Everyone who hears these words of mine and puts them into practice is like a wise man.'",
         "House on rock: Build two houses one on sand, one on a rock and test with water"),
        ("Joseph's Colourful Coat — God's Plan Even in Hard Times", "Genesis 37-50",
         "Children will learn that God has a plan even when things go wrong.",
         "Genesis 50:20 — 'You intended to harm me, but God intended it for good.'",
         "Colourful coat: Decorate a coat shape with strips of coloured paper"),
        ("The Prodigal Son — Coming Home to God", "Luke 15:11-32",
         "Children will understand that God always welcomes us back with open arms.",
         "Luke 15:20 — 'While he was still a long way off, his father saw him and was filled with compassion.'",
         "Welcome sign: Make a 'Welcome Home' banner and role-play the story"),
        ("Moses and the Burning Bush — Answering God's Call", "Exodus 3:1-22",
         "Children will learn that God calls ordinary people for extraordinary purposes.",
         "Exodus 3:12 — 'I will be with you.'",
         "Burning bush: Create a bush from twigs with tissue paper flames"),
    ]

    age = age_groups[idx % len(age_groups)]
    story, scripture, objective, memory_verse, craft = bible_stories[idx % len(bible_stories)]
    teacher = utils.random_name(rng)

    templates = [
        lambda: (
            f"SUNDAY SCHOOL LESSON PLAN\n"
            f"{'=' * 50}\n"
            f"Age Group: {age}\n"
            f"Lesson Title: {story}\n"
            f"Scripture: {scripture}\n"
            f"Teacher: {teacher}\n"
            f"{'=' * 50}\n\n"
            f"LESSON OBJECTIVE:\n"
            f"{objective}\n\n"
            f"BIBLE STORY:\n"
            f"Read {scripture} from a children's Bible. Tell the story in your own words, "
            f"using simple language. Ask questions along the way to keep children engaged.\n\n"
            f"Key points to emphasise:\n"
            f"  1. God is powerful and loving\n"
            f"  2. We can trust God in every situation\n"
            f"  3. God has a plan for each of us\n\n"
            f"MEMORY VERSE:\n"
            f"{memory_verse}\n"
            f"Tip: Say it together three times. Use hand motions if possible.\n\n"
            f"CRAFT / ACTIVITY:\n"
            f"{craft}\n"
            f"Materials needed: Scissors, glue, coloured paper, markers\n"
            f"Time: 15-20 minutes\n\n"
            f"CLOSING PRAYER:\n"
            f"Dear Jesus, thank You for this story from Your Word. "
            f"Help us to remember what we learned today and to live it out this week. "
            f"Amen.\n\n"
            f"TEACHER NOTE:\n"
            f"{"Relate the story to the children's lives in " + loc + "." if loc != 'Londiani Town' else 'Use examples the children can relate to from their daily lives.'} "
            f"For example, when talking about God providing, you might mention "
            f"how God gives us rain for the maize and grass for the cows."
        ),
        lambda: (
            f"📖 Children's Ministry — Lesson of the Week\n\n"
            f"Class: {age}\n"
            f"Story: {story}\n"
            f"Text: {scripture}\n\n"
            f"WHAT WE'RE LEARNING:\n"
            f"{objective}\n\n"
            f"LET'S READ TOGETHER:\n"
            f"Open your Bibles to {scripture}. (For younger children, use the picture Bible.)\n\n"
            f"TALK ABOUT IT:\n"
            f"  • What happened in this story?\n"
            f"  • How did the people feel?\n"
            f"  • What does this teach us about God?\n"
            f"  • What should we do because of what we learned?\n\n"
            f"MEMORY VERSE CHALLENGE:\n"
            f"{memory_verse}\n"
            f"Can you say it by yourself next Sunday? 🌟\n\n"
            f"FUN ACTIVITY:\n"
            f"{craft}\n\n"
            f"CLOSING:\n"
            f"Let us pray: Thank You, God, for loving us and for this story. "
            f"Help us to be brave, kind, and obedient like the people in the Bible. "
            f"In Jesus' name, amen! 🙏\n\n"
            f"— {teacher}, Sunday School Teacher"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "sunday_school_curriculum",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": teacher,
            "target_audience": f"children aged {age}",
            "location_tag": loc,
            "language_mix": "primarily English",
            "document_style": "lesson_plan",
            "keywords": rng.sample([
                "sunday school", "curriculum", story.lower().split("—")[0].strip().lower() if "—" in story else story.lower().split()[0],
                "bible story", "children", "craft", "memory verse",
            ], k=rng.randint(4, 7)),
        },
    }


def gen_choir_rehearsal_schedule(idx, rng, tracker):
    loc = utils.pick(config.LOCATIONS, rng)
    choir_master = utils.random_name(rng)
    tracker.add_name(choir_master)

    song_sets = [utils.pick_unique(config.SONG_TITLES, 5, rng) for _ in range(5)]
    current_songs = song_sets[idx % len(song_sets)]

    venues = ["Main Sanctuary", "Fellowship Hall", "Youth Centre", "Church Compound", "Conference Room A"]
    venue = utils.pick(venues, rng)
    alt_venue = utils.pick([v for v in venues if v != venue], rng)

    voice_sections = ["Soprano", "Alto", "Tenor", "Bass"]
    featured_sections = utils.pick_unique(voice_sections, 2, rng)

    uniform_options = [
        "White robe with blue sash", "Church choir uniform (navy and white)",
        "African print kitenge", "All black with gold accessories",
        "White shirt/blouse and black skirt/trousers",
        "Choir robes (maroon)", "Casual smart matching colours to be confirmed",
    ]

    templates = [
        lambda: (
            f"CHOIR REHEARSAL SCHEDULE\n"
            f"Londiani Worshippers Voices of Praise\n"
            f"{'=' * 55}\n\n"
            f"Choir Director: {choir_master}\n\n"
            f"WEEKLY REHEARSAL TIMES:\n"
            f"  Tuesday:    5:30 PM - 7:30 PM  ({venue})\n"
            f"  Thursday:   5:30 PM - 7:30 PM  ({venue})\n"
            f"  Saturday:   9:00 AM - 12:00 PM (Full rehearsal, {alt_venue if rng.random() < 0.5 else venue})\n"
            f"  Sunday:     7:00 AM (Warm-up before first service)\n\n"
            f"CURRENT SONG LIST:\n"
            f"  1. {current_songs[0]}\n"
            f"  2. {current_songs[1]}\n"
            f"  3. {current_songs[2]}\n"
            f"  4. {current_songs[3]}\n"
            f"  5. {current_songs[4]}\n\n"
            f"VOICE SECTION FOCUS THIS WEEK:\n"
            f"  → {featured_sections[0]}: New harmonies for songs 2 & 4\n"
            f"  → {featured_sections[1]}: Strengthening blend and dynamics\n\n"
            f"UNIFORM:\n"
            f"  This Sunday: {utils.pick(uniform_options, rng)}\n"
            f"  Please ensure uniforms are clean and pressed.\n\n"
            f"NOTES:\n"
            f"  • All members must attend at least 2 rehearsals per week\n"
            f"  • New members welcome audition with {choir_master} on Saturdays\n"
            f"  • {'Saturday rehearsal venue changed to ' + alt_venue + ' this week due to another event.' if rng.random() < 0.4 else ''}\n"
            f"  • Please arrive 10 minutes early for warm-up\n\n"
            f"Bwana asifiwe! Let us sing unto the Lord!\n— {choir_master}"
        ),
        lambda: (
            f"🎵 VOICES OF PRAISE — Rehearsal Notice 🎵\n\n"
            f"Hi Choir Family!\n\n"
            f"Here's our schedule for the coming week:\n\n"
            f"THU 5:30 PM — Sectional rehearsals\n"
            f"  • {featured_sections[0]} and {featured_sections[1]} in the {venue}\n"
            f"  • Other sections: individual practice at home\n\n"
            f"SAT 9:00 AM — Full rehearsal\n"
            f"  • Run-through of all 5 songs\n"
            f"  •{' Venue: ' + alt_venue + ' (NOT the usual place!)' if rng.random() < 0.3 else ' Venue: ' + venue}\n\n"
            f"SONGS:\n"
            f"  1. {current_songs[0]}\n"
            f"  2. {current_songs[1]}\n"
            f"  3. {current_songs[2]}\n"
            f"  4. {current_songs[3]}\n"
            f"  5. {current_songs[4]}\n\n"
            f"SUNDAY: Arrive by 7:00 AM for sound check.\n"
            f"Uniform: {utils.pick(uniform_options, rng)}\n\n"
            f"Important:\n"
            f"  ⚠ Attendance is mandatory for Sunday ministration. "
            f"If you cannot make it, please inform {choir_master} by Friday.\n\n"
            f"Karibu to any new members interested in joining!\n\n"
            f"— {choir_master}, Choir Director"
        ),
    ]

    raw_text = templates[idx % len(templates)]()
    return {
        "id": f"LW-{idx + 1:04d}",
        "category": "choir_rehearsal_schedule",
        "timestamp": utils.random_timestamp(rng),
        "raw_text": raw_text,
        "inferred_metadata": {
            "author": choir_master,
            "target_audience": "choir members",
            "location_tag": loc,
            "language_mix": "primarily English",
            "document_style": "schedule",
            "keywords": rng.sample([
                "choir", "rehearsal", "schedule", "songs", "voice sections",
                "uniform", featured_sections[0].lower(),
            ], k=rng.randint(4, 7)),
        },
    }
