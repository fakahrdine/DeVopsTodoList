import unittest
import os
import json

# Import our Flask application script
import app

# Set the TODO_FILE to a temporary testing file so we don't overwrite the user's real tasks!
TEST_TODO_FILE = "test_tasks.json"
app.TODO_FILE = TEST_TODO_FILE

class TodoAppTestCase(unittest.TestCase):

    # setUp runs BEFORE every single test function automatically
    def setUp(self):
        # Create a test client which acts like a fake web browser inside Python
        self.client = app.app.test_client()
        
        # Start every test with a fresh, empty JSON file
        with open(TEST_TODO_FILE, 'w') as file:
            json.dump([], file)

    # tearDown runs AFTER every single test function automatically
    def tearDown(self):
        # Clean up the test file so it doesn't leave junk on the hard drive
        if os.path.exists(TEST_TODO_FILE):
            os.remove(TEST_TODO_FILE)

    def test_homepage(self):
        # We simulate navigating to the homepage '/' using our fake browser client
        response = self.client.get('/')
        
        # We assert (expect) that the web server answers with a 200 OK status code
        self.assertEqual(response.status_code, 200)
        
        # We assert that the title "My Tasks" is literally inside the HTML returned
        self.assertIn(b"My Tasks", response.data)

    def test_add_task(self):
        # We simulate a user submitting the HTML form with a POST request
        response = self.client.post('/add', data={'title': 'Learn Unit Testing'})
        
        # After a successful task add, the server redirects (Status code 302 means redirect)
        self.assertEqual(response.status_code, 302)
        
        # Let's verify the task actually saved to our TEST JSON file
        with open(TEST_TODO_FILE, 'r') as file:
            tasks = json.load(file)
            
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], 'Learn Unit Testing')
        self.assertFalse(tasks[0]['completed'])

    def test_complete_task(self):
        # First, add a task directly to the file to set up the test data
        with open(TEST_TODO_FILE, 'w') as file:
            json.dump([{"title": "Task to Complete", "completed": False}], file)
            
        # Simulate clicking the "Done" button for the first task (index 0)
        response = self.client.post('/complete/0')
        self.assertEqual(response.status_code, 302)
        
        # Verify it was actually marked as completed in the file
        with open(TEST_TODO_FILE, 'r') as file:
            tasks = json.load(file)
            
        self.assertTrue(tasks[0]['completed'])

# This runs the tests if we execute the file directly
if __name__ == '__main__':
    unittest.main()
