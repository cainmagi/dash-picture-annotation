# Dash Picture Annotation

{:toc}

## CHANGELOG

### 0.1.0 @ 11/10/2024

#### :wrench: Fix

1. Fix: Lossen the input argument type of `sanitize_data(...)` and `sanitize_data_item(...)`. Previously, passing not sanitized data to these functions will cause type checking issues.

### 0.1.0 @ 11/06/2024

#### :mega: New

1. Add typehints: `AnnoStyle`, `DashSelectOptionItem`, and `Size`.

#### :wrench: Fix

1. Fix: Fix few typos in the docstrings.
2. Fix: Fix the aliases in the top-level package.

#### :floppy_disk: Change

1. Upgrade Yarn to `v4.5.1`.
2. Downgrade React to `v18.2.x` because the `defaultProps` which is used by Dash is marked as deprecated since `v18.3.0`.

### 0.1.0 @ 11/04/2024

#### :mega: New

1. Create this project.
2. Finish the react implement `src` and the automatically generated package `dash_picture_annotation`.
3. Add the React demo `App.js`.
4. Add the Dash demo `usage.py` and more examples in `./examples`.
5. Add the unit tests in `./tests`.
6. Add configurations `pyproject.toml`.
7. Add the devloper's environment folder `./docker` and the `Dockerfile`.
8. Add GitHub workflows and issue/PR templates.
9. Add the banner in the readme file.

#### :wrench: Fix

1. Fix: Fix the video link in the readme file.
