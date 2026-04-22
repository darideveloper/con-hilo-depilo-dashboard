# core-settings Specification

## Purpose
TBD - created by archiving change setup-initial-dashboard. Update Purpose after archive.
## Requirements
### Requirement: Dynamic Settings Initialization
The `settings.py` SHALL initialize `python-dotenv` and load the appropriate environment file based on the `ENV` variable.

#### Scenario: Load Settings from ENV
- Given `ENV=dev` in `.env`.
- When `settings.py` is loaded.
- Then `.env.dev` is loaded and `DEBUG` is set based on its content.

### Requirement: Dynamic Database Selection
The database backend SHALL switch between PostgreSQL (production/dev) and SQLite (testing) automatically.

#### Scenario: SQLite for Testing
- When running `python manage.py test`.
- Then the `DATABASES` setting uses the SQLite backend.

### Requirement: Conditional Storage
The project SHALL support switching between local file storage and AWS S3 based on the `STORAGE_AWS` environment variable.

#### Scenario: AWS Storage enabled
- Given `STORAGE_AWS=True`.
- When the application handles file uploads.
- Then files are uploaded to the configured S3 bucket.

### Requirement: Branding Context Processor
 the project SHALL include a context processor to provide derived brand colors to all templates.

#### Scenario: Inject Brand Colors
- GIVEN the `branding` context processor is registered
- WHEN any template is rendered
- THEN `brand_colors` (containing 400, 500, 600 shades) MUST be available in the context.

### Requirement: Default Language Configuration
The project's default language SHALL be configured to Spanish (`es`).

#### Scenario: Spanish Language Setup
- Given the Django application is running.
- When `LANGUAGE_CODE` is loaded from settings.
- Then the language code MUST be `"es"` by default.

#### Scenario: Environment Override for Language
- Given `LANGUAGE_CODE=en-us` in the environment.
- When the Django application starts.
- Then the `LANGUAGE_CODE` setting MUST be `"en-us"`.

### Requirement: Environment Variable Documentation
All environment-specific configuration files (`.env*`) SHALL include the `LANGUAGE_CODE` variable to ensure visibility across different stages.

#### Scenario: Sync Environment Examples
- Given the `.env.example` file.
- When a new language setting is introduced.
- Then `.env.example` MUST be updated with the `LANGUAGE_CODE` variable.

