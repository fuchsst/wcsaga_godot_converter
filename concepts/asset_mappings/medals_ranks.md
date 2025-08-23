# Medals and Ranks Asset Mapping

## Overview
This document maps the medal and rank definitions from medals.tbl and rank.tbl to their corresponding visual and textual assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### Medal Definitions (.tbl)
Medals.tbl defines military decorations and awards:
- Campaign medals
- Service medals
- Achievement medals
- Valor medals
- Special commendations
- Unit citations
- Meritorious service awards
- Honor guard distinctions

Each medal entry contains:
- Medal name and description
- Award criteria and prerequisites
- Visual representation references
- Audio announcement references
- Textual description references
- Unlock conditions and restrictions

Common medal types:
- Bronze Star - Basic service recognition
- Silver Star - Meritorious achievement
- Gold Star - Exceptional valor
- Distinguished Service Medal - Outstanding leadership
- Legion of Honor - Highest military honor
- Purple Heart - Wounded in action
- Air Medal - Combat flight excellence
- Navy Cross - Naval heroism
- Congressional Medal of Honor - Ultimate sacrifice/heroism
- Special commendations for specific actions

### Rank Definitions (.tbl)
Rank.tbl defines military rank structure:
- Enlisted ranks (E-1 through E-9)
- Petty officer ranks (E-4 through E-9)
- Chief petty officer ranks (E-7 through E-9)
- Warrant officer ranks (W-1 through W-5)
- Commissioned officer ranks (O-1 through O-10)
- Flag officer ranks (O-7 through O-10)

Each rank entry contains:
- Rank title and abbreviation
- Rank insignia references
- Promotion requirements
- Salary/pay grade information
- Authority level definitions
- Responsibility scope descriptions
- Eligibility criteria

### Visual Assets (.pcx/.png)
Medal and rank visual representations:
- Medal icons and full-size images
- Rank insignia graphics
- Certificate background designs
- Presentation ceremony graphics
- UI display elements for medals/ranks
- Inventory screen representations
- Award ceremony animations
- Promotion ceremony graphics

### Audio Assets (.wav/.ogg)
Sound effects for medals and ranks:
- Medal award ceremony sounds
- Rank promotion announcement sounds
- Insignia pinning ceremonies
- Certificate presentation sounds
- Achievement unlock jingles
- Milestone celebration sounds
- Voice announcements for awards
- Military band fanfare music

### Text Assets (.txt)
Descriptive text for medals and ranks:
- Medal citation text
- Rank description text
- Award criteria explanations
- Historical significance information
- Recipient eligibility details
- Ceremony script text
- Presentation speech content
- Achievement unlock messages

## Target Structure
```
/data/medals/                        # Medal data definitions
├── terran/                          # Terran Confederation medals
│   ├── campaign/                    # Campaign-specific medals
│   │   ├── hermes/                  # Hermes campaign medals
│   │   │   ├── bronze_star.tres     # Bronze Star medal
│   │   │   ├── silver_star.tres     # Silver Star medal
│   │   │   ├── gold_star.tres       # Gold Star medal
│   │   │   ├── distinguished_service.tres # Distinguished Service Medal
│   │   │   ├── legion_of_honor.tres  # Legion of Honor
│   │   │   ├── purple_heart.tres    # Purple Heart
│   │   │   ├── air_medal.tres       # Air Medal
│   │   │   ├── navy_cross.tres      # Navy Cross
│   │   │   └── congressional_medal.tres # Congressional Medal of Honor
│   │   └── ...                      # Additional campaigns
│   ├── service/                     # Service branch medals
│   │   ├── navy/                    # Navy medals
│   │   ├── marines/                 # Marine medals
│   │   ├── air_force/               # Air Force medals
│   │   └── special_forces/          # Special Forces medals
│   ├── achievement/                 # Achievement-based medals
│   │   ├── kill_counts/             # Kill-based medals
│   │   ├── mission_completion/      # Mission completion medals
│   │   ├── objective_achievement/   # Objective achievement medals
│   │   └── special_achievements/    # Special achievement medals
│   └── valor/                       # Valor-based medals
│       ├── combat_bravery/          # Combat bravery medals
│       ├── rescue_operations/       # Rescue operation medals
│       ├── sacrifice_awards/         # Sacrifice recognition medals
│       └── heroism_recognition/     # Heroism recognition medals
├── kilrathi/                        # Kilrathi Empire medals
│   ├── honor/                       # Honor-based medals
│   ├── courage/                     # Courage-based medals
│   ├── loyalty/                     # Loyalty-based medals
│   ├── strength/                    # Strength-based medals
│   └── glory/                       # Glory-based medals
└── pirate/                          # Pirate faction medals
    ├── infamy/                      # Infamy-based medals
    ├── wealth/                      # Wealth-based medals
    ├── cunning/                     # Cunning-based medals
    └── survival/                    # Survival-based medals

/data/ranks/                         # Rank data definitions
├── terran/                          # Terran Confederation ranks
│   ├── enlisted/                    # Enlisted ranks (E-1 through E-9)
│   │   ├── e1_airman_basic.tres     # Airman Basic (E-1)
│   │   ├── e2_airman.tres           # Airman (E-2)
│   │   ├── e3_airman_first_class.tres # Airman First Class (E-3)
│   │   ├── e4_specialist.tres       # Specialist (E-4)
│   │   ├── e5_staff_sergeant.tres   # Staff Sergeant (E-5)
│   │   ├── e6_technical_sergeant.tres # Technical Sergeant (E-6)
│   │   ├── e7_master_sergeant.tres  # Master Sergeant (E-7)
│   │   ├── e8_senior_master_sergeant.tres # Senior Master Sergeant (E-8)
│   │   └── e9_chief_master_sergeant.tres # Chief Master Sergeant (E-9)
│   ├── petty_officers/              # Petty Officer ranks (E-4 through E-9)
│   │   ├── po3_airman.tres          # Airman (E-4)
│   │   ├── po2_petty_officer_third_class.tres # Petty Officer Third Class (E-5)
│   │   ├── po1_petty_officer_second_class.tres # Petty Officer Second Class (E-6)
│   │   ├── cpo_petty_officer_first_class.tres # Petty Officer First Class (E-7)
│   │   ├── scpo_senior_chief_petty_officer.tres # Senior Chief Petty Officer (E-8)
│   │   └── mcpo_master_chief_petty_officer.tres # Master Chief Petty Officer (E-9)
│   ├── warrant_officers/            # Warrant Officer ranks (W-1 through W-5)
│   │   ├── wo1_warrant_officer_one.tres # Warrant Officer One (W-1)
│   │   ├── cw2_chief_warrant_officer_two.tres # Chief Warrant Officer Two (W-2)
│   │   ├── cw3_chief_warrant_officer_three.tres # Chief Warrant Officer Three (W-3)
│   │   ├── cw4_chief_warrant_officer_four.tres # Chief Warrant Officer Four (W-4)
│   │   └── cw5_chief_warrant_officer_five.tres # Chief Warrant Officer Five (W-5)
│   ├── commissioned_officers/       # Commissioned Officer ranks (O-1 through O-10)
│   │   ├── o1_enisgn.tres           # Ensign (O-1)
│   │   ├── o2_lieutenant_junior_grade.tres # Lieutenant Junior Grade (O-2)
│   │   ├── o3_lieutenant.tres       # Lieutenant (O-3)
│   │   ├── o4_lieutenant_commander.tres # Lieutenant Commander (O-4)
│   │   ├── o5_commander.tres        # Commander (O-5)
│   │   ├── o6_captain.tres          # Captain (O-6)
│   │   ├── o7_rear_admiral_lower_half.tres # Rear Admiral (Lower Half) (O-7)
│   │   ├── o8_rear_admiral_upper_half.tres # Rear Admiral (Upper Half) (O-8)
│   │   ├── o9_vice_admiral.tres      # Vice Admiral (O-9)
│   │   └── o10_admiral.tres         # Admiral (O-10)
│   └── flag_officers/               # Flag Officer ranks (O-7 through O-10)
│       ├── fo1_rear_admiral.tres    # Rear Admiral (O-7)
│       ├── fo2_rear_admiral.tres    # Rear Admiral (O-8)
│       ├── fo3_vice_admiral.tres    # Vice Admiral (O-9)
│       └── fo4_admiral.tres         # Admiral (O-10)
├── kilrathi/                        # Kilrathi Empire ranks
│   ├── warrior_caste/               # Warrior caste ranks
│   ├── laborer_caste/               # Laborer caste ranks
│   ├── artisan_caste/               # Artisan caste ranks
│   ├── scientist_caste/             # Scientist caste ranks
│   └── leader_caste/                # Leader caste ranks
└── pirate/                          # Pirate faction ranks
    ├── crew/                        # Crew member ranks
    ├── officers/                    # Officer ranks
    ├── captains/                    # Captain ranks
    └── admirals/                    # Admiral ranks

/textures/ui/medals/                 # Medal texture directory
├── terran/                          # Terran medal textures
│   ├── icons/                       # Medal icons
│   │   ├── bronze_star.webp         # Bronze Star icon
│   │   ├── silver_star.webp         # Silver Star icon
│   │   ├── gold_star.webp           # Gold Star icon
│   │   ├── distinguished_service.webp # Distinguished Service Medal icon
│   │   ├── legion_of_honor.webp      # Legion of Honor icon
│   │   ├── purple_heart.webp        # Purple Heart icon
│   │   ├── air_medal.webp           # Air Medal icon
│   │   ├── navy_cross.webp          # Navy Cross icon
│   │   └── congressional_medal.webp # Congressional Medal of Honor icon
│   ├── certificates/                # Medal certificates
│   │   ├── bronze_star.webp         # Bronze Star certificate
│   │   ├── silver_star.webp         # Silver Star certificate
│   │   ├── gold_star.webp           # Gold Star certificate
│   │   ├── distinguished_service.webp # Distinguished Service Medal certificate
│   │   ├── legion_of_honor.webp      # Legion of Honor certificate
│   │   ├── purple_heart.webp        # Purple Heart certificate
│   │   ├── air_medal.webp           # Air Medal certificate
│   │   ├── navy_cross.webp          # Navy Cross certificate
│   │   └── congressional_medal.webp # Congressional Medal of Honor certificate
│   └── presentation/                # Medal presentation graphics
│       ├── ceremony_background.webp  # Ceremony background
│       ├── medal_stand.webp          # Medal stand graphics
│       └── presentation_table.webp   # Presentation table graphics
├── kilrathi/                        # Kilrathi medal textures
│   ├── icons/
│   ├── certificates/
│   └── presentation/
└── pirate/                          # Pirate medal textures
    ├── icons/
    ├── certificates/
    └── presentation/

/textures/ui/ranks/                  # Rank texture directory
├── terran/                          # Terran rank textures
│   ├── insignia/                    # Rank insignia graphics
│   │   ├── enlisted/                # Enlisted rank insignia
│   │   │   ├── e1_airman_basic.webp  # Airman Basic insignia
│   │   │   ├── e2_airman.webp        # Airman insignia
│   │   │   ├── e3_airman_first_class.webp # Airman First Class insignia
│   │   │   ├── e4_specialist.webp    # Specialist insignia
│   │   │   ├── e5_staff_sergeant.webp # Staff Sergeant insignia
│   │   │   ├── e6_technical_sergeant.webp # Technical Sergeant insignia
│   │   │   ├── e7_master_sergeant.webp # Master Sergeant insignia
│   │   │   ├── e8_senior_master_sergeant.webp # Senior Master Sergeant insignia
│   │   │   └── e9_chief_master_sergeant.webp # Chief Master Sergeant insignia
│   │   ├── petty_officers/          # Petty Officer insignia
│   │   │   ├── po3_airman.webp       # Airman insignia
│   │   │   ├── po2_petty_officer_third_class.webp # Petty Officer Third Class insignia
│   │   │   ├── po1_petty_officer_second_class.webp # Petty Officer Second Class insignia
│   │   │   ├── cpo_petty_officer_first_class.webp # Petty Officer First Class insignia
│   │   │   ├── scpo_senior_chief_petty_officer.webp # Senior Chief Petty Officer insignia
│   │   │   └── mcpo_master_chief_petty_officer.webp # Master Chief Petty Officer insignia
│   │   ├── warrant_officers/        # Warrant Officer insignia
│   │   │   ├── wo1_warrant_officer_one.webp # Warrant Officer One insignia
│   │   │   ├── cw2_chief_warrant_officer_two.webp # Chief Warrant Officer Two insignia
│   │   │   ├── cw3_chief_warrant_officer_three.webp # Chief Warrant Officer Three insignia
│   │   │   ├── cw4_chief_warrant_officer_four.webp # Chief Warrant Officer Four insignia
│   │   │   └── cw5_chief_warrant_officer_five.webp # Chief Warrant Officer Five insignia
│   │   ├── commissioned_officers/   # Commissioned Officer insignia
│   │   │   ├── o1_enisgn.webp        # Ensign insignia
│   │   │   ├── o2_lieutenant_junior_grade.webp # Lieutenant Junior Grade insignia
│   │   │   ├── o3_lieutenant.webp    # Lieutenant insignia
│   │   │   ├── o4_lieutenant_commander.webp # Lieutenant Commander insignia
│   │   │   ├── o5_commander.webp     # Commander insignia
│   │   │   ├── o6_captain.webp       # Captain insignia
│   │   │   ├── o7_rear_admiral_lower_half.webp # Rear Admiral (Lower Half) insignia
│   │   │   ├── o8_rear_admiral_upper_half.webp # Rear Admiral (Upper Half) insignia
│   │   │   ├── o9_vice_admiral.webp   # Vice Admiral insignia
│   │   │   └── o10_admiral.webp      # Admiral insignia
│   │   └── flag_officers/           # Flag Officer insignia
│   │       ├── fo1_rear_admiral.webp  # Rear Admiral insignia
│   │       ├── fo2_rear_admiral.webp  # Rear Admiral insignia
│   │       ├── fo3_vice_admiral.webp  # Vice Admiral insignia
│   │       └── fo4_admiral.webp       # Admiral insignia
│   ├── certificates/                # Rank certificates
│   │   ├── promotion/               # Promotion certificates
│   │   ├── commissioning/           # Commissioning certificates
│   │   └── retirement/              # Retirement certificates
│   └── presentation/                # Rank presentation graphics
│       ├── ceremony_background.webp  # Ceremony background
│       ├── insignia_stand.webp       # Insignia stand graphics
│       └── presentation_table.webp   # Presentation table graphics
├── kilrathi/                        # Kilrathi rank textures
│   ├── insignia/
│   ├── certificates/
│   └── presentation/
└── pirate/                          # Pirate rank textures
    ├── insignia/
    ├── certificates/
    └── presentation/

/audio/sfx/medals/                   # Medal sound effects directory
├── terran/                          # Terran medal sounds
│   ├── award_ceremony/              # Award ceremony sounds
│   │   ├── medal_pin.ogg            # Medal pinning sound
│   │   ├── applause.ogg             # Audience applause
│   │   ├── fanfare.ogg              # Fanfare music
│   │   └── certificate_present.ogg  # Certificate presentation sound
│   ├── unlock/                      # Medal unlock sounds
│   │   ├── achievement_unlock.ogg   # Achievement unlock jingle
│   │   ├── milestone_reached.ogg    # Milestone reached sound
│   │   └── new_medal.ogg            # New medal acquired sound
│   └── presentation/                # Medal presentation sounds
│       ├── introduction.ogg         # Medal introduction sound
│       ├── description.ogg          # Medal description sound
│       └── citation_read.ogg        # Citation reading sound
├── kilrathi/                        # Kilrathi medal sounds
│   ├── award_ceremony/
│   ├── unlock/
│   └── presentation/
└── pirate/                          # Pirate medal sounds
    ├── award_ceremony/
    ├── unlock/
    └── presentation/

/audio/sfx/ranks/                    # Rank sound effects directory
├── terran/                          # Terran rank sounds
│   ├── promotion_ceremony/          # Promotion ceremony sounds
│   │   ├── insignia_pin.ogg         # Insignia pinning sound
│   │   ├── oath_administration.ogg  # Oath administration sound
│   │   ├── salute.ogg               # Salute sound
│   │   └── ceremony_conclude.ogg    # Ceremony conclusion sound
│   ├── unlock/                      # Rank unlock sounds
│   │   ├── promotion.ogg             # Promotion sound
│   │   ├── new_rank.ogg             # New rank acquired sound
│   │   └── rank_increase.ogg        # Rank increase sound
│   └── presentation/                # Rank presentation sounds
│       ├── introduction.ogg         # Rank introduction sound
│       ├── description.ogg          # Rank description sound
│       └── authority_explanation.ogg # Authority explanation sound
├── kilrathi/                        # Kilrathi rank sounds
│   ├── promotion_ceremony/
│   ├── unlock/
│   └── presentation/
└── pirate/                          # Pirate rank sounds
    ├── promotion_ceremony/
    ├── unlock/
    └── presentation/

/text/medals/                        # Medal text directory
├── terran/                          # Terran medal text
│   ├── descriptions/                # Medal descriptions
│   │   ├── bronze_star.txt          # Bronze Star description
│   │   ├── silver_star.txt          # Silver Star description
│   │   ├── gold_star.txt            # Gold Star description
│   │   ├── distinguished_service.txt # Distinguished Service Medal description
│   │   ├── legion_of_honor.txt       # Legion of Honor description
│   │   ├── purple_heart.txt         # Purple Heart description
│   │   ├── air_medal.txt            # Air Medal description
│   │   ├── navy_cross.txt           # Navy Cross description
│   │   └── congressional_medal.txt  # Congressional Medal of Honor description
│   ├── citations/                   # Medal citations
│   │   ├── bronze_star.txt          # Bronze Star citation
│   │   ├── silver_star.txt          # Silver Star citation
│   │   ├── gold_star.txt            # Gold Star citation
│   │   ├── distinguished_service.txt # Distinguished Service Medal citation
│   │   ├── legion_of_honor.txt       # Legion of Honor citation
│   │   ├── purple_heart.txt         # Purple Heart citation
│   │   ├── air_medal.txt            # Air Medal citation
│   │   ├── navy_cross.txt           # Navy Cross citation
│   │   └── congressional_medal.txt  # Congressional Medal of Honor citation
│   ├── criteria/                    # Award criteria
│   │   ├── bronze_star.txt          # Bronze Star criteria
│   │   ├── silver_star.txt          # Silver Star criteria
│   │   ├── gold_star.txt            # Gold Star criteria
│   │   ├── distinguished_service.txt # Distinguished Service Medal criteria
│   │   ├── legion_of_honor.txt       # Legion of Honor criteria
│   │   ├── purple_heart.txt         # Purple Heart criteria
│   │   ├── air_medal.txt            # Air Medal criteria
│   │   ├── navy_cross.txt           # Navy Cross criteria
│   │   └── congressional_medal.txt  # Congressional Medal of Honor criteria
│   └── ceremony_scripts/            # Ceremony scripts
│       ├── bronze_star.txt          # Bronze Star ceremony script
│       ├── silver_star.txt          # Silver Star ceremony script
│       ├── gold_star.txt            # Gold Star ceremony script
│       ├── distinguished_service.txt # Distinguished Service Medal ceremony script
│       ├── legion_of_honor.txt       # Legion of Honor ceremony script
│       ├── purple_heart.txt         # Purple Heart ceremony script
│       ├── air_medal.txt            # Air Medal ceremony script
│       ├── navy_cross.txt           # Navy Cross ceremony script
│       └── congressional_medal.txt  # Congressional Medal of Honor ceremony script
├── kilrathi/                        # Kilrathi medal text
│   ├── descriptions/
│   ├── citations/
│   ├── criteria/
│   └── ceremony_scripts/
└── pirate/                          # Pirate medal text
    ├── descriptions/
    ├── citations/
    ├── criteria/
    └── ceremony_scripts/

/text/ranks/                         # Rank text directory
├── terran/                          # Terran rank text
│   ├── descriptions/                # Rank descriptions
│   │   ├── enlisted/                # Enlisted rank descriptions
│   │   │   ├── e1_airman_basic.txt   # Airman Basic description
│   │   │   ├── e2_airman.txt         # Airman description
│   │   │   ├── e3_airman_first_class.txt # Airman First Class description
│   │   │   ├── e4_specialist.txt     # Specialist description
│   │   │   ├── e5_staff_sergeant.txt  # Staff Sergeant description
│   │   │   ├── e6_technical_sergeant.txt # Technical Sergeant description
│   │   │   ├── e7_master_sergeant.txt # Master Sergeant description
│   │   │   ├── e8_senior_master_sergeant.txt # Senior Master Sergeant description
│   │   │   └── e9_chief_master_sergeant.txt # Chief Master Sergeant description
│   │   ├── petty_officers/          # Petty Officer descriptions
│   │   │   ├── po3_airman.txt        # Airman description
│   │   │   ├── po2_petty_officer_third_class.txt # Petty Officer Third Class description
│   │   │   ├── po1_petty_officer_second_class.txt # Petty Officer Second Class description
│   │   │   ├── cpo_petty_officer_first_class.txt # Petty Officer First Class description
│   │   │   ├── scpo_senior_chief_petty_officer.txt # Senior Chief Petty Officer description
│   │   │   └── mcpo_master_chief_petty_officer.txt # Master Chief Petty Officer description
│   │   ├── warrant_officers/        # Warrant Officer descriptions
│   │   │   ├── wo1_warrant_officer_one.txt # Warrant Officer One description
│   │   │   ├── cw2_chief_warrant_officer_two.txt # Chief Warrant Officer Two description
│   │   │   ├── cw3_chief_warrant_officer_three.txt # Chief Warrant Officer Three description
│   │   │   ├── cw4_chief_warrant_officer_four.txt # Chief Warrant Officer Four description
│   │   │   └── cw5_chief_warrant_officer_five.txt # Chief Warrant Officer Five description
│   │   ├── commissioned_officers/   # Commissioned Officer descriptions
│   │   │   ├── o1_enisgn.txt         # Ensign description
│   │   │   ├── o2_lieutenant_junior_grade.txt # Lieutenant Junior Grade description
│   │   │   ├── o3_lieutenant.txt     # Lieutenant description
│   │   │   ├── o4_lieutenant_commander.txt # Lieutenant Commander description
│   │   │   ├── o5_commander.txt      # Commander description
│   │   │   ├── o6_captain.txt        # Captain description
│   │   │   ├── o7_rear_admiral_lower_half.txt # Rear Admiral (Lower Half) description
│   │   │   ├── o8_rear_admiral_upper_half.txt # Rear Admiral (Upper Half) description
│   │   │   ├── o9_vice_admiral.txt    # Vice Admiral description
│   │   │   └── o10_admiral.txt       # Admiral description
│   │   └── flag_officers/           # Flag Officer descriptions
│   │       ├── fo1_rear_admiral.txt   # Rear Admiral description
│   │       ├── fo2_rear_admiral.txt   # Rear Admiral description
│   │       ├── fo3_vice_admiral.txt   # Vice Admiral description
│   │       └── fo4_admiral.txt        # Admiral description
│   ├── requirements/                # Rank requirements
│   │   ├── promotion_criteria/      # Promotion criteria
│   │   ├── time_in_grade/           # Time in grade requirements
│   │   ├── performance_standards/   # Performance standards
│   │   └── training_requirements/   # Training requirements
│   ├── responsibilities/            # Rank responsibilities
│   │   ├── authority_levels/        # Authority level definitions
│   │   ├── duty_assignments/        # Duty assignment descriptions
│   │   └── leadership_expectations/ # Leadership expectations
│   └── ceremony_scripts/            # Ceremony scripts
│       ├── enlisted_promotions/     # Enlisted promotion ceremonies
│       ├── officer_commissions/     # Officer commissioning ceremonies
│       └── flag_officer_promotions/ # Flag officer promotion ceremonies
├── kilrathi/                        # Kilrathi rank text
│   ├── descriptions/
│   ├── requirements/
│   ├── responsibilities/
│   └── ceremony_scripts/
└── pirate/                          # Pirate rank text
    ├── descriptions/
    ├── requirements/
    ├── responsibilities/
    └── ceremony_scripts/

/animations/ui/medals/               # Medal animations directory
├── terran/                          # Terran medal animations
│   ├── award_ceremony/              # Award ceremony animations
│   │   ├── medal_presentation.ani   # Medal presentation animation
│   │   ├── certificate_award.ani    # Certificate award animation
│   │   └── applause_reaction.ani    # Applause reaction animation
│   ├── unlock/                      # Medal unlock animations
│   │   ├── achievement_pulse.ani    # Achievement pulse animation
│   │   ├── milestone_glow.ani       # Milestone glow animation
│   │   └── new_medal_spin.ani       # New medal spin animation
│   └── presentation/                # Medal presentation animations
│       ├── introduction_fade.ani    # Introduction fade animation
│       ├── description_scroll.ani   # Description scroll animation
│       └── citation_display.ani     # Citation display animation
├── kilrathi/                        # Kilrathi medal animations
│   ├── award_ceremony/
│   ├── unlock/
│   └── presentation/
└── pirate/                          # Pirate medal animations
    ├── award_ceremony/
    ├── unlock/
    └── presentation/

/animations/ui/ranks/                # Rank animations directory
├── terran/                          # Terran rank animations
│   ├── promotion_ceremony/          # Promotion ceremony animations
│   │   ├── insignia_placement.ani   # Insignia placement animation
│   │   ├── oath_administration.ani  # Oath administration animation
│   │   └── salute_return.ani        # Salute return animation
│   ├── unlock/                      # Rank unlock animations
│   │   ├── promotion_glow.ani       # Promotion glow animation
│   │   ├── new_rank_pulse.ani       # New rank pulse animation
│   │   └── rank_increase_sparkle.ani # Rank increase sparkle animation
│   └── presentation/                # Rank presentation animations
│       ├── introduction_zoom.ani    # Introduction zoom animation
│       ├── description_slide.ani    # Description slide animation
│       └── authority_explain.ani    # Authority explanation animation
├── kilrathi/                        # Kilrathi rank animations
│   ├── promotion_ceremony/
│   ├── unlock/
│   └── presentation/
└── pirate/                          # Pirate rank animations
    ├── promotion_ceremony/
    ├── unlock/
    └── presentation/

/ui/medals/                          # Medal UI directory
├── terran/                          # Terran medal UI
│   ├── inventory/                   # Medal inventory screens
│   │   ├── display/                 # Medal display components
│   │   ├── sorting/                 # Medal sorting controls
│   │   └── filtering/               # Medal filtering controls
│   ├── details/                     # Medal detail screens
│   │   ├── information/             # Medal information panels
│   │   ├── criteria/                # Award criteria panels
│   │   └── history/                 # Award history panels
│   └── ceremony/                    # Medal ceremony screens
│       ├── presentation/            # Presentation screens
│       ├── citation/                # Citation screens
│       └── certificate/             # Certificate screens
├── kilrathi/                        # Kilrathi medal UI
│   ├── inventory/
│   ├── details/
│   └── ceremony/
└── pirate/                          # Pirate medal UI
    ├── inventory/
    ├── details/
    └── ceremony/

/ui/ranks/                           # Rank UI directory
├── terran/                          # Terran rank UI
│   ├── progression/                 # Rank progression screens
│   │   ├── ladder/                  # Rank ladder displays
│   │   ├── requirements/            # Requirement displays
│   │   └── timeline/                # Promotion timeline
│   ├── details/                     # Rank detail screens
│   │   ├── information/             # Rank information panels
│   │   ├── responsibilities/        # Responsibility panels
│   │   └── authority/               # Authority panels
│   └── ceremony/                    # Rank ceremony screens
│       ├── promotion/               # Promotion screens
│       ├── commissioning/           # Commissioning screens
│       └── retirement/              # Retirement screens
├── kilrathi/                        # Kilrathi rank UI
│   ├── progression/
│   ├── details/
│   └── ceremony/
└── pirate/                          # Pirate rank UI
    ├── progression/
    ├── details/
    └── ceremony/
```

## Example Mapping
For Bronze Star Medal:
- medals.tbl entry → /data/medals/terran/campaign/hermes/bronze_star.tres
- bronze_star.pcx → /textures/ui/medals/terran/icons/bronze_star.webp
- bronze_star_certificate.pcx → /textures/ui/medals/terran/certificates/bronze_star.webp
- medal_award_sound.wav → /audio/sfx/medals/terran/award_ceremony/medal_pin.ogg
- bronze_star_description.txt → /text/medals/terran/descriptions/bronze_star.txt
- bronze_star_citation.txt → /text/medals/terran/citations/bronze_star.txt
- bronze_star_criteria.txt → /text/medals/terran/criteria/bronze_star.txt
- medal_presentation.ani → /animations/ui/medals/terran/award_ceremony/medal_presentation.png

For Ensign Rank:
- rank.tbl entry → /data/ranks/terran/enlisted/o1_enisgn.tres
- ensign_insignia.pcx → /textures/ui/ranks/terran/insignia/commissioned_officers/o1_enisgn.webp
- ensign_certificate.pcx → /textures/ui/ranks/terran/certificates/promotion/o1_enisgn.webp
- rank_promotion_sound.wav → /audio/sfx/ranks/terran/promotion_ceremony/insignia_pin.ogg
- ensign_description.txt → /text/ranks/terran/descriptions/commissioned_officers/o1_enisgn.txt
- ensign_requirements.txt → /text/ranks/terran/requirements/promotion_criteria/o1_enisgn.txt
- ensign_responsibilities.txt → /text/ranks/terran/responsibilities/authority_levels/o1_enisgn.txt
- insignia_placement.ani → /animations/ui/ranks/terran/promotion_ceremony/insignia_placement.png