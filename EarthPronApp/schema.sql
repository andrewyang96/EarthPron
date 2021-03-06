CREATE TABLE hot_posts(
    url         TEXT NOT NULL,
    image_url   TEXT NOT NULL,
    title       TEXT NOT NULL,
    subreddit   TEXT NOT NULL,
    query       TEXT NOT NULL,
    created_utc INT NOT NULL,
    lat         REAL NOT NULL,
    lng         REAL NOT NULL,
    PRIMARY KEY (url, created_utc)
);

CREATE TABLE update_history(
    timestamp   INT NOT NULL,
    posts_added INT NOT NULL
);
