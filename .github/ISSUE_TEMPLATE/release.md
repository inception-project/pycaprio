---
name: Release
about: Create a new release of pycaprio

---

**Checklist**

- [ ] Make sure all issues for the milestone are completed, otherwise move them
- [ ] Checkout the `main` branch
- [ ] Bump the version in `pyproject.toml` to a stable one, e.g. `version = "0.4.0"`, commit and push
- [ ] Check and wait that the build completed. 
- [ ] Create a tag for that version and push it
- [ ] Wait for the build and Pypi to show the new version
- [ ] Bump the version to the next development version, commit and push that.
- [ ] Convert the tag to a release on GitHub, write release note based on issues in the respective milestone
- [ ] Create a new milestone
