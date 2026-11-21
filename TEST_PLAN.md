# Test Plan - DaveAI QA Assignment

## Scope and targets

- **API target:** Reqres (`https://reqres.in`), an external public test API. Use the requested classic demo endpoints without an API key and keep requests within the shared demo's low daily limit.
- **UI target:** `https://www.iamdave.ai`, the actual DaveAI company website.
- **Browser:** Chrome through Selenium WebDriver. UI automation should use `WebDriverWait` and Selenium expected conditions instead of fixed sleeps, and should always close the browser through fixture teardown. Capture a screenshot on UI failure where practical.
- **Credentials:** None are specified or hardcoded.
- **Safety:** UI tests must not submit a contact inquiry.

The homepage title and main heading were verified in the live DOM. The Contact link used by UI-02 is in the footer navigation and leads to `/contact-us/`; the site uses smooth scrolling, so the test scrolls the link into view before clicking. The Contact page visibly presents Name, Email, Company name, and Phone number inputs. Selenium locators were selected from the live DOM.

## API test cases

| Test ID | Description | Test steps | Expected result |
|---|---|---|---|
| API-01 | List users on page 2 | Send `GET /api/users?page=2`; parse the response as JSON; inspect the pagination and user-list fields. | HTTP 200; valid JSON object with page 2 and a user list whose entries contain user fields. |
| API-02 | Retrieve user 2 | Send `GET /api/users/2`; parse the response as JSON; inspect the returned user record. | HTTP 200; valid JSON containing a `data` user record with ID 2 and user fields. The current demo response identifies this record as Janet Weaver (`janet.weaver@reqres.in`). |
| API-03 | Request a missing user | Send `GET /api/users/23`. | HTTP 404. |
| API-04 | Login without a password | Send `POST /api/login` with an email field and omit the password. | HTTP 400 and a JSON error response. |

## UI test cases

| Test ID | Description | Test steps | Expected result |
|---|---|---|---|
| UI-01 | Load the DaveAI homepage | Open the configured UI base URL; wait for the page to load; inspect the document title and main heading. | The homepage loads successfully; title is `AI-Native Automotive Intelligence Platform | DaveAI`; main heading is `Automotive Intelligence Across Every Function`. |
| UI-02 | Navigate to Contact | From the homepage, locate the Contact link in the footer navigation; scroll it into view; click it and wait for navigation. | Browser navigates to the DaveAI Contact page at `/contact-us/`, and the page content is visible. |
| UI-03 | Verify Contact form fields | On the Contact page, locate the form and inspect its Name, Email, Company name, and Phone number inputs. | All four requested inputs are present and available for interaction. |
| UI-04 | Enter and clear the Name field | Locate the Name input; enter a sample value; verify the field contains that value; clear the field; verify it is empty. | The sample value is accepted and can be cleared. Do not submit the form or send a contact inquiry. |

## Implementation notes

- Keep API and UI tests in their separate `tests/api/` and `tests/ui/` folders.
- Use the reusable base URLs from `config/settings.py`.
- Inspect the live DOM before choosing Selenium locators; prefer accessible labels or stable rendered attributes.
- Use explicit waits for page and element state, configure Chrome WebDriver, and ensure teardown runs after both passing and failing tests.
- If a UI test fails, save a screenshot under `screenshots/` where practical.
- All four API and all four UI test functions are implemented in their separate test directories. Recorded suite results are documented in `README.md`.