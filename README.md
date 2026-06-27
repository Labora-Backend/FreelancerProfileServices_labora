# Freelancer Profile Service

Freelancer Profile Service owns freelancer profile records for Labora. It validates Auth Service JWTs, stores freelancer portfolio and availability details, and enriches profile reads with skill data from Skill Service when available.

## Responsibilities

- Create, update, view, and delete freelancer profiles.
- Store freelancer availability, hourly rate, portfolio, language, rating, and review totals.
- Fetch a freelancer's skills from Skill Service for profile display.
- Allow Review Service to update freelancer rating totals through an internal endpoint.
- Provide paginated freelancer summaries for Admin Service.

## Features

- Freelancer-only profile CRUD.
- Duplicate profile prevention on create.
- Skill enrichment through `SKILL_SERVICE_URL`.
- Internal rating synchronization.
- Optional profile image storage under `media/freelancer_profiles/`.

## API Endpoints

Base path: `/api/`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `freelancer/add/` | Freelancer JWT | Create a freelancer profile for the authenticated user. |
| `PUT`, `PATCH` | `freelancer/update/` | Freelancer JWT | Update the authenticated user's profile. |
| `GET` | `freelancer/view/` | Freelancer JWT | Return the authenticated user's profile and skills when Skill Service responds. |
| `DELETE` | `freelancer/delete/` | Freelancer JWT | Delete the authenticated user's profile. |

## Internal Service Endpoints

Internal endpoints use `X-Service-Key: <SERVICE_API_KEY>`.

| Method | Path | Description |
| --- | --- | --- |
| `PATCH` | `internal/freelancers/<user_id>/rating/` | Update `average_rating` and/or `total_reviews`. |
| `GET` | `internal/freelancers/` | Return paginated freelancer summaries. |

## Authentication

Profile APIs require `Authorization: Bearer <access_token>` and the token role must be `freelancer`. JWT verification uses the shared RS256 public key.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key. |
| `DEBUG` | Enables debug mode when set to `True`. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | MySQL database configuration. |
| `JWT_PUBLIC_KEY_PATH` | Public key used to verify Auth Service JWTs. |
| `SERVICE_API_KEY` | Shared key for internal requests. |
| `SKILL_SERVICE_URL` | Skill Service base URL used to fetch freelancer skills. |
| `*_SERVICE_URL` | Optional service URLs loaded by settings for cross-service configuration. |

## Setup

```bash
cd FreelancerProfileServices
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8002
```

## Service Architecture

- Django project: `freelancer_profile_service`
- App: `profiles`
- Authentication: `profiles.authentication.CustomJWTAuthentication`
- Role checks: `profiles.role_permissions.IsFreelancer`
- Internal permission: `profiles.permissions.internal_service.IsInternalService`
- Outbound dependency: Skill Service for profile skill enrichment

## Database Models

- `FreelancerProfile`: stores `user_id`, identity fields, title, bio, location, image, experience, hourly rate, currency, availability, languages, portfolio URL, completed-job count, average rating, review count, verification/active flags, last seen, and timestamps.

## Notification/Event Flow

This service does not create notifications. Review Service calls its internal rating endpoint after a review is created.
