import logging

import azure.functions as func

from app.automation.worker import NewsAutomation

app = func.FunctionApp()


@app.schedule(
    schedule="0 * * * * *", arg_name="timer", run_on_startup=True, use_monitor=False
)
def FacebookPost(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.info("The timer is past due!")

    automation = NewsAutomation()
    post_id = automation.run()

    logging.info(f"Post published succeesfully! Post ID: {post_id}")
    logging.info("Python timer trigger function executed.")
