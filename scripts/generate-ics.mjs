#!/usr/bin/env node
/**
 * generate-ics.mjs
 * Generates static .ics files in public/ics/ from src/data/events.json
 * Runs automatically as part of `npm run build` (prebuild hook)
 */

import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const events = JSON.parse(readFileSync(join(root, 'src/data/events.json'), 'utf8'));
const outDir = join(root, 'public/ics');

mkdirSync(outDir, { recursive: true });

const LOCATIONS = {
  toksvær: 'Lundebakkevej 18C\\, 4684 Holmegaard',
  holmegaard: 'Villavej 2\\, 4684 Holmegaard',
};

const now = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

for (const event of events) {
  const dateStr = event.date.replace(/-/g, '');
  const [hour, min] = event.time.split(':');
  const timeStart = `${hour}${min}00`;
  const timeEnd = `${String(parseInt(hour) + 2).padStart(2, '0')}${min}00`;
  const location = LOCATIONS[event.location] ?? 'Holmegaard';
  const desc = event.description.replace(/\n/g, '\\n').replace(/,/g, '\\,');
  const title = event.title.replace(/,/g, '\\,');

  const ics = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//HSKF//Holmegaard Skytteforening//DA',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    `UID:hskf-${event.id}@hskf.dk`,
    `DTSTAMP:${now}`,
    `DTSTART:${dateStr}T${timeStart}Z`,
    `DTEND:${dateStr}T${timeEnd}Z`,
    `SUMMARY:${title}`,
    `DESCRIPTION:${desc}`,
    `LOCATION:${location}`,
    `ORGANIZER;CN=Holmegaard Skytteforening:mailto:kontakt@hskf.dk`,
    'STATUS:CONFIRMED',
    'SEQUENCE:0',
    'BEGIN:VALARM',
    'TRIGGER:-PT15M',
    'ACTION:DISPLAY',
    'DESCRIPTION:Reminder',
    'END:VALARM',
    'END:VEVENT',
    'END:VCALENDAR',
  ].join('\r\n');

  const outPath = join(outDir, `event-${event.id}.ics`);
  writeFileSync(outPath, ics);
  console.log(`✓ Generated ${outPath}`);
}

console.log(`✓ ${events.length} .ics file(s) written to public/ics/`);
