import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chapters } from '../data/guide.ts';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const imageDir = path.resolve(scriptDir, '../public/images');
const expectedFigureCounts = [0, 0, 4, 2, 6, 6, 4, 5, 9, 4];
const expectedStepNumbers = [
  [], [], [1, 2, 3, 4, 5], [], [1, 2, 3, 4, 5, 6, 7],
  [1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3],
  [1, 2, 3, 4, 5, 6, 1, 2], [1, 2, 3, 4, 5, 6, 7],
];
const expectedStepFigures = [
  [], [],
  [[1], [2], [3], [], [4]],
  [],
  [[7], [8], [9], [10], [11], [12], []],
  [[13, 14], [15], [16], [17], [18]],
  [[19], [20, 21], [22], []],
  [[23, 24], [25], [26, 27]],
  [[28], [29], [30], [31], [32, 33], [34], [35], [36]],
  [[], [38], [39], [], [], [40], []],
];

assert.equal(chapters.length, 10, 'expected 10 chapters');
const chapterIds = chapters.map((chapter) => chapter.id);
assert.deepEqual(chapterIds, Array.from({ length: 10 }, (_, i) => String(i + 1).padStart(2, '0')), 'chapters must be ordered 01–10');
assert.equal(new Set(chapterIds).size, chapterIds.length, 'chapter IDs must be unique');

const blockIds = new Set();
const referencedFigureIds = new Set();
const allFigureIds = [];
let nextFigureId = 1;

for (const [chapterIndex, chapter] of chapters.entries()) {
  const figures = chapter.figures;
  const figureIds = figures.map((figure) => figure.id);
  assert.deepEqual(figureIds, Array.from({ length: figures.length }, (_, i) => nextFigureId + i), `figure numbering in chapter ${chapter.id}`);
  assert.equal(figures.length, expectedFigureCounts[chapterIndex], `figure count in chapter ${chapter.id}`);
  allFigureIds.push(...figureIds);
  nextFigureId += figures.length;

  let stepIndex = 0;
  for (const block of chapter.blocks) {
    assert.ok(block.id, `every block in chapter ${chapter.id} needs an ID`);
    assert.ok(!blockIds.has(block.id), `duplicate block ID: ${block.id}`);
    blockIds.add(block.id);
    if (block.kind === 'step') {
      assert.equal(block.number, expectedStepNumbers[chapterIndex][stepIndex], `step number sequence in chapter ${chapter.id}`);
      const actual = block.figureIds ?? [];
      assert.deepEqual(actual, expectedStepFigures[chapterIndex][stepIndex], `figure refs for step ${block.number} in chapter ${chapter.id}`);
      stepIndex += 1;
    }
    for (const id of block.figureIds ?? []) {
      assert.ok(figureIds.includes(id), `block ${block.id} references missing figure ${id}`);
      referencedFigureIds.add(id);
    }
    assert.doesNotMatch(JSON.stringify(block), /(?:https?:\/\/|(?:\.docx|\.xlsx)(?:\b|$))/i, `block ${block.id} must not link to downloads or remote content`);
  }
  assert.equal(stepIndex, expectedStepNumbers[chapterIndex].length, `step count in chapter ${chapter.id}`);
  for (const id of figureIds) assert.ok(referencedFigureIds.has(id), `figure ${id} is never referenced`);
}
assert.deepEqual(allFigureIds, Array.from({ length: 40 }, (_, i) => i + 1), 'figure IDs must cover 1–40 in order');
assert.doesNotMatch(JSON.stringify(chapters), /gmail\.com/i, 'content must not include Gmail examples');

const publicImages = readdirSync(imageDir).filter((name) => name.toLowerCase().endsWith('.png'));
assert.equal(publicImages.length, 40, 'expected exactly 40 local PNG figures');
for (const chapter of chapters) {
  for (const figure of chapter.figures) {
    assert.match(figure.src, /^\/images\/[\w.-]+\.png$/, `figure ${figure.id} must use a local /images path`);
    const imagePath = path.resolve(imageDir, path.basename(figure.src));
    assert.ok(imagePath.startsWith(`${imageDir}${path.sep}`), `figure ${figure.id} path must stay inside public/images`);
    assert.ok(existsSync(imagePath), `missing image file for figure ${figure.id}: ${figure.src}`);
    const png = readFileSync(imagePath);
    assert.equal(png.toString('hex', 0, 8), '89504e470d0a1a0a', `figure ${figure.id} is not PNG`);
    assert.equal(png.toString('ascii', 12, 16), 'IHDR', `figure ${figure.id} has no PNG IHDR`);
    assert.equal(png.readUInt32BE(16), figure.width, `width mismatch for figure ${figure.id}`);
    assert.equal(png.readUInt32BE(20), figure.height, `height mismatch for figure ${figure.id}`);
  }
}

console.log('Content integrity checks passed: chapters, step mappings, local figures, and PNG dimensions.');


