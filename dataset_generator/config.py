"""Configuration constants and reference data for dataset generation."""

CATEGORIES = [
    "sermon_transcript_snippet",
    "weekly_bulletin_announcement",
    "bible_study_guide",
    "financial_tithe_report",
    "ministry_leader_update",
    "community_outreach_log",
    "facility_booking_request",
    "counseling_intake_summary",
    "prayer_request_wall",
    "sunday_school_curriculum",
    "choir_rehearsal_schedule",
    "church_board_minutes_excerpt",
    "event_calendar_entry",
    "volunteer_roster_notice",
    "visitor_welcome_followup",
]

DOCS_PER_CATEGORY = 15
TOTAL_DOCS = len(CATEGORIES) * DOCS_PER_CATEGORY
CATEGORIES_COUNT = len(CATEGORIES)

# Date range
DATE_START_YEAR = 2022
DATE_END_YEAR = 2026

LOCATIONS = [
    "Londiani Town", "Kipkelion", "Fort Ternan", "Koru", "Kedowa",
    "Chepseon", "Tulwet", "Kipsitet", "Molo Road", "Kericho County",
    "Nakuru County", "Londiani Market", "Londiani Catholic Parish",
    "Londiani District Hospital", "Kipkelion East", "Kipkelion West",
]

LOCAL_CONTEXT = [
    "tea farming", "maize harvest", "dairy farming", "rainy season",
    "planting season", "school opening", "market day", "hospital visit",
    "youth employment", "elderly members", "church construction",
    "water project", "community cleanup", "long rains", "short rains",
    "tea picking season", "milk delivery", "cattle dip", "boda boda",
    "matatu", "shamba", "chama", "harambee", "baraza",
]

SWAHILI_EXPRESSIONS = [
    "Amen", "Karibu", "Mungu akubariki", "Bwana asifiwe",
    "Asante sana", "Tuko pamoja", "Hakuna Mungu kama wewe",
    "Yesu ni Bwana", "Baraka", "Twabariki", "Umoja",
    "Amani", "Tumaini", "Neema", "Rehema",
]

FIRST_NAMES = [
    "Samuel", "Grace", "Peter", "Esther", "John", "Mary", "David",
    "Ruth", "Joshua", "Naomi", "Daniel", "Sarah", "Joseph", "Rebecca",
    "Elijah", "Priscilla", "Isaac", "Deborah", "Solomon", "Lydia",
    "Moses", "Hannah", "Aaron", "Miriam", "Ezekiel", "Martha",
    "Philip", "Dorcas", "Stephen", "Lois", "James", "Eunice",
    "Thomas", "Rhoda", "Andrew", "Persis", "Mark", "Tryphena",
    "Luke", "Julia", "Paul", "Drusilla", "Timothy", "Phoebe",
    "Silas", "Tabitha", "Barnabas", "Sapphira", "Matthias", "Junia",
    "Kipruto", "Chebet", "Kipng'etich", "Jepkosgei", "Koech",
    "Cherono", "Bett", "Chemutai", "Rono", "Jeptoo",
    "Kigen", "Chepchumba", "Tanui", "Kosgei", "Sigilai",
]

LAST_NAMES = [
    "Kiprono", "Cheruiyot", "Rotich", "Kurgat", "Koech",
    "Bett", "Ruto", "Kipkemoi", "Langat", "Kiptoo",
    "Kemboi", "Sang", "Kiprop", "Maiyo", "Kiptanui",
    "Koskei", "Too", "Mitei", "Chepkwony", "Ng'eno",
    "Kigen", "Kilel", "Korir", "Kimutai", "Cheboi",
    "Muge", "Tum", "Sigei", "Kibiwott", "Kipchumba",
    "Odhiambo", "Ochieng", "Omondi", "Otieno", "Akinyi",
    "Wanjiku", "Muthoni", "Kamau", "Njoroge", "Waweru",
    "Kimani", "Mwangi", "Maina", "Githinji", "Chege",
]

MINISTRY_NAMES = [
    "Youth Ministry", "Women's Guild", "Men's Fellowship", "Choir",
    "Hospitality Ministry", "Children's Ministry", "Evangelism Team",
    "Prayer Team", "Media Ministry", "Ushering Team", "Couples' Fellowship",
    "Singles' Ministry", "Senior Citizens' Ministry", "Missions Committee",
    "Discipleship Team", "Worship Team", "Technical Team", "Drama Ministry",
]

VOLUNTEER_TEAMS = [
    "Ushers", "Media", "Security", "Hospitality", "Parking",
    "Worship", "Prayer", "Protocol", "First Aid", "Decoration",
    "Sound", "Children's Church", "Translation", "Offering", "Follow-up",
]

BOOKS_OT = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
]

BOOKS_NT = [
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
    "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation",
]

SONG_TITLES = [
    "Amazing Grace", "How Great Thou Art", "It Is Well With My Soul",
    "Blessed Assurance", "Holy Holy Holy", "Come Thou Fount",
    "Great Is Thy Faithfulness", "In Christ Alone", "Be Thou My Vision",
    "Praise Father", "Mungu Ni Mwema", "Hakuna Mungu Kama Wewe",
    "Yesu Nakupenda", "Sifa Zako", "Bwana Ni Mchungaji Wangu",
    "Uliniwezesha", "Nimeinuliwa", "Wastahili Sifa", "Moyo Wangu Uko Tayari",
    "Before the Throne", "What a Friend We Have in Jesus",
    "Standing on the Promises", "To God Be the Glory",
    "Crown Him with Many Crowns", "All Hail the Power",
    "Victory in Jesus", "Turn Your Eyes Upon Jesus",
    "Leaning on the Everlasting Arms", "A Mighty Fortress",
    "Fairest Lord Jesus", "My Hope Is Built",
    "Rock of Ages", "When I Survey", "Abide with Me",
    "Guide Me O Thou Great Jehovah", "Be Still and Know",
    "Shine Jesus Shine", "Lord I Lift Your Name on High",
    "Open the Eyes of My Heart", "Shout to the Lord",
    "Here I Am to Worship", "Forever",
]

VENUES = [
    "Main Sanctuary", "Fellowship Hall", "Youth Centre", "Church Compound",
    "Pastor's Office", "Conference Room A", "Conference Room B",
    "Sunday School Block", "Kitchen Hall", "Prayer Room",
    "Outdoor Pergola", "Church Verandah", "Londiani Community Hall",
    "Kipkelion Parish Hall", "Chepseon Meeting Room",
]
