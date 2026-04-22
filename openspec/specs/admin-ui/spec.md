# admin-ui Specification

## Purpose
TBD - created by archiving change setup-initial-dashboard. Update Purpose after archive.
## Requirements
### Requirement: Modern Admin Interface
The project SHALL use `django-unfold` to provide a modern, Tailwind-based administrative interface with a functional sticky action bar.

#### Scenario: Branding Visibility on Subpages
- GIVEN the superuser is on a model list view (e.g., Bookings) or a change form.
- WHEN the page is rendered.
- THEN the sidebar MUST display the brand logo and site name.
- AND the `branding` template block MUST be explicitly defined in `base_site.html`.

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

#### Scenario: Apply Dynamic Colors without Recursion
- GIVEN the `skeleton.html` override is active.
- WHEN the admin dashboard is loaded.
- THEN the template MUST NOT cause a recursion error during extension.
- AND the `--brand-primary-500` CSS variable MUST match the value provided by the `brand_theme_context`.

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

