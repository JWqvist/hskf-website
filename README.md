# HSKF.dk — Holmegaard Skytteforening

The association's website built with [Astro](https://astro.build) and [Tailwind CSS v4](https://tailwindcss.com).

## 🚀 Getting Started

```bash
npm install
npm run dev       # Start local development server
npm run build     # Build for production (automatically generates ICS files)
npm run preview   # Preview production build locally
```

## 📁 Project Structure

```
/
├── public/
│   ├── ics/              # Auto-generated calendar files (.ics) — do not edit manually
│   ├── images/           # Images and assets
│   └── vedtaegter.pdf    # Association bylaws (PDF)
├── scripts/
│   └── generate-ics.mjs  # Runs automatically before build — generates .ics from events.json
├── src/
│   ├── data/             # ← Edit content here (JSON)
│   │   ├── events.json
│   │   ├── notices.json
│   │   └── training.json
│   ├── layouts/
│   └── pages/
└── package.json
```

---

## 📝 Content — How to Update

All site content is managed via three JSON files in `src/data/`. No code changes are required to update events, notices, or training schedules.

---

### 📅 `events.json` — Events & Calendar

Displayed on the **Kalender** page. Each event automatically generates a `.ics` file (compatible with Apple Calendar, Google Calendar, and Outlook) on the next build.

```json
[
  {
    "id": 0,
    "title": "Udendørs sæsonstart 2026",
    "date": "2026-04-09",
    "time": "18:30",
    "location": "toksvær",
    "disciplines": ["Riffel", "Pistol"],
    "description": "Description of the event. Shown on the calendar page."
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | `number` | Unique integer — increment by 1 for each new event. Used as the `.ics` filename. |
| `title` | `string` | Name of the event |
| `date` | `string` | Date in `YYYY-MM-DD` format |
| `time` | `string` | Start time in `HH:MM` format (e.g. `"18:30"`) |
| `location` | `string` | Either `"toksvær"` (Lundebakkevej 18C) or `"holmegaard"` (Villavej 2) |
| `disciplines` | `string[]` | List of disciplines, e.g. `["Riffel", "Pistol"]`. Use an empty array `[]` if not applicable. |
| `description` | `string` | Free-text description of the event |
| `link` | `object` \| `null` | Optional action button on the event card. Omit or set to `null` for no button. |
| `link.label` | `string` | Button text, e.g. `"Tilmeld dig"`, `"Læs mere"`, `"Book plads"` |
| `link.href` | `string` | URL or `mailto:` address the button links to |

> **Note:** When an event is added, `scripts/generate-ics.mjs` runs automatically on the next `npm run build` and creates `/public/ics/event-{id}.ics`.

---

### 📢 `notices.json` — Notification Banner

Displayed as a banner at the top of the site within a given date range. Use for important time-sensitive messages such as membership deadlines, cancellations, or announcements.

```json
[
  {
    "id": "kontingent-2026",
    "message": "Remember to pay your membership fee for 2026 – deadline April 1st.",
    "type": "warning",
    "from": "2026-03-01",
    "to": "2026-04-01",
    "link": { "label": "Contact the board", "href": "mailto:kontakt@hskf.dk" }
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique ID (used to show the notice once per user via local storage) |
| `message` | `string` | The message text displayed in the banner |
| `type` | `string` | Visual style: `"info"` (blue), `"warning"` (yellow), `"error"` (red), `"success"` (green) |
| `from` | `string` | Start date in `YYYY-MM-DD` format — banner becomes visible from this date |
| `to` | `string` | End date in `YYYY-MM-DD` format — banner is hidden after this date |
| `link` | `object` \| `null` | Optional link shown inside the banner. Omit the field or set to `null` for no link. |
| `link.label` | `string` | Link text |
| `link.href` | `string` | URL or `mailto:` address |

> **Tip:** Banner visibility is controlled automatically by the `from`/`to` dates. You do not need to delete old notices — they hide themselves.

---

### 🏋️ `training.json` — Training Schedule

Displayed on the **Bliv medlem** page and other relevant pages. Defines weekly training sessions per day of the week.

```json
[
  {
    "day": "Torsdag",
    "dayEn": "Thursday",
    "sessions": [
      {
        "time": "Fra kl. 18:30",
        "location": "toksvær",
        "discipline": "Riffel",
        "notes": "Summer season: April 9 – September 25. Outdoor on the 25m range in Toksværd."
      }
    ]
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `day` | `string` | Day of the week in Danish (e.g. `"Torsdag"`) |
| `dayEn` | `string` | Day of the week in English (e.g. `"Thursday"`) — used internally for sorting |
| `sessions` | `array` | List of training sessions for this day. Use an empty array `[]` if no training. |
| `sessions[].time` | `string` | Time slot, e.g. `"Fra kl. 18:30"` |
| `sessions[].location` | `string` | Either `"toksvær"` or `"holmegaard"` |
| `sessions[].discipline` | `string` | E.g. `"Riffel"` or `"Pistol"` |
| `sessions[].notes` | `string` | Additional info such as season period or special rules |

> **Note:** All seven days of the week must be present in the array (even with empty sessions). The order in the file determines the display order on the site.

---

## 🌿 Git Workflow

```
main  ← Production (hskf-website.pages.dev) — requires PR + approval
dev   ← Staging/preview — push freely
```

All changes are made on `dev`. When ready for production, open a PR from `dev` → `main`.

## 🔧 Deployment

Cloudflare Pages deploys automatically:
- `dev` → preview URL on every push
- `main` → <https://hskf-website.pages.dev> on merge
