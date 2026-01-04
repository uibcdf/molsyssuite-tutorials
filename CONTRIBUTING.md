# Contributing to MolSysSuite Tutorials

## Add a new tutorial

1. Create a directory:
   - `tutorials/<tool>/<slug>/` (e.g. `tutorials/molsysmt/quickstart/`)
2. Add `README.md` using `templates/tutorial-README.md`.
3. Add the notebook/markdown content.
4. Include an `environment.yml` when possible.
5. Update the corresponding tool repository pointer (`resources/tutorials.yml`).

## Notes

- Keep tutorials runnable and minimal.
- If API changes, update the tutorial and note the tested versions.
