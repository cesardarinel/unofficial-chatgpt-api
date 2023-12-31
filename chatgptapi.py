from playwright.sync_api import sync_playwright
import time

class chatgtp:
    

    def __init__(self,ruta=None,visible=True) -> None:
        self.int_sync_playwright(r=ruta,vista=visible)
        if not self.is_logged_in():
            print("Please log in to OpenAI Chat")
            print("Press enter when you're done")
            input()
        
    def int_sync_playwright(self,r=None,vista=True):
        if r is None:
            r="./playwright/firefox/data"
        self.close()
        self.PLAY = sync_playwright().start()
        self.BROWSER = self.PLAY.firefox.launch_persistent_context(
            user_data_dir=r,
            headless=vista,
        )
        self.PAGE = self.BROWSER.new_page()
        self.PAGE.goto("https://chat.openai.com/")

    def get_input_box(self):
        return self.PAGE.query_selector("textarea")

    def is_logged_in(self):
        # See if we have a textarea with data-id="root"
        return self.get_input_box() is not None
    
    def is_loading_response(self) -> bool:
        """See if the send button is diabled, if it does, we're not loading"""
        return self.PAGE.query_selector('button div.text-2xl') != None
    
    def get_last_message(self):
        """Get the latest message"""
        while self.is_loading_response():
            time.sleep(0.25)
        page_elements = self.PAGE.query_selector_all(".markdown.prose")
        last_element = page_elements.pop()
        return last_element.inner_html()
    
    def send_message(self,message)-> str:
        # Send the message
        box = self.get_input_box()
        box.click()
        box.fill(message)
        box.press("Enter")
        return self.get_last_message()

    def regenerate_response(self):
        """Clicks on the Try again button.
        Returns None if there is no button"""
        try_again_button = self.PAGE.query_selector("button:has-text('Try again')")
        if try_again_button is not None:
            try_again_button.click()
        return try_again_button

    def get_reset_button(self):
        """Returns the reset thread button (it is an a tag not a button)"""
        lista=self.PAGE.query_selector_all('nav.flex li.relative')
        if len(lista) > 0:
            self.PAGE.query_selector('nav.flex li.relative').click()
            self.PAGE.wait_for_timeout(1000)
            self.PAGE.query_selector("button.p-1:nth-child(2)").click()
            self.PAGE.query_selector('button.btn-danger').click()
        #print("No tenemos historial a borrar ")

    def close(self):
        try:
            self.PAGE.close()
            self.BROWSER.close()
            self.PLAY.stop()
        except:
            None
        time.sleep(0.25)