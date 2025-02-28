from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# SQLite Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///youtube_config.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Default YouTube Parameters
DEFAULT_SETTINGS = {
    "youtube_id": "0mCsluv5FXA",
    "youtube_height": "360",
    "youtube_width": "640",
    "youtube_json_params": "{}"
}

# Database Model


class YouTubeConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(
        db.String(50), default=DEFAULT_SETTINGS["youtube_id"])
    youtube_height = db.Column(
        db.String(10), default=DEFAULT_SETTINGS["youtube_height"])
    youtube_width = db.Column(
        db.String(10), default=DEFAULT_SETTINGS["youtube_width"])
    youtube_json_params = db.Column(
        db.Text, default=DEFAULT_SETTINGS["youtube_json_params"])


# Create the database if it doesn't exist
with app.app_context():
    db.create_all()
    if YouTubeConfig.query.count() == 0:
        db.session.add(YouTubeConfig(**DEFAULT_SETTINGS))
        db.session.commit()

# HTML Template for the YouTube Embed Page
TEMPLATE = """
<!doctype html>
<html lang="en-US">
 <head>
  <style>
   :root {
    --app-background-color: white;
   }
   body {
    margin: 0;
    padding: 0;
   }
   @media (prefers-color-scheme: dark) {
    :root {
     --app-background-color: #111111ff;
    }
   }
  </style>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0"/>
  <script id="embed-resize-handler">
   window.sentMessages = [];
   window.embedHeight = 0;
   window.targetSelector = '';

   window.sendHeightToNativeOS = (newHeight, source) => {
    if (window.webkit?.messageHandlers?.heightCallback) {
     window.webkit.messageHandlers.heightCallback.postMessage(newHeight);
    } else if (typeof androidArticleHandler !== 'undefined') {
     androidArticleHandler.setNewHeight(newHeight);
    }
    sentMessages.push(`Sent height ${newHeight} from ${source}`);
   };

   window.observer = new ResizeObserver(([entry]) => {
    const measureEl = window.targetSelector
     ? entry.target.querySelector(window.targetSelector)
     : entry.target;

    if (measureEl) {
     const { height: newHeight } = measureEl.getBoundingClientRect();
     if (window.embedHeight === newHeight) return;
     window.embedHeight = newHeight;
     window.sendHeightToNativeOS(newHeight, 'ResizeObserver');
    }
   });

   window.initializeEmbedMessaging = (observeEl, targetSelector = '') => {
    const { height: initialHeight } = observeEl.getBoundingClientRect();
    window.sendHeightToNativeOS(initialHeight, 'initial');
    window.embedHeight = initialHeight;
    window.targetSelector = targetSelector;
    window.observer.observe(observeEl);
   };
  </script>
 </head>
 <body>
  <style>
   body { background-color: var(--app-background-color); }
   iframe { display: block; margin: 0 auto; }
  </style>
  <div id="ytplayer"></div>

  <script id="youtube-load-player">
   var tag = document.createElement('script');
   tag.src = 'https://www.youtube.com/player_api';
   var firstScriptTag = document.getElementsByTagName('script')[0];
   firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

   var player;

   const height = "{{ height }}";
   const width = "{{ width }}";
   let playerVars = {};

   try {
    const templateVars = `{{ youtube_json_params }}`;
    if (templateVars) {
     playerVars = JSON.parse(decodeURIComponent(templateVars));
    }
   } catch {
    playerVars = {};
   }

   function onYouTubePlayerAPIReady() {
    player = new YT.Player('ytplayer', {
     height,
     width,
     videoId: "{{ youtube_id }}",
     playerVars,
     events: {
      onReady: (event) => {
       const playerEl = event.target.getIframe();
       if (playerEl) window.initializeEmbedMessaging(playerEl);
      },
     },
    });
   }
  </script>
  <a href="/config">Change Video Settings</a>
 </body>
</html>
"""

# Configuration Page
CONFIG_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <title>Configure YouTube Embed</title>
</head>
<body>
    <h2>Configure YouTube Video</h2>
    <form action="/config" method="post">
        <label for="youtube_id">YouTube Video ID:</label>
        <input type="text" name="youtube_id" value="{{ youtube_id }}" required /><br>

        <label for="youtube_height">Height:</label>
        <input type="text" name="youtube_height" value="{{ youtube_height }}" required /><br>

        <label for="youtube_width">Width:</label>
        <input type="text" name="youtube_width" value="{{ youtube_width }}" required /><br>

        <label for="youtube_json_params">JSON Params:</label>
        <input type="text" name="youtube_json_params" value='{{ youtube_json_params }}' required /><br>

        <input type="submit" value="Save">
    </form>
    <br>
    <a href="/">Back to Video</a>
</body>
</html>
"""


@app.route("/")
def home():
    """Loads the YouTube video with stored or default settings."""
    config = YouTubeConfig.query.first()
    return render_template_string(
        TEMPLATE,
        youtube_id=config.youtube_id,
        height=config.youtube_height,
        width=config.youtube_width,
        youtube_json_params=config.youtube_json_params,
    )


@app.route("/config", methods=["GET", "POST"])
def config():
    """Configuration page to update YouTube embed settings."""
    config = YouTubeConfig.query.first()

    if request.method == "POST":
        config.youtube_id = request.form["youtube_id"]
        config.youtube_height = request.form["youtube_height"]
        config.youtube_width = request.form["youtube_width"]
        config.youtube_json_params = request.form["youtube_json_params"]

        db.session.commit()
        return redirect(url_for("home"))

    return render_template_string(
        CONFIG_TEMPLATE,
        youtube_id=config.youtube_id,
        youtube_height=config.youtube_height,
        youtube_width=config.youtube_width,
        youtube_json_params=config.youtube_json_params,
    )


if __name__ == "__main__":
    app.run(debug=True)
