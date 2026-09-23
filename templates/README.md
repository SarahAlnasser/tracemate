# Letter templates

One JSON file per letter, made with `device/tools/template_maker.py`.

| File | Letter | Status |
| --- | --- | --- |
| alif.json | ا | Starter (straight line); retrace with the tool if needed |
| baa.json | ب | To make |
| jeem.json | ج | To make |

Format: coordinates run from 0 to 1 inside a square box, strokes are in writing order,
`tolerance` is the allowed distance from the path (0.05 = 5% of the box).
