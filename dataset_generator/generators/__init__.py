"""Generator registry mapping categories to their respective functions."""

from dataset_generator.generators.worship_teaching import (
    gen_sermon_transcript_snippet,
    gen_bible_study_guide,
    gen_sunday_school_curriculum,
    gen_choir_rehearsal_schedule,
)

from dataset_generator.generators.admin_planning import (
    gen_weekly_bulletin_announcement,
    gen_financial_tithe_report,
    gen_church_board_minutes_excerpt,
    gen_event_calendar_entry,
    gen_facility_booking_request,
    gen_volunteer_roster_notice,
)

from dataset_generator.generators.community_care import (
    gen_ministry_leader_update,
    gen_community_outreach_log,
    gen_counseling_intake_summary,
    gen_prayer_request_wall,
    gen_visitor_welcome_followup,
)

GENERATORS = {
    "sermon_transcript_snippet": gen_sermon_transcript_snippet,
    "weekly_bulletin_announcement": gen_weekly_bulletin_announcement,
    "bible_study_guide": gen_bible_study_guide,
    "financial_tithe_report": gen_financial_tithe_report,
    "ministry_leader_update": gen_ministry_leader_update,
    "community_outreach_log": gen_community_outreach_log,
    "facility_booking_request": gen_facility_booking_request,
    "counseling_intake_summary": gen_counseling_intake_summary,
    "prayer_request_wall": gen_prayer_request_wall,
    "sunday_school_curriculum": gen_sunday_school_curriculum,
    "choir_rehearsal_schedule": gen_choir_rehearsal_schedule,
    "church_board_minutes_excerpt": gen_church_board_minutes_excerpt,
    "event_calendar_entry": gen_event_calendar_entry,
    "volunteer_roster_notice": gen_volunteer_roster_notice,
    "visitor_welcome_followup": gen_visitor_welcome_followup,
}
