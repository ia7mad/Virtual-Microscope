# Visitor media repair — 2026-10-25

## Observed library

The current Edge profile contained 16 cases, not just the eight source defaults. All tray entries were selected, including entries outside the visible horizontal tray and every category. The visitor's library is retained in the regression fixture. No case is created or removed by the repair.

| Existing case | Failure | Replacement |
| --- | --- | --- |
| عينة دم طبيعية / Normal Blood Sample | Unavailable `/uploads/` JPEG | Giemsa blood film from a healthy adult |
| حيوانات منوية / sperm | Unavailable `/uploads/` MP4 | Real human sperm microscopy video, transcoded to H.264 MP4 |
| جرثومة المعدة / H.pylori | Unavailable `/uploads/` PNG | Electron micrograph of H. pylori and flagella |
| candida / كانديدا | Unavailable `/uploads/` PNG | Urine sediment with yeast and leukocytes |
| الأنيميا المنجلية / sicklecellanemia | Unavailable `/uploads/` JPEG | Blood film from sickle-cell anemia |
| تكسر الدم الفولي / G6PD | Unavailable `/uploads/` JPEG | Films from confirmed G6PD deficiency, panels A and B |
| خلايا طلائية / Epithelia cell | Unavailable `/uploads/` JPEG | Squamous epithelial cells in urine |
| البكتيريا / Bacteria | Unavailable `/uploads/` JPEG | Bacterial UTI urine microscopy |
| حمض اليوريك / Uric acid | Unavailable `/uploads/` PNG | Uric acid crystals in urine |
| الاملاح / Amorphous | Unavailable `/uploads/` PNG | Amorphous urates in urine |

The other six visitor images already loaded from GitHub and remain unchanged. The extra default-only onion-root case remains in the default library; it is not inserted into the visitor's 16-case list.

## Cause and recovery

The prior URL migration only recognized `/specimens/` objects. These failures were opaque, timestamped `/uploads/` objects on the unavailable old Supabase host. Git history contained additional illustrative assets but not the corresponding upload originals. They were not assumed to be the same photographs. In particular, a schistocyte image is not used for G6PD.

The exact upload URL mapping, replacement details, attribution and SHA-256 hashes are in [manifest.json](assets/recovered/manifest.json). Every replacement has a matching, reviewed description and newly placed annotations. Moving sperm has no fixed annotations; the urine-bacteria image labels only an unambiguous leukocyte rather than guessing an organism's identity from small dots. Names, IDs, categories, order and unrelated metadata remain unchanged. Previous media metadata and a raw cache snapshot remain recoverable in localStorage.

## Verification

- Node regression suite: 14 tests passing, including the observed 16-case cache, unchanged identity/order/categories, exact URL matching, asset hashes, unknown uploads, idempotence, original metadata retention and rectangular-image annotation geometry.
- Local browser: all 16 visitor cases and all eight fresh-session defaults loaded and were visually inspected in the microscope, not merely checked for HTTP 200. Stage images, tray thumbnails and mini-map images decoded successfully. The video played in the stage, thumbnail and mini-map.
- English and Arabic, all category filters, horizontal tray navigation, 10× / 40× / 100× lens changes, Identify, focus adjustment, pan and recenter were exercised. High-power centering was corrected to use the fitted image coordinates and one reviewed landmark, avoiding empty space between distant markers.
- Local video verification used an HTTP server with byte-range support, as required for simultaneous video playback. The video is stored in the repository; no external image/video host is required at runtime.

Replacement media are real microscopy, with attribution displayed beside the case description. Still images are unchanged; the video is transcoded without cuts or speed changes. The simulated lenses do not establish a physical calibration for these source images.
