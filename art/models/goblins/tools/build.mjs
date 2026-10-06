import { readFile, writeFile, mkdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import * as core from "./goblin_source.mjs";
import { renderSheet, encodePNG } from "./render_sheet.mjs";

const root = new URL("../", import.meta.url);
const config = JSON.parse(await readFile(new URL("clans.json", root), "utf8"));
const raw = await readFile(new URL("source/Goblin_Male.gltf", root));
const hash = createHash("sha1").update("blob " + raw.length + "\0").update(raw).digest("hex");
if (hash !== config.source.git_blob) throw Error("Upstream source blob differs from the pinned asset.");
const source = JSON.parse(raw.toString("utf8"));
const base = core.prepareBase(source);
const models = [];
const reports = [];
let buffers;
for (const clan of config.clans) {
  const result = core.buildVariant(base, clan, config);
  const report = core.validateModel(result.gltf, result.buffers);
  if (JSON.stringify(result.gltf.animations) !== JSON.stringify(source.animations)) throw Error("Animation metadata changed.");
  if (JSON.stringify(result.gltf.skins) !== JSON.stringify(source.skins)) throw Error("Skin topology changed.");
  if (Math.abs(report.bounds.height - config.height_m) > 1e-6) throw Error("Wrong target height.");
  if (Math.abs(report.bounds.min[1]) > 1e-6) throw Error("Ground plane mismatch.");
  const output = core.toGLB(result.gltf, result.buffers);
  await mkdir(new URL("variants/", root), { recursive: true });
  await writeFile(new URL("variants/" + clan.id + ".glb", root), output);
  models.push(result.gltf);
  buffers = result.buffers;
  reports.push({ clan: clan.id, bytes: output.length, ...report });
}
const sheet = renderSheet(models, buffers, config, core);
await mkdir(new URL("preview/", root), { recursive: true });
await writeFile(new URL("preview/clan_lineup.svg", root), sheet.svg);
await writeFile(new URL("preview/clan_lineup.png", root), encodePNG(sheet.width,sheet.height,sheet.rgb));
console.log(JSON.stringify({ models: reports, engine_exported: false }, null, 2));
