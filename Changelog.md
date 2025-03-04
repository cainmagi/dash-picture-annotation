# Dash Picture Annotation

[toc]

## CHANGELOG

### 0.2.1 @ 03/04/2025

#### :mega: New

1. Bump the document to the new version `0.2.1`.
2. Add the documents for the new features `DashPictureAnnotation(init_scale=...)`, `dpa.Scale`, and `dpa.sanitize_scale`.
3. Add source file links for the new version `0.2.1`.

#### :wrench: Fix

1. Fix: Add the missing links in the entry pages of the modules and packages.
2. Fix: Correct typos in the legacy documents.
3. Fix: Bump the yarn typescript support from `4.0.0` to `4.0.1`. It solves an compatibility issue with `typescript@5.8.x`.

#### :floppy_disk: Change

1. Bump the `yarn` version from `4.6.0` to `4.7.0`.
2. Bump the `docusaurus` version from `3.6.3` to `3.7.0`.
3. Bump the `typescript` version from `5.7.2` to `5.8.2`.

### 0.1.2 @ 12/02/2024

#### :wrench: Fix

1. Fix: Correct typos, where the "*Dash Picture Annotation*" is not correctly named.

#### :floppy_disk: Change

1. Bump the yarn version from `4.5.3` to `4.6.0`.

### 0.1.2 @ 12/02/2024

#### :wrench: Fix

1. Fix: Correct a typo in the code highlight in the page `/docs/examples/options`.
2. Fix: Correct a style issue in the page `/docs/usages/image` of the zh-cn document.
3. Fix: Correct a bad-located link in `/zh-cn/docs/usages/image`.
4. Fix: Correct the spacing in `/zh-cn/docs/apis/utilities/sanitize_data` and `.../compare_anno_marks`.
5. Fix: Correct the link of the translation in `/zh-cn/docs/apis/utilities/get_data_items_by_regex`.

#### :floppy_disk: Change

1. Bump the document version to `0.1.2`.

### 0.1.1 @ 12/01/2024

#### :mega: New

1. Provide the translation of zh-cn.

#### :wrench: Fix

1. Fix: Correct typos and ambiguity in the whole document.

#### :floppy_disk: Change

1. Make the example section in the sidebar collapsed by default.

### 0.1.0 @ 11/29/2024

#### :wrench: Fix

1. Fix: Switch from the hook `useDocsPreferredVersion` to `useDocsVersion`. This change fix the issue caused on the change of the browser navigation.

#### :floppy_disk: Change

1. Bump the `yarn` version from `4.5.1` to `4.5.3`.
2. Bump the `docusaurus` version from `3.6.1` to `3.6.3`.
3. Bump the `typescript` version from `5.6.3` to `5.7.2`.

### 0.1.0 @ 11/05/2024

#### :mega: New

1. Create this project.
2. Upload the first version of the document, containing the tutorial and API docs.

#### :wrench: Fix

1. Fix：Temporarily remove the `zh-cn` local because it is not ready yet.
2. Fix: `Plyr` component cannot be imported by the server-side rendering. Move the component to the client-side only rendering. This change will let the component only appears when it is accessed by a browser.
3. Fix: Fix the CSS style incompatibility issue of the `video.js`.
4. Fix: Add two missing pages to the side bar.

#### :floppy_disk: Change

1. Drop [`plyr-react`](https://github.com/chintan9/plyr-react) because it cannot be used for rendering a static site. Migrate to [`video.js`](https://videojs.com).
