# Availability API Documentation

## Endpoint: `GET /api/availability/days/`

The Availability API provides a way to query available dates for specific services, respecting both service-level and company-wide business rules, including availability ranges, weekday slots, and date overrides.

---

### Request Details

- **Method**: `GET`
- **URL**: `/api/availability/days/`
- **Authentication**: Public (no authentication required).

#### Query Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `service_ids` | `string` | Yes | Comma-separated list of service IDs to check (e.g., `1,5`). |
| `start_date` | `string` | No | Start date in `YYYY-MM-DD` format. Defaults to today's date if omitted. |

---

### Request Variants

#### 1. Fetch availability for a single service
```bash
curl -X GET "http://127.0.0.1:8000/api/availability/days/?service_ids=5"
```

#### 2. Fetch availability for multiple services
```bash
curl -X GET "http://127.0.0.1:8000/api/availability/days/?service_ids=1,5"
```

#### 3. Fetch availability starting from a specific date
```bash
curl -X GET "http://127.0.0.1:8000/api/availability/days/?service_ids=5&start_date=2026-05-01"
```

---

### Response Details

#### Expected Response (Success - 200 OK)
Returns a JSON array of strings representing available dates (YYYY-MM-DD) for the next 30 days from the `start_date`.

```json
[
  "2026-04-30",
  "2026-05-01",
  "2026-05-04",
  "2026-05-05"
]
```

#### Expected Response (Error - 400 Bad Request)
Returned if required parameters are missing or invalid.

```json
{
  "error": "service_ids is required"
}
```
OR
```json
{
  "error": "Invalid service_ids format"
}
```

---

### Validation Hierarchy
The API calculates availability using the following precedence:

1.  **Availability Ranges**: If defined, validates against service-level `EventAvailability`. Falls back to `CompanyAvailability`.
2.  **Overrides**: Service-level `EventDateOverride` are checked, followed by `CompanyDateOverride`. Positive overrides (is_available=True) take precedence over weekly slot filters.
3.  **Weekday Slots**: Validates against `AvailabilitySlot` (Service) or `CompanyWeekdaySlot` (Company). If no slots are defined at either level, the day is considered enabled.
