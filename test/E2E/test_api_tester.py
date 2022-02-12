from playwright.sync_api import Playwright, sync_playwright


def run(pt: Playwright) -> None:
    browser = pt.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to http://localhost:10101/api
    page.goto("http://localhost:10101/api")

    # Click #Dropdown0-option
    page.click("#Dropdown0-option")

    # Click button[role="option"]:has-text("GET")
    page.click("button[role=\"option\"]:has-text(\"GET\")")

    # Click [data-test="url"]
    page.click("[data-test=\"url\"]")

    # Fill [data-test="url"]
    page.fill("[data-test=\"url\"]", "https://run.mocky.io/v3/27c4d516-4d91-4414-91e9-7978e26e8d05")

    # Click [data-test="send"]
    page.click("[data-test=\"send\"]")

    # Click [data-test="headers"]
    page.click("[data-test=\"headers\"]")

    # Click [data-test="key"]
    page.click("[data-test=\"key\"]")

    # Fill [data-test="key"]
    page.fill("[data-test=\"key\"]", "APPLICATION_ID")

    # Click [data-test="val"]
    page.click("[data-test=\"val\"]")

    # Fill [data-test="val"]
    page.fill("[data-test=\"val\"]", "12")

    # Click [data-test="addHeader"]
    page.click("[data-test=\"addHeader\"]")

    # Click [data-test="ok"]
    page.click("[data-test=\"ok\"]")

    # Click [data-test="body"]
    page.click("[data-test=\"body\"]")

    # Click [data-test="text"]
    page.click("[data-test=\"text\"]")

    # Fill [data-test="text"]
    page.fill("[data-test=\"text\"]", "{}")

    # Press ArrowLeft
    page.press("[data-test=\"text\"]", "ArrowLeft")

    # Fill [data-test="text"]
    page.fill("[data-test=\"text\"]", "{\"\"}")

    # Press ArrowLeft
    page.press("[data-test=\"text\"]", "ArrowLeft")

    # Fill [data-test="text"]
    page.fill("[data-test=\"text\"]", "{\"test\"}")

    # Press ArrowRight
    page.press("[data-test=\"text\"]", "ArrowRight")

    # Fill [data-test="text"]
    page.fill("[data-test=\"text\"]", "{\"test\":\"\"}")

    # Press ArrowLeft
    page.press("[data-test=\"text\"]", "ArrowLeft")

    # Fill [data-test="text"]
    page.fill("[data-test=\"text\"]", "{\"test\":\"test\"}")

    # Click [data-test="ok"]
    page.click("[data-test=\"ok\"]")

    # Click #Dropdown124-option
    page.click("data-test=method")

    # Click button[role="option"]:has-text("GET")
    page.click("button[role=\"option\"]:has-text(\"GET\")")

    # Click [data-test="send"]
    page.click("[data-test=\"send\"]")

    # assert "GET" in page.text_content("button[role=\"option\"]:has-text(\"GET\")")
    assert "Send" in page.text_content("data-test=send")

    # ---------------------
    context.close()
    browser.close()


def test_api_test():
    with sync_playwright() as playwright:
        run(playwright)
