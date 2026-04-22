# admin-ui Specification

## Purpose
TBD - created by archiving change setup-initial-dashboard. Update Purpose after archive.
## Requirements
### Requirement: Modern Admin Interface
The project SHALL use `django-unfold` to provide a modern, Tailwind-based administrative interface with a functional sticky action bar.

#### Scenario: Sticky Bottom Bar Presence
- Given the superuser is on a model change form (e.g., editing a Booking).
- When the page content exceeds the viewport height.
- Then the action bar (containing Save and Delete buttons) SHALL remain pinned to the bottom of the viewport.
- And the layout SHALL use Unfold's standard container classes to ensure proper spacing.

#### Scenario: Standardized Admin UI Features
- Given an admin class inheriting from `ModelAdminUnfoldBase`.
- When accessing the change form.
- Then "Warn Unsaved Changes" MUST be enabled.
- And fields SHALL be displayed in their compressed format by default.
- And a "Cancel" button SHALL be visible in the action bar.

### Requirement: Markdown Support in Admin
Text areas in the admin interface SHALL support Markdown editing via SimpleMDE.

#### Scenario: Edit Markdown Field
- When editing a model with a text area in the admin.
- Then the field is enhanced with a SimpleMDE editor.

### Requirement: Environment Badges
The admin interface SHALL display a badge indicating the current environment (Production, Development, etc.).

#### Scenario: Display Environment Badge
- Given `ENV=prod`.
- When accessing the admin.
- Then a "Production" badge is visible in the header.

### Requirement: Template-based CSS Variable Injection
The admin interface SHALL inject dynamic primary color shades into the document `:root` using a template override.

#### Scenario: Apply Dynamic Colors
- GIVEN the `skeleton.html` override is active
- WHEN the admin dashboard is loaded
- THEN the `--brand-primary-500` CSS variable MUST match the `brand_color` in the `CompanyProfile`.

### Requirement: Admin Color Picker
The `brand_color` field in the `CompanyProfile` admin interface MUST be rendered using a visual color picker.

#### Scenario: Selecting a new brand color
- GIVEN the user is on the `CompanyProfile` change page in the admin
- AND the user is logged in as the development admin (`admin` / `admin`)
- WHEN the user clicks the `brand_color` input
- THEN a visual color picker MUST be displayed
- AND selecting a color MUST update the field value with a HEX code
- AND saving the profile MUST successfully update the `brand_color` and trigger the regeneration of the dashboard theme colors.

### Requirement: Color Restoration
After verification, the system MUST be restored to its original brand color to maintain design consistency.

#### Scenario: Restoring original color
- GIVEN the verification of the color picker is complete
- WHEN the `brand_color` is reset to `#ee5837`
- THEN the system MUST function exactly as it did prior to the change.

### Requirement: Color Math Preservation
The system MUST continue to derive a full color palette from the `brand_color`, even when it is provided in HEX format by the picker.

#### Scenario: Verifying derived shades
- GIVEN a `CompanyProfile` with `brand_color` set to `#682896`
- WHEN `get_brand_config()` is called
- THEN it MUST return a dictionary of 11 shades (50-950)
- AND the `500` shade MUST match `#682896`.

