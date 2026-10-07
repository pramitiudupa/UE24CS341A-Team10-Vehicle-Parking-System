# Software Test Plan

Upload the team's Software Test Plan v1.1 here.

SAD v1.1 §3.8 maps every SRS v1.1 requirement to the STP v1.1 test cases (`TC-AUTH`, `TC-VEH`, `TC-SLOT`, `TC-ENT`, `TC-EXT`, `TC-FEE`, `TC-SRCH`, `TC-REP`, `TC-PERF`, `TC-CONC`, `TC-REL`, `TC-USAB`, `TC-PORT`, `TC-SEC`). The role matrix that TC-SEC-02 needs is in SAD §4.3.

Before final submission, fix these differences between the STP and SRS v1.1:
- **Old requirement numbers:** the STP still uses FR-01…FR-23, NFR-01…NFR-07 and SEC-01…SEC-07. Renumber them to match the SRS.
- **Missing test cases:** the requirements marked "Not yet in STP" in SAD §3.8 need test cases: FR-04, FR-10, FR-12, FR-26, FR-31, FR-33, NFR-02, NFR-07, NFR-09, NFR-10, NFR-11, SEC-06, SEC-08, SEC-09 and BR-06.
- **Grace period:** the STP treats it as fixed, but the SRS lets the administrator configure it (FR-26).
- **Vehicle Owner functions:** the STP lists them as removed, but the SRS still includes them.
- **Slot Availability login:** TC-SEC-01 expects the Slot Availability page to require login, but SRS SEC-01 allows it without login.
