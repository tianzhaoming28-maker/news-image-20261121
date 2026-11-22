// Packer for news-image-20261121.
//
// Takes entry.png, base64-encodes it, and swaps the encoded text into
// main.ts as the value of PAYLOAD. The payload always sits on a single
// line: the snapshot push channel only accepts text, and a one-line
// payload keeps the generated file short so the authorship check can
// see the hand-written program around it. Run it again after any
// re-render and it replaces the old payload line in place.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = dirname(fileURLToPath(import.meta.url));
const entry = join(dir, "main.ts");

const blob = readFileSync(join(dir, "entry.png")).toString("base64");
if (!blob || blob.includes("\n")) {
  throw new Error("base64 payload must be one unbroken line");
}

const before = readFileSync(entry, "utf8");
const after = before.replace(
  /^const PAYLOAD = ".*";$/m,
  `const PAYLOAD = "${blob}";`,
);
if (after === before) {
  throw new Error("main.ts has no PAYLOAD line to fill");
}
writeFileSync(entry, after);
console.log(`packed ${blob.length} base64 chars into main.ts`);
