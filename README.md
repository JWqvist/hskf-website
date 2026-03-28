# HSKF.dk — Holmegaard Skytteforening

Foreningens hjemmeside bygget med [Astro](https://astro.build) og [Tailwind CSS v4](https://tailwindcss.com).

## 🚀 Kom i gang

```bash
npm install
npm run dev       # Start lokal udviklingsserver
npm run build     # Byg til produktion (kører automatisk ICS-generering)
npm run preview   # Forhåndsvisning af produktionsbuild
```

## 📁 Projektstruktur

```
/
├── public/
│   ├── ics/              # Auto-genererede kalender-filer (.ics) — redigér ikke manuelt
│   ├── images/           # Billeder og assets
│   └── vedtaegter.pdf    # Foreningens vedtægter
├── scripts/
│   └── generate-ics.mjs  # Kører automatisk før build – genererer .ics filer fra events.json
├── src/
│   ├── data/             # ← Her redigeres indhold (JSON)
│   │   ├── events.json
│   │   ├── notices.json
│   │   └── training.json
│   ├── layouts/
│   └── pages/
└── package.json
```

---

## 📝 Indhold — sådan opdateres det

Alt siteindhold styres via tre JSON-filer i `src/data/`. Ingen kode skal ændres for at opdatere events, beskeder eller træningstider.

---

### 📅 `events.json` — Begivenheder og kalender

Vises på **Kalender**-siden. Hvert event genererer automatisk en `.ics` fil (Apple Calendar, Google Calendar, Outlook) ved næste build.

```json
[
  {
    "id": 0,
    "title": "Udendørs sæsonstart 2026",
    "date": "2026-04-09",
    "time": "18:30",
    "location": "toksvær",
    "disciplines": ["Riffel", "Pistol"],
    "description": "Beskrivelse af eventet. Vises på kalender-siden."
  }
]
```

| Felt | Type | Beskrivelse |
|------|------|-------------|
| `id` | `number` | Unikt heltal — øg med 1 for hvert nyt event. Bruges til `.ics` filnavn. |
| `title` | `string` | Eventets navn |
| `date` | `string` | Dato i format `YYYY-MM-DD` |
| `time` | `string` | Starttidspunkt i format `HH:MM` (f.eks. `"18:30"`) |
| `location` | `string` | Enten `"toksvær"` (Lundebakkevej 18C) eller `"holmegaard"` (Villavej 2) |
| `disciplines` | `string[]` | Liste over discipliner, f.eks. `["Riffel", "Pistol"]`. Tom liste `[]` hvis ikke relevant. |
| `description` | `string` | Fritekst-beskrivelse af eventet |

> **Bemærk:** Når et event tilføjes, kører `scripts/generate-ics.mjs` automatisk ved næste `npm run build` og opretter `/public/ics/event-{id}.ics`.

---

### 📢 `notices.json` — Notifikationsbanner

Vises som et banner øverst på sitet i en given tidsperiode. Bruges til vigtige beskeder som kontingent-deadlines, aflysninger eller andet tidskritisk.

```json
[
  {
    "id": "kontingent-2026",
    "message": "Husk at betale kontingent for 2026 – deadline 1. april.",
    "type": "warning",
    "from": "2026-03-01",
    "to": "2026-04-01",
    "link": { "label": "Kontakt bestyrelsen", "href": "mailto:kontakt@hskf.dk" }
  }
]
```

| Felt | Type | Beskrivelse |
|------|------|-------------|
| `id` | `string` | Unikt ID (bruges til at vise beskeden én gang per bruger) |
| `message` | `string` | Beskedteksten der vises i banneret |
| `type` | `string` | Udseende/farve: `"info"` (blå), `"warning"` (gul), `"error"` (rød), `"success"` (grøn) |
| `from` | `string` | Startdato i format `YYYY-MM-DD` — banneret vises fra denne dato |
| `to` | `string` | Slutdato i format `YYYY-MM-DD` — banneret skjules efter denne dato |
| `link` | `object` \| `null` | Valgfrit link i banneret. Udelad feltet eller sæt `null` for intet link. |
| `link.label` | `string` | Linktekst |
| `link.href` | `string` | URL eller `mailto:`-adresse |

> **Tip:** Bannervisning styres automatisk af `from`/`to` datoerne. Du behøver ikke slette gamle notices — de skjules af sig selv.

---

### 🏋️ `training.json` — Træningstider

Vises på **Bliv medlem**-siden og andre relevante steder. Definerer ugentlige træningstider per ugedag.

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
        "notes": "Sommersæson: 9. april – 25. september. Udendørs på 25m banen i Toksværd."
      }
    ]
  }
]
```

| Felt | Type | Beskrivelse |
|------|------|-------------|
| `day` | `string` | Ugedag på dansk (f.eks. `"Torsdag"`) |
| `dayEn` | `string` | Ugedag på engelsk (f.eks. `"Thursday"`) — bruges internt til sortering |
| `sessions` | `array` | Liste over træningssessioner denne dag. Tom liste `[]` hvis ingen træning. |
| `sessions[].time` | `string` | Tidspunkt, f.eks. `"Fra kl. 18:30"` |
| `sessions[].location` | `string` | Enten `"toksvær"` eller `"holmegaard"` |
| `sessions[].discipline` | `string` | F.eks. `"Riffel"` eller `"Pistol"` |
| `sessions[].notes` | `string` | Yderligere info, f.eks. sæsonperiode eller særlige regler |

> **Bemærk:** Alle syv ugedage skal være til stede i arrayet (selv uden sessions). Rækkefølgen i filen er den rækkefølge de vises på sitet.

---

## 🌿 Git-workflow

```
main  ← Produktion (hskf-website.pages.dev) — kræver PR + godkendelse
dev   ← Staging/preview — push frit
```

Alle ændringer laves på `dev`. Når klar til produktion: opret PR fra `dev` → `main`.

## 🔧 Deploy

Cloudflare Pages deployer automatisk:
- `dev` → preview URL ved hvert push
- `main` → <https://hskf-website.pages.dev> ved merge
