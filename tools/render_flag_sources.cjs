// Editable vector masters -> transparent PNG sources for the Python DDS exporter.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');
const flags = JSON.parse(fs.readFileSync(path.join(root, 'data/clan_flags.json'), 'utf8'));
(async () => {
  for (const flag of Object.values(flags)) {
    const base = path.join(root, 'art/flags/sources', flag.source);
    await sharp(base + '.svg', { density: 288 }).resize(384, 256).png().toFile(base + '.png');
  }
  console.log('Rendered five transparent emblem sources.');
})().catch(error => { console.error(error); process.exit(1); });
