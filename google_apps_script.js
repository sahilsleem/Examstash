/**
 * ExamStash — Google Form to GitHub Automation (Google Apps Script)
 * 
 * This script runs automatically whenever someone submits your Google Form.
 * It makes the uploaded PDF public in your Google Drive and triggers
 * a GitHub Action that immediately publishes the paper to ExamStash!
 * 
 * -------------------------------------------------------------
 * HOW TO SET THIS UP (2 MINUTES):
 * -------------------------------------------------------------
 * 1. Open your Google Form in Google Drive.
 * 2. Click the 3 dots (⋮) in the top-right -> Click "Script editor" (or Extensions -> Apps Script).
 * 3. Delete any code in the editor, and paste this entire file.
 * 4. Replace `PASTE_YOUR_GITHUB_TOKEN_HERE` with your GitHub Personal Access Token (classic, repo scope).
 * 5. Click the Clock icon (⏰) on the left sidebar ("Triggers") -> Click "+ Add Trigger":
 *    - Function to run: onFormSubmit
 *    - Deployment: Head
 *    - Event source: From form
 *    - Event type: On form submit
 *    - Click "Save" and authorize the permissions when prompted.
 * -------------------------------------------------------------
 */

// ======================= CONFIGURATION =======================
const GITHUB_REPO_OWNER = "sahilsleem";
const GITHUB_REPO_NAME = "Examstash";
const GITHUB_TOKEN = "PASTE_YOUR_GITHUB_TOKEN_HERE"; // GitHub Personal Access Token (classic) with 'repo' scope

// Telegram Instant Alerts (Get pinged on your phone on new uploads)
const TELEGRAM_BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"; // From @BotFather
const TELEGRAM_CHAT_ID = "PASTE_YOUR_TELEGRAM_CHAT_ID_HERE";     // From @userinfobot
// =============================================================

// Maps form dropdown values to exact ExamStash directory slugs
const COURSE_MAP = {
  "bca": "bca",
  "b.sc. it": "bsc-it",
  "bsc it": "bsc-it",
  "b.sc it": "bsc-it",
  "information technology": "bsc-it",
  "bba": "bba",
  "business administration": "bba",
  "b.com": "bcom",
  "bcom": "bcom",
  "commerce": "bcom",
  "b.com (honours)": "bcom-hons",
  "b.com honours": "bcom-hons",
  "bcom hons": "bcom-hons",
  "b.a. & english honours": "ba",
  "b.a": "ba",
  "ba": "ba",
  "arts": "ba",
  "multidisciplinary & skill courses": "common-courses",
  "common courses": "common-courses",
  "skill courses": "common-courses",
  "b.sc. botany": "bsc-botany",
  "bsc botany": "bsc-botany",
  "botany": "bsc-botany",
  "b.sc. zoology": "bsc-zoology",
  "bsc zoology": "bsc-zoology",
  "zoology": "bsc-zoology",
  "b.sc. biotechnology": "bsc-biotechnology",
  "bsc biotechnology": "bsc-biotechnology",
  "biotechnology": "bsc-biotechnology",
  "b.sc. biochemistry": "bsc-biochemistry",
  "bsc biochemistry": "bsc-biochemistry",
  "biochemistry": "bsc-biochemistry",
  "b.sc. chemistry": "bsc-chemistry",
  "bsc chemistry": "bsc-chemistry",
  "chemistry": "bsc-chemistry",
  "b.sc. mathematics": "bsc-mathematics",
  "bsc mathematics": "bsc-mathematics",
  "mathematics": "bsc-mathematics",
  "b.sc. medical": "bsc-medical",
  "bsc medical": "bsc-medical",
  "b.sc. non-medical": "bsc-non-medical",
  "bsc non-medical": "bsc-non-medical",
  "b.sc. physics": "bsc-physics",
  "bsc physics": "bsc-physics",
  "physics": "bsc-physics"
};

function onFormSubmit(e) {
  try {
    const itemResponses = e.response.getItemResponses();
    let course = "bca";
    let semester = "semester-1";
    let resourceType = "paper";
    let subject = "Past Paper";
    let driveLink = "";

    for (let i = 0; i < itemResponses.length; i++) {
      const item = itemResponses[i];
      const title = item.getItem().getTitle().toLowerCase();
      const val = item.getResponse();

      if (title.indexOf("course") !== -1 || title.indexOf("programme") !== -1 || title.indexOf("stream") !== -1) {
        const key = String(val).toLowerCase().trim();
        course = COURSE_MAP[key] || slugify(key);
      } else if (title.indexOf("semester") !== -1 || title.indexOf("sem") !== -1) {
        const m = String(val).match(/[1-6]/);
        semester = m ? "semester-" + m[0] : "semester-1";
      } else if (title.indexOf("resource") !== -1 || title.indexOf("type") !== -1) {
        resourceType = String(val).toLowerCase().indexOf("syllabus") !== -1 ? "syllabus" : "paper";
      } else if (title.indexOf("subject") !== -1 || title.indexOf("name") !== -1 || title.indexOf("year") !== -1) {
        subject = String(val).trim();
      } else if (title.indexOf("upload") !== -1 || title.indexOf("file") !== -1 || title.indexOf("paper") !== -1 || title.indexOf("pdf") !== -1) {
        // In Google Forms, file upload returns an array of Google Drive file IDs
        if (Array.isArray(val) && val.length > 0) {
          const fileId = val[0];
          try {
            const file = DriveApp.getFileById(fileId);
            // Grant "anyone with link can view" permission so visitors can access the PDF
            file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
            driveLink = "https://drive.google.com/file/d/" + fileId + "/view?usp=sharing";
          } catch (fileErr) {
            Logger.log("Permission notice: " + fileErr);
            driveLink = "https://drive.google.com/file/d/" + fileId + "/view?usp=sharing";
          }
        }
      }
    }

    if (!driveLink) {
      Logger.log("Notice: No file uploaded in submission.");
      return;
    }

    Logger.log("Triggering ExamStash deployment for: " + course + " | " + semester + " | " + subject);

    // Call GitHub repository_dispatch API
    const url = "https://api.github.com/repos/" + GITHUB_REPO_OWNER + "/" + GITHUB_REPO_NAME + "/dispatches";
    const payload = {
      event_type: "new-paper",
      client_payload: {
        course: course,
        semester: semester,
        subject: subject,
        type: resourceType,
        link: driveLink
      }
    };

    const options = {
      method: "post",
      contentType: "application/json",
      headers: {
        "Authorization": "Bearer " + GITHUB_TOKEN,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "ExamStash-Form-Automation"
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    Logger.log("GitHub Response Code: " + response.getResponseCode());
    Logger.log("GitHub Response Content: " + response.getContentText());

    // Send Telegram alert to your phone
    sendTelegramAlert(course, semester, subject, resourceType, driveLink);

  } catch (err) {
    Logger.log("Error during onFormSubmit: " + err);
  }
}

function slugify(text) {
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
}

/**
 * Run this function manually by selecting 'testTrigger' in the toolbar
 * and clicking 'Run' to test your GitHub token and see instant execution logs!
 */
function testTrigger() {
  Logger.log("Testing GitHub connection with owner: " + GITHUB_REPO_OWNER + ", repo: " + GITHUB_REPO_NAME);
  const url = "https://api.github.com/repos/" + GITHUB_REPO_OWNER + "/" + GITHUB_REPO_NAME + "/dispatches";
  const payload = {
    event_type: "new-paper",
    client_payload: {
      course: "bca",
      semester: "semester-1",
      subject: "Test Connection",
      type: "paper",
      link: "https://drive.google.com/file/d/1poLHK7rC1-oPeNGhmk---6BYMWntdeyA/view?usp=sharing"
    }
  };

  const options = {
    method: "post",
    contentType: "application/json",
    headers: {
      "Authorization": "Bearer " + GITHUB_TOKEN,
      "Accept": "application/vnd.github.v3+json",
      "User-Agent": "ExamStash-Form-Automation"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  Logger.log("GitHub Response Code: " + response.getResponseCode());
  Logger.log("GitHub Response Content: " + response.getContentText());
  if (response.getResponseCode() === 204) {
    Logger.log("SUCCESS! Your GitHub token is working perfectly.");
  } else if (response.getResponseCode() === 401) {
    Logger.log("ERROR: Token is invalid or expired. Check your GitHub Personal Access Token.");
  } else if (response.getResponseCode() === 404) {
    Logger.log("ERROR: Repository not found or token lacks 'repo' permission.");
  }
}

/**
 * Sends an instant notification to your Telegram whenever a paper is submitted.
 */
function sendTelegramAlert(course, semester, subject, resourceType, driveLink) {
  if (!TELEGRAM_BOT_TOKEN || TELEGRAM_BOT_TOKEN.indexOf("PASTE_") === 0 || !TELEGRAM_CHAT_ID || TELEGRAM_CHAT_ID.indexOf("PASTE_") === 0) {
    Logger.log("Telegram notification skipped: Bot token or Chat ID not configured.");
    return;
  }

  try {
    const text = "📄 *New Paper Contributed to ExamStash!*\n\n" +
                 "📚 *Programme:* " + course.toUpperCase() + "\n" +
                 "🎓 *Semester:* " + semester.replace("-", " ").toUpperCase() + "\n" +
                 "📖 *Subject:* " + subject + "\n" +
                 "📑 *Type:* " + resourceType.toUpperCase() + "\n" +
                 "🔗 [View Uploaded File on Google Drive](" + driveLink + ")\n\n" +
                 "🚀 *Status:* GitHub Action triggered — site is updating live!";

    const tgUrl = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage";
    const payload = {
      chat_id: TELEGRAM_CHAT_ID,
      text: text,
      parse_mode: "Markdown",
      disable_web_page_preview: false
    };

    const options = {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const tgRes = UrlFetchApp.fetch(tgUrl, options);
    Logger.log("Telegram Alert Sent! Status Code: " + tgRes.getResponseCode());
  } catch (tgErr) {
    Logger.log("Notice (Telegram alert): " + tgErr);
  }
}

/**
 * Test your Telegram Bot connection!
 * Select 'testTelegram' in the toolbar and click 'Run'.
 * You should immediately receive a ping on your phone!
 */
function testTelegram() {
  Logger.log("Testing Telegram bot connection...");
  if (!TELEGRAM_BOT_TOKEN || TELEGRAM_BOT_TOKEN.indexOf("PASTE_") === 0 || !TELEGRAM_CHAT_ID || TELEGRAM_CHAT_ID.indexOf("PASTE_") === 0) {
    Logger.log("ERROR: Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID first.");
    return;
  }

  const tgUrl = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage";
  const payload = {
    chat_id: TELEGRAM_CHAT_ID,
    text: "🎉 *ExamStash Telegram Bot is connected and working!*\n\nYou will receive an alert here whenever a student submits a paper.",
    parse_mode: "Markdown"
  };

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const res = UrlFetchApp.fetch(tgUrl, options);
  Logger.log("Telegram Response Code: " + res.getResponseCode());
  Logger.log("Telegram Response Body: " + res.getContentText());
  if (res.getResponseCode() === 200) {
    Logger.log("SUCCESS! Check your Telegram app for the message.");
  } else {
    Logger.log("FAILED. Check that you started your bot in Telegram and that your Bot Token and Chat ID are correct.");
  }
}

