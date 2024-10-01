import datetime
import os
import pytest
from playwright.sync_api import sync_playwright
import allure

# Set up the directory for screenshots
screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
os.makedirs(screenshot_dir, exist_ok=True)  # Create the directory if it doesn't exist


@allure.step('Open TodoMVC')
def open_todomvc(page):
    page.goto("https://todomvc.com/examples/react/dist/")
    assert page.url == "https://todomvc.com/examples/react/dist/"


@allure.step('Add TODO item')
def add_todo_item(page, todo_text):
    page.fill('.new-todo', todo_text)
    page.press('.new-todo', 'Enter')


@allure.step('Delete TODO item')
def delete_todo_item(page, item_index):
    todo_item = page.locator('.todo-list li').nth(item_index)
    delete_button = todo_item.locator('.destroy')

    # Hover over the todo item to make the delete button visible
    todo_item.hover()  # Ensure the cursor is on the item to show the delete button
    delete_button.wait_for(state='visible')  # Ensure delete button is visible
    delete_button.click()  # Click the delete button


@allure.step('Mark TODO item as completed')
def complete_todo_item(page, item_index):
    todo_item = page.locator('.todo-list li').nth(item_index)
    todo_item.locator('.toggle').check()


@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@allure.title('TodoMVC UI Testing')
def test_todomvc(browser_context):
    page = browser_context

    # Step 1: Open TodoMVC
    open_todomvc(page)
    page.screenshot(path=os.path.join(screenshot_dir, 'screenshot01.png'))  # Screenshot after opening TodoMVC

    # Set up dates
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # Step 3: Add a TODO item with the current date
    add_todo_item(page, f"TODO 1 - {current_date}")
    page.screenshot(path=os.path.join(screenshot_dir, 'screenshot02.png'))  # Screenshot after adding first TODO

    # Step 4: Verify that the new to-do item appears in the list
    assert page.locator('.todo-list li').nth(0).text_content() == f"TODO 1 - {current_date}"

    # Step 5: Add a TODO item with tomorrow's date
    add_todo_item(page, f"TODO 2 - {tomorrow_date}")
    page.screenshot(path=os.path.join(screenshot_dir, 'screenshot03.png'))  # Screenshot after adding second TODO

    # Step 6: Mark the current date TODO item as completed
    complete_todo_item(page, 0)
    page.screenshot(path=os.path.join(screenshot_dir, 'screenshot04.png'))  # Screenshot after completing first TODO

    # Step 7: Verify that the item is displayed as completed
    assert 'completed' in page.locator('.todo-list li').nth(0).get_attribute('class')

    # Step 8: Delete the TODO 2 item
    delete_todo_item(page, 1)
    page.screenshot(path=os.path.join(screenshot_dir, 'screenshot05.png'))  # Screenshot after deleting second TODO

    # Step 9: Verify that the item is removed from the list
    assert not page.locator('.todo-list li').nth(1).is_visible()

    # Step 10: Take a final screenshot of the remaining TODO list
    page.screenshot(path=os.path.join(screenshot_dir, 'screenshot06.png'))  # Final state of the todo list

    # Step 11: Retrieve video file
    video_file_path = os.path.join(os.getcwd(), 'video.webm')
    print(f"Video saved at: {video_file_path}")


# Run the tests
if __name__ == "__main__":
    pytest.main()
