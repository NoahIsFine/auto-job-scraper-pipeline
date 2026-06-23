# Windows Task Scheduler Setup Guide

This guide explains how to configure Windows Task Scheduler to run the Job Scraper pipeline automatically on a recurring schedule (default: every Monday at 9:00 AM).

There are two ways to set this up: the **Automated Method** (Recommended) and the **Manual Method**.

---

## Method 1: Automated Setup (Recommended)

You can automatically configure the scheduled task using the included setup script.

1. Locate the `setup_task.bat` file in the project folder.
2. **Right-click** `setup_task.bat` and select **"Run as administrator"**.
3. A command prompt window will open, configure the task, and print `[SUCCESS] Scheduled task created successfully!`.
4. Press any key to close the window.

The task is now created! It will automatically run the scraper every Monday at 9:00 AM. 

*(If you ever want to change the time or day, you can open the Task Scheduler app and edit the "Auto Job Scraper Pipeline" task manually).*

---

## Method 2: Manual Setup

If you prefer to configure the task yourself, follow these step-by-step instructions.

1. **Open Task Scheduler**
   - Press the `Windows` key on your keyboard.
   - Type `Task Scheduler` and hit Enter to open the app.

2. **Create a Basic Task**
   - In the right-hand panel (Actions pane), click **"Create Basic Task..."**.
   - **Name:** Type `Auto Job Scraper Pipeline` (or whatever you prefer) and click **Next**.

3. **Set the Trigger (Schedule)**
   - Select **Weekly** and click **Next**.
   - **Start Date:** Leave today's date, or choose the upcoming Monday.
   - **Time:** Change the time to `09:00:00 AM` (or your preferred time).
   - **Recur every:** `1` weeks on: Check the box next to **Monday**.
   - Click **Next**.

4. **Set the Action**
   - Select **"Start a program"** and click **Next**.
   - Under Program/script, click **"Browse..."** and navigate to your cloned repository folder.
   - Select the `run_scraper.bat` file and click **Open**.
   - Click **Next**.

5. **Finish**
   - Review your settings on the final screen.
   - Click **Finish**.

---

### Optional Pro-Tips
- **Test it manually:** You can find your new task in the "Task Scheduler Library" (left panel), right-click it, and select "Run" to test that it opens the command prompt and fires the script.
- **Run silently:** By default, a black command prompt window will briefly appear when the task runs. If you want it to run completely silently in the background, you can right-click the task > Properties > Check the box for "Run whether user is logged on or not" (this requires entering your Windows password).
