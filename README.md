# Interviewer Platform

The **Interviewer Platform** is a Django-based application designed to facilitate automated interviews with integrated transcription, vocalization, and comprehensive interview scripting functionalities. This repository houses the complete source code, configuration, and assets required to deploy and run the platform.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Interviewer Platform is built to manage and conduct interviews using a combination of automated scripts and real-time agent modules. It leverages Django’s robust framework to deliver a seamless user experience for both interview administrators and participants. Key functionalities include:

- **Interview Scripting:** Define detailed interview modules using JSON scripts.
- **Agent Modules:** Automated agents for transcription and vocalization.
- **User Interface:** A comprehensive set of templates and views for managing interviews, user accounts, and settings.
- **Infrastructure:** Ready-to-deploy configurations with Heroku support (Procfile, Aptfile, runtime.txt) and a structured settings module.

---

## Features

- **Dynamic Interview Scripts:** Customize interview flow with a collection of JSON scripts.
- **Transcription & Vocalization:** Integrated modules (`transcribe.py`, `vocalize.py`) to handle audio processing.
- **Scalable Architecture:** Separation of concerns through modular directory structure (apps, templates, and utilities).
- **User Management:** Full-featured account management with email confirmation, password reset, and social account integration.
- **Deployment Ready:** Includes configuration files for easy deployment to platforms like Heroku.

---

## Directory Structure

Below is an overview of the repository’s directory structure:

```
gabm_interviewer_platform/
├── Aptfile
├── Procfile
├── db.sqlite3
├── global_methods.py
├── manage.py
├── requirements.txt
├── runtime.txt
├── gabm_infra/
│   ├── __init__.py
│   ├── asgi.py
│   ├── db.sqlite3
│   ├── urls.py
│   ├── utils.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       └── base.py
├── interviewer_agent/
│   ├── agent_modules/
│   │   ├── transcribe.py
│   │   ├── transcribe_OLD.py
│   │   ├── transcribe_test.py
│   │   └── vocalize.py
│   ├── interview_script/
│   │   └── new_avp_full_v1/
│   │       ├── meta.json
│   │       ├── module1.json
│   │       ├── module10.json
│   │       ├── module11.json
│   │       ├── module12.json
│   │       ├── module13.json
│   │       ├── module14.json
│   │       ├── module15.json
│   │       ├── module16.json
│   │       ├── module17.json
│   │       ├── module18.json
│   │       ├── module19.json
│   │       ├── module2.json
│   │       ├── module20.json
│   │       ├── module21.json
│   │       ├── module22.json
│   │       ├── module23.json
│   │       ├── module24.json
│   │       ├── module25.json
│   │       ├── module26.json
│   │       ├── module27.json
│   │       ├── module28.json
│   │       ├── module29.json
│   │       ├── module3.json
│   │       ├── module30.json
│   │       ├── module31.json
│   │       ├── module32.json
│   │       ├── module33.json
│   │       ├── module34.json
│   │       ├── module35.json
│   │       ├── module36.json
│   │       ├── module37.json
│   │       ├── module38.json
│   │       ├── module39.json
│   │       ├── module4.json
│   │       ├── module40.json
│   │       ├── module41.json
│   │       ├── module42.json
│   │       ├── module43.json
│   │       ├── module44.json
│   │       ├── module45.json
│   │       ├── module46.json
│   │       ├── module47.json
│   │       ├── module48.json
│   │       ├── module49.json
│   │       ├── module5.json
│   │       ├── module50.json
│   │       ├── module51.json
│   │       ├── module52.json
│   │       ├── module53.json
│   │       ├── module54.json
│   │       ├── module55.json
│   │       ├── module56.json
│   │       ├── module57.json
│   │       ├── module6.json
│   │       ├── module7.json
│   │       ├── module8.json
│   │       └── module9.json
│   ├── interviewer_utils/
│   │   └── settings.py
│   └── prompt_template/
│       ├── __init__.py
│       ├── gpt_structure.py
│       ├── gpt_structure_OLD.py
│       ├── gpt_structure_test.py
│       ├── print_prompt.py
│       ├── run_gpt_prompt.py
│       └── prompts/
│           ├── conditional_v1.txt
│           ├── factualq_next_interview_step_v1.txt
│           ├── factualq_next_interview_step_v2.txt
│           ├── module_notes_v1.txt
│           ├── q_end_thankyou_v1.txt
│           ├── qualitativeq_next_interview_step_v1.txt
│           └── qualitativeq_next_interview_step_v2.txt
├── pages/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── interview_settings.py
│   ├── models.py
│   ├── pipelines.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│       ├── 0001_initial.py
│       ├── 0002_alter_participant_email.py
│       ├── 0003_interview_pruned_p_notes.py
│       ├── 0004_alter_interview_p_notes_and_more.py
│       ├── 0005_perfmeasurement.py
│       ├── 0006_participant_completed_modules_det_timeouttimer.py
│       ├── 0007_timeouttimer_cause.py
│       ├── 0008_alter_timeouttimer_endtime.py
│       ├── 0009_alter_interviewquestion_q_max_sec.py
│       ├── 0010_interviewquestion_q_condition.py
│       ├── 0011_behavioralstudymodule_and_more.py
│       ├── 0012_remove_behavioralstudymodule_study_completed_1_and_more.py
│       ├── 0013_participant_camerer_activated.py
│       ├── 0014_interviewquestion_zipped_audio_and_more.py
│       ├── 0015_remove_interviewquestion_zipped_audio_and_more.py
│       └── __init__.py
└── templates/
    ├── aside_navbar.html
    ├── base.html
    ├── footer.html
    ├── navbar.html
    ├── account/
    │   ├── account_inactive.html
    │   ├── base.html
    │   ├── email.html
    │   ├── email_change.html
    │   ├── email_confirm.html
    │   ├── login.html
    │   ├── logout.html
    │   ├── password_change.html
    │   ├── password_reset.html
    │   ├── password_reset_done.html
    │   ├── password_reset_from_key.html
    │   ├── password_reset_from_key_done.html
    │   ├── password_set.html
    │   ├── reauthenticate.html
    │   ├── signup.html
    │   ├── signup_closed.html
    │   ├── verification_sent.html
    │   ├── verified_email_required.html
    │   ├── email/
    │   │   ├── account_already_exists_message.txt
    │   │   ├── account_already_exists_subject.txt
    │   │   ├── base_message.txt
    │   │   ├── email_confirmation_message.txt
    │   │   ├── email_confirmation_signup_message.txt
    │   │   ├── email_confirmation_signup_subject.txt
    │   │   ├── email_confirmation_subject.txt
    │   │   ├── password_reset_key_message.txt
    │   │   ├── password_reset_key_subject.txt
    │   │   ├── unknown_account_message.txt
    │   │   └── unknown_account_subject.txt
    │   ├── messages/
    │   │   ├── cannot_delete_primary_email.txt
    │   │   ├── email_confirmation_failed.txt
    │   │   ├── email_confirmation_sent.txt
    │   │   ├── email_confirmed.txt
    │   │   ├── email_deleted.txt
    │   │   ├── logged_in.txt
    │   │   ├── logged_out.txt
    │   │   ├── password_changed.txt
    │   │   ├── password_set.txt
    │   │   ├── primary_email_set.txt
    │   │   └── unverified_primary_email.txt
    │   └── snippets/
    │       ├── already_logged_in.html
    │       └── warn_no_email.html
    ├── pages/
    │   ├── archive/
    │   │   └── login.html
    │   ├── create_avatar/
    │   │   └── create_avatar.html
    │   ├── home/
    │   │   ├── home.html
    │   │   ├── home_OLD_2.html
    │   │   ├── home_old.html
    │   │   └── landing.html
    │   ├── interview/
    │   │   ├── interivew_Jan7end_save.html
    │   │   ├── interview.html
    │   │   ├── interview_Feb19_save.html
    │   │   ├── interview_Jan7_save.html
    │   │   ├── interview_OLD.html
    │   │   ├── interview_base.html
    │   │   └── interview_modals.html
    │   ├── summary/
    │   │   └── summary.html
    │   └── transcript/
    │       └── transcript.html
    └── socialaccount/
        ├── authentication_error.html
        ├── base.html
        ├── connections.html
        ├── login.html
        ├── login_cancelled.html
        ├── signup.html
        ├── messages/
        │   ├── account_connected.txt
        │   ├── account_connected_other.txt
        │   ├── account_connected_updated.txt
        │   └── account_disconnected.txt
        └── snippets/
            ├── login_extra.html
            └── provider_list.html
```

This structure separates concerns by grouping similar functionalities together:
- **gabm_infra:** Core infrastructure and settings.
- **interviewer_agent:** Logic for interview scripting, agent modules (transcription, vocalization), and GPT prompt templates.
- **pages:** Django app containing models, views, forms, pipelines, and migrations for the interview process.
- **templates:** HTML templates for various parts of the application, including account management and interview pages.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/gabm_interviewer_platform.git
   cd gabm_interviewer_platform
   ```

2. **Set Up a Virtual Environment**

   It is recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   Set up your database:

   ```bash
   python manage.py migrate
   ```

5. **Collect Static Files (if applicable)**

   ```bash
   python manage.py collectstatic
   ```

---

## Usage

1. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at [http://localhost:8000](http://localhost:8000).

2. **Managing Interviews**

   - Configure your interview settings via the Django admin or through the dedicated settings in the `pages` app.
   - Update or customize interview scripts located in `interviewer_agent/interview_script/new_avp_full_v1/` as needed.
   - Use the agent modules in `interviewer_agent/agent_modules/` for transcription and vocalization functionalities.

3. **Working with Templates**

   Customize the look and feel of the platform by editing the HTML templates in the `templates/` directory.

---

## Configuration

- **Settings:** The core settings are managed in `gabm_infra/settings/base.py`. Adjust database configurations, allowed hosts, and other Django settings here.
- **Deployment Files:** The repository includes:
  - **Procfile**: For Heroku deployment.
  - **Aptfile**: To specify additional system-level dependencies.
  - **runtime.txt**: To define the Python runtime version.

---

## Contributing

Contributions are welcome! If you would like to contribute to the project, please:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear descriptions.
4. Submit a pull request detailing your changes.

Please follow the existing code style and include tests for any new features or bug fixes.

---

## License

This project is licensed under the [MIT License](LICENSE).
